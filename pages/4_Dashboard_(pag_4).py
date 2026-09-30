import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from data_prep_dashboard import carregar_base_analitica
from dashboard_utils import (
    configurar_pagina, titulo_pagina, box_perguntas,
    aplicar_filtros, kpi, preparar_eixo
)

configurar_pagina("Ponto de Virada e Visão Multidimensional")

df = aplicar_filtros(carregar_base_analitica(), "p4")

titulo_pagina(
    "PAINEL DE PONTO DE VIRADA E VISÃO MULTIDIMENSIONAL"
)

if df.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi("IPV médio", f"{df['IPV'].mean():.2f}")
with c2:
    kpi("INDE médio", f"{df['INDE_analitico'].mean():.2f}")
with c3:
    kpi("Fases", f"{df['Fase_num'].nunique()}")
with c4:
    kpi("Alunos únicos", f"{df['RA'].nunique():,}".replace(",", "."))

st.markdown("---")
left, right = st.columns(2)

with left:
    vars_ipv = ["IDA", "IEG", "IAA", "IPS", "IPP"]
    corr = (
        df[vars_ipv + ["IPV"]]
        .corr(numeric_only=True)["IPV"]
        .drop("IPV")
        .dropna()
        .sort_values(key=lambda x: x.abs())
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.barh(corr.index, corr.values)
    preparar_eixo(
        ax,
        "INDICADORES MAIS ASSOCIADOS AO IPV",
        "Correlação com IPV",
        ""
    )
    ax.axvline(0, linewidth=0.8)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with right:
    tab = (
        df.groupby(["Fase_num", "Ano"])["IPV"]
        .mean()
        .unstack()
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    for ano in tab.columns:
        ax.plot(tab.index, tab[ano], marker="o", label=str(int(ano)))
    preparar_eixo(
        ax,
        "IPV MÉDIO POR FASE E ANO",
        "Fase",
        "IPV médio"
    )
    ax.legend(title="Ano", fontsize=7, title_fontsize=7)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

base_combo = df[["IDA", "IEG", "IPS", "IPP", "INDE_analitico"]].dropna().copy()

if not base_combo.empty:
    indicadores = ["IDA", "IEG", "IPS", "IPP"]
    medianas = base_combo[indicadores].median()

    for col in indicadores:
        base_combo[f"{col}_alto"] = base_combo[col] >= medianas[col]

    base_combo["Qtd_indicadores_altos"] = base_combo[
        [f"{c}_alto" for c in indicadores]
    ].sum(axis=1)

    def nome_combo(linha):
        altos = [c for c in indicadores if linha[f"{c}_alto"]]
        return " + ".join(altos) if altos else "Nenhum ≥ mediana"

    base_combo["Combinacao"] = base_combo.apply(nome_combo, axis=1)

with left:
    tab = (
        base_combo.groupby("Qtd_indicadores_altos")["INDE_analitico"]
        .agg(["mean", "count"])
        if not base_combo.empty
        else pd.DataFrame()
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    if not tab.empty:
        ax.bar(tab.index.astype(str), tab["mean"])
    preparar_eixo(
        ax,
        "INDE POR QUANTIDADE DE INDICADORES ALTOS",
        "Qtd. de IDA/IEG/IPS/IPP ≥ mediana",
        "INDE médio"
    )
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with right:
    tab = (
        base_combo.groupby("Combinacao")["INDE_analitico"]
        .agg(["mean", "count"])
        .query("count >= 3")
        .sort_values("mean", ascending=False)
        .head(8)
        .sort_values("mean")
        if not base_combo.empty
        else pd.DataFrame()
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    if not tab.empty:
        ax.barh(tab.index, tab["mean"])
    preparar_eixo(
        ax,
        "COMBINAÇÕES DE INDICADORES COM MAIOR INDE",
        "INDE médio",
        ""
    )
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
