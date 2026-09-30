import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_prep_dashboard import carregar_base_analitica
from dashboard_utils import (
    configurar_pagina, titulo_pagina, box_perguntas,
    aplicar_filtros, kpi, preparar_eixo
)

configurar_pagina("Engajamento e Autopercepção")

df = aplicar_filtros(carregar_base_analitica(), "p2")

titulo_pagina(
    "PAINEL DE ENGAJAMENTO E AUTOPERCEPÇÃO"
)

if df.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi("IEG médio", f"{df['IEG'].mean():.2f}")
with c2:
    kpi("IAA médio", f"{df['IAA'].mean():.2f}")
with c3:
    kpi("IDA médio", f"{df['IDA'].mean():.2f}")
with c4:
    kpi("IPV médio", f"{df['IPV'].mean():.2f}")


def adicionar_rotulos_barras(ax, casas=2, sufixo=""):
    for barra in ax.patches:
        altura = barra.get_height()
        if pd.notna(altura):
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                altura + (0.12 if sufixo != "%" else 1.0),
                f"{altura:.{casas}f}{sufixo}",
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold"
            )


def quartis_por_ano(base, coluna):
    """
    Divide a variável em quatro faixas relativas dentro de cada ano.
    O uso do rank evita erro quando existem valores repetidos no quartil.
    """
    saida = pd.Series(index=base.index, dtype="object")
    rotulos = [
        "Q1 — 25% inferior",
        "Q2",
        "Q3",
        "Q4 — 25% superior"
    ]

    for _, grupo in base.groupby("Ano"):
        valores = pd.to_numeric(grupo[coluna], errors="coerce").dropna()
        if valores.empty:
            continue

        if len(valores) < 4:
            saida.loc[valores.index] = "Faixa única"
            continue

        ranking = valores.rank(method="first")
        saida.loc[valores.index] = pd.qcut(
            ranking,
            q=4,
            labels=rotulos
        ).astype(str)

    return saida


def tabela_media_por_quartil(base, coluna_resultado):
    temp = base[["Ano", "IEG", coluna_resultado]].copy()
    temp["Faixa_IEG"] = quartis_por_ano(temp, "IEG")
    temp = temp.dropna(subset=["Faixa_IEG", coluna_resultado])

    ordem = [
        "Q1 — 25% inferior",
        "Q2",
        "Q3",
        "Q4 — 25% superior",
        "Faixa única"
    ]

    tab = (
        temp.groupby("Faixa_IEG")[coluna_resultado]
        .agg(["mean", "count"])
        .reindex(ordem)
        .dropna(how="all")
    )
    return tab


def perfis_iaa(base, coluna_resultado, nome_resultado):
    registros = []

    for _, grupo in base.groupby("Ano"):
        temp = grupo[["IAA", coluna_resultado]].dropna().copy()
        if temp.empty:
            continue

        med_iaa = temp["IAA"].median()
        med_resultado = temp[coluna_resultado].median()

        iaa_alta = temp["IAA"] >= med_iaa
        resultado_alto = temp[coluna_resultado] >= med_resultado

        temp["Perfil"] = "Sinais alinhados"
        temp.loc[
            iaa_alta & ~resultado_alto,
            "Perfil"
        ] = f"IAA alta / {nome_resultado} baixo"
        temp.loc[
            ~iaa_alta & resultado_alto,
            "Perfil"
        ] = f"IAA baixa / {nome_resultado} alto"

        registros.append(temp[["Perfil"]])

    if not registros:
        return pd.Series(dtype=float)

    perfis = pd.concat(registros, ignore_index=True)["Perfil"]
    ordem = [
        "Sinais alinhados",
        f"IAA alta / {nome_resultado} baixo",
        f"IAA baixa / {nome_resultado} alto"
    ]

    return (
        perfis.value_counts(normalize=True)
        .mul(100)
        .reindex(ordem)
        .fillna(0)
    )


st.markdown("---")
left, right = st.columns(2)

with left:
    tab = tabela_media_por_quartil(df, "IDA")
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.bar(tab.index.astype(str), tab["mean"])
    preparar_eixo(
        ax,
        "IDA MÉDIO POR FAIXA DE ENGAJAMENTO (IEG)",
        "Faixa relativa de IEG",
        "IDA médio"
    )
    ax.set_ylim(0, 10.5)
    ax.tick_params(axis="x", rotation=12)
    adicionar_rotulos_barras(ax)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with right:
    tab = tabela_media_por_quartil(df, "IPV")
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.bar(tab.index.astype(str), tab["mean"])
    preparar_eixo(
        ax,
        "IPV MÉDIO POR FAIXA DE ENGAJAMENTO (IEG)",
        "Faixa relativa de IEG",
        "IPV médio"
    )
    ax.set_ylim(0, 10.5)
    ax.tick_params(axis="x", rotation=12)
    adicionar_rotulos_barras(ax)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with left:
    percentuais = perfis_iaa(df, "IDA", "IDA")
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.bar(percentuais.index.astype(str), percentuais.values)
    preparar_eixo(
        ax,
        "PERFIS DE ALINHAMENTO — IAA × IDA",
        "Perfil",
        "Proporção dos registros (%)"
    )
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=12)
    adicionar_rotulos_barras(ax, casas=1, sufixo="%")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)


with right:
    percentuais = perfis_iaa(df, "IEG", "IEG")
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.bar(percentuais.index.astype(str), percentuais.values)
    preparar_eixo(
        ax,
        "PERFIS DE ALINHAMENTO — IAA × IEG",
        "Perfil",
        "Proporção dos registros (%)"
    )
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=12)
    adicionar_rotulos_barras(ax, casas=1, sufixo="%")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

