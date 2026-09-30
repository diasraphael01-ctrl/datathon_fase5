from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from data_prep_dashboard import carregar_base_analitica, carregar_base_longitudinal
from dashboard_utils import (
    configurar_pagina,
    titulo_pagina,
    box_perguntas,
    aplicar_filtros,
    kpi,
    preparar_eixo,
)
from model_support import carregar_artefato_modelo


configurar_pagina("Risco, Evolução e Impacto do Programa")

df_full = carregar_base_analitica()
df = aplicar_filtros(df_full, "p5")

titulo_pagina(
    "PAINEL DE RISCO, EVOLUÇÃO E IMPACTO DO PROGRAMA",
)

if df.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi("INDE médio", f"{df['INDE_analitico'].mean():.2f}")
with c2:
    kpi("Alunos únicos", f"{df['RA'].nunique():,}".replace(",", "."))
with c3:
    kpi("Tempo médio no programa", f"{df['Tempo_programa'].mean():.1f} anos")
with c4:
    pct_def = df["Defasagem"].lt(0).mean() * 100
    kpi("Com defasagem", f"{pct_def:.1f}%")

st.markdown("---")
left, right = st.columns(2)

scores = pd.DataFrame()
importancias = pd.Series(dtype=float)
threshold = None
ano_risco = None

try:
    BASE_DIR = Path(__file__).resolve().parent.parent
    CAMINHO_MODELO = (
        BASE_DIR
        / "modelo"
        / "random_forest_balanceado_threshold_025.joblib"
    )

    artefato = carregar_artefato_modelo(CAMINHO_MODELO)

    preprocessador = artefato["preprocessador"]
    modelo = artefato["modelo"]
    threshold = float(artefato["threshold"])
    features_entrada = list(artefato["features_entrada"])

    ano_risco = int(df["Ano"].max())
    base_score = df[df["Ano"] == ano_risco].copy()

    base_score["INDE_atual"] = base_score["INDE_analitico"]

    colunas_ausentes = [
        coluna for coluna in features_entrada
        if coluna not in base_score.columns
    ]
    if colunas_ausentes:
        raise ValueError(
            "Colunas ausentes para aplicar o modelo: "
            + ", ".join(colunas_ausentes)
        )


    colunas_estruturais = [
        "Ano", "Idade", "Ano ingresso", "Fase_num",
        "Pedra_anterior", "Defasagem"
    ]
    base_score = base_score.dropna(subset=colunas_estruturais)

    if not base_score.empty:
        X_modelo = base_score[features_entrada].copy()
        X_proc = preprocessador.transform(X_modelo)

        scores = base_score[
            ["RA", "Nome", "Ano", "Fase_num", "Gênero", "Defasagem"]
        ].copy()
        scores["score_risco"] = modelo.predict_proba(X_proc)[:, 1]
        scores["em_risco"] = scores["score_risco"] >= threshold

        imp = pd.Series(
            modelo.feature_importances_,
            index=X_proc.columns
        )

        grupos = {}
        for nome, valor in imp.items():
            if nome.startswith("Pedra_anterior_"):
                grupo = "Pedra anterior"
            elif nome.startswith("status_historico_"):
                grupo = "Status histórico"
            else:
                grupo = nome
            grupos[grupo] = grupos.get(grupo, 0) + valor

        importancias = (
            pd.Series(grupos)
            .sort_values(ascending=False)
            .head(10)
        )

except Exception as erro:
    st.sidebar.warning(
        "Modelo de risco não pôde ser carregado. "
        "Os gráficos preditivos serão omitidos."
    )
    st.sidebar.caption(str(erro))


with left:
    fig, ax = plt.subplots(figsize=(6.5, 3.2))

    if not scores.empty:
        risco_fase = (
            scores.groupby("Fase_num")["em_risco"]
            .mean()
            .mul(100)
            .sort_index()
        )

        labels_fase = [
            "ALFA" if int(fase) == 0 else f"Fase {int(fase)}"
            for fase in risco_fase.index
        ]

        barras = ax.bar(labels_fase, risco_fase.values)

        for barra, valor in zip(barras, risco_fase.values):
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                valor + 1,
                f"{valor:.1f}%",
                ha="center",
                va="bottom",
                fontsize=7
            )

        ax.set_ylim(0, max(100, risco_fase.max() + 12))

    titulo_risco = (
        f"PERFIS SINALIZADOS EM RISCO DE PERDA DE POSIÇÃO POR FASE — {ano_risco}"
        if ano_risco is not None
        else "PERFIS SINALIZADOS EM RISCO DE PERDA DE POSIÇÃO POR FASE"
    )

    preparar_eixo(
        ax,
        titulo_risco,
        "Fase",
        "% de perfis sinalizados"
    )
    ax.tick_params(axis="x", rotation=35)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    if threshold is not None:
        st.caption(
            f"Sinalização definida por score ≥ {threshold * 100:.0f}%. "
            "A classificação representa risco estimado de perder uma ou mais posições "
            "no ano seguinte, não apenas de entrar em defasagem."
        )


with right:
    fig, ax = plt.subplots(figsize=(6.5, 3.2))

    if not importancias.empty:
        serie = importancias.sort_values()
        ax.barh(serie.index, serie.values)

    preparar_eixo(
        ax,
        "VARIÁVEIS MAIS IMPORTANTES NO RANDOM FOREST FINAL",
        "Importância preditiva",
        ""
    )
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with left:
    pedras = ["Quartzo", "Ágata", "Ametista", "Topázio"]
    tab = (
        df.groupby(["Ano", "Pedra_analitica"])["INDE_analitico"]
        .mean()
        .unstack()
        .reindex(columns=pedras)
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    for pedra in tab.columns:
        if tab[pedra].notna().any():
            ax.plot(tab.index, tab[pedra], marker="o", label=pedra)

    preparar_eixo(
        ax,
        "INDE MÉDIO POR ANO E PEDRA",
        "Ano",
        "INDE médio"
    )
    ax.legend(fontsize=7, title="Pedra", title_fontsize=7)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)


with right:
    pares = carregar_base_longitudinal()
    chaves = df[["RA", "Ano"]].drop_duplicates()
    pares = pares.merge(chaves, on=["RA", "Ano"], how="inner")

    tab = (
        pares[pares["Transicao_Pedra"].isin(["Avançou", "Manteve", "Caiu"])]
        .groupby(["Ano", "Transicao_Pedra"])
        .size()
        .unstack(fill_value=0)
    )

    if not tab.empty:
        tab_pct = tab.div(tab.sum(axis=1), axis=0) * 100
    else:
        tab_pct = tab

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    if not tab_pct.empty:
        tab_pct.plot(kind="bar", stacked=True, ax=ax, width=0.65)

    preparar_eixo(
        ax,
        "TRANSIÇÃO DE PEDRA ENTRE ANOS CONSECUTIVOS",
        "Ano de origem",
        "Proporção de alunos (%)"
    )
    ax.tick_params(axis="x", rotation=0)
    ax.legend(fontsize=7, title="Transição", title_fontsize=7)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)