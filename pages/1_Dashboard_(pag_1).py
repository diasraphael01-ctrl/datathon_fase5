import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_prep_dashboard import carregar_base_analitica
from dashboard_utils import (
    configurar_pagina, titulo_pagina, box_perguntas,
    aplicar_filtros, kpi, preparar_eixo
)

configurar_pagina("Panorama de Adequação e Desempenho")

df = carregar_base_analitica()
df = aplicar_filtros(df, "p1")

titulo_pagina(
    "PAINEL DE ADEQUAÇÃO E DESEMPENHO ACADÊMICO",
)

if df.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi("Registros analisados", f"{len(df):,}".replace(",", "."))
with c2:
    kpi("Alunos únicos", f"{df['RA'].nunique():,}".replace(",", "."))
with c3:
    pct_def = (df["Defasagem"].lt(0).mean() * 100)
    kpi("Com defasagem", f"{pct_def:.1f}%")
with c4:
    kpi("IDA médio", f"{df['IDA'].mean():.2f}")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    ordem = [
        "Sem defasagem / adiantado",
        "Defasagem moderada (-1)",
        "Defasagem severa (≤ -2)"
    ]
    tab = (
        df.groupby(["Ano", "Severidade_defasagem"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=ordem, fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    tab.plot(kind="bar", stacked=True, ax=ax, width=0.65)
    preparar_eixo(
        ax,
        "PERFIL DE DEFASAGEM POR ANO",
        "Ano",
        "Quantidade de alunos"
    )
    ax.tick_params(axis="x", rotation=0)
    ax.legend(fontsize=7, title="Severidade", title_fontsize=7)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_right:
    serie = df.groupby("Ano")["IAN"].mean().dropna()

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.plot(serie.index, serie.values, marker="o", linewidth=2)
    preparar_eixo(ax, "IAN MÉDIO POR ANO", "Ano", "IAN médio")
    ax.set_xticks(serie.index)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_left:
    serie = df.groupby("Ano")["IDA"].mean().dropna()

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.plot(serie.index, serie.values, marker="o", linewidth=2)
    preparar_eixo(ax, "IDA MÉDIO POR ANO", "Ano", "IDA médio")
    ax.set_xticks(serie.index)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_right:
    tab = (
        df.groupby(["Fase_num", "Ano"])["IDA"]
        .mean()
        .unstack()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    for ano in tab.columns:
        ax.plot(tab.index, tab[ano], marker="o", label=str(int(ano)))
    preparar_eixo(
        ax,
        "IDA MÉDIO POR FASE E ANO",
        "Fase",
        "IDA médio"
    )
    ax.legend(title="Ano", fontsize=7, title_fontsize=7)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
