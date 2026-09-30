import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from data_prep_dashboard import carregar_base_analitica, carregar_base_longitudinal
from dashboard_utils import (
    configurar_pagina, titulo_pagina, box_perguntas,
    aplicar_filtros, kpi, preparar_eixo
)

configurar_pagina("Desenvolvimento Psicossocial e Psicopedagógico")

df_full = carregar_base_analitica()
df = aplicar_filtros(df_full, "p3")

pares_full = carregar_base_longitudinal()
chaves = df[["RA", "Ano"]].drop_duplicates()
pares = pares_full.merge(chaves, on=["RA", "Ano"], how="inner")

titulo_pagina(
    "PAINEL DE DESENVOLVIMENTO PSICOSSOCIAL E PSICOPEDAGÓGICO"
)

if df.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi("IPS médio", f"{df['IPS'].mean():.2f}")
with c2:
    kpi("IPP médio", f"{df['IPP'].mean():.2f}")
with c3:
    kpi("Pares longitudinais", f"{len(pares):,}".replace(",", "."))
with c4:
    kpi("Defasagem média", f"{df['Defasagem'].mean():.2f}")

def faixa_ips(s):
    return pd.cut(
        s,
        bins=[-np.inf, 6, 8, np.inf],
        labels=["Baixo (<6)", "Médio (6–<8)", "Alto (≥8)"],
        right=False
    )

pares = pares.copy()
pares["Faixa_IPS"] = faixa_ips(pares["IPS"])

st.markdown("---")
left, right = st.columns(2)

with left:
    tab = pares.groupby("Faixa_IPS", observed=False)["delta_IDA"].agg(["mean", "count"])
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.bar(tab.index.astype(str), tab["mean"])
    preparar_eixo(
        ax,
        "VARIAÇÃO DO IDA NO ANO SEGUINTE POR IPS ATUAL",
        "Faixa do IPS atual",
        "Δ IDA (ano seguinte - atual)"
    )
    ax.axhline(0, linewidth=0.8)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with right:
    tab = pares.groupby("Faixa_IPS", observed=False)["delta_IEG"].agg(["mean", "count"])
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.bar(tab.index.astype(str), tab["mean"])
    preparar_eixo(
        ax,
        "VARIAÇÃO DO IEG NO ANO SEGUINTE POR IPS ATUAL",
        "Faixa do IPS atual",
        "Δ IEG (ano seguinte - atual)"
    )
    ax.axhline(0, linewidth=0.8)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with left:
    ordem = [
        "Sem defasagem / adiantado",
        "Defasagem moderada (-1)",
        "Defasagem severa (≤ -2)"
    ]
    tab = (
        df.groupby("Severidade_defasagem")["IPP"]
        .agg(["mean", "count"])
        .reindex(ordem)
        .dropna(how="all")
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    ax.bar(tab.index.astype(str), tab["mean"])
    preparar_eixo(
        ax,
        "IPP MÉDIO POR SEVERIDADE DE DEFASAGEM",
        "",
        "IPP médio"
    )
    ax.tick_params(axis="x", rotation=12)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with right:
    tab = (
        df[["IAN", "IPP"]]
        .dropna()
        .groupby("IAN")["IPP"]
        .agg(["mean", "count"])
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    rotulos = [f"IAN {valor:g}".replace(".", ",") for valor in tab.index]
    ax.bar(rotulos, tab["mean"])
    preparar_eixo(
        ax,
        "IPP MÉDIO POR NÍVEL DE IAN",
        "IAN — Adequação ao nível",
        "IPP médio"
    )
    ax.set_ylim(0, 10.5)

    for barra in ax.patches:
        altura = barra.get_height()
        if pd.notna(altura):
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                altura + 0.12,
                f"{altura:.2f}",
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold"
            )

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
