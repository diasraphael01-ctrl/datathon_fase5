import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

PEDRAS = ["Quartzo", "Ágata", "Ametista", "Topázio", "Sem classificação"]
FASES = list(range(10))

CSS = """
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .main-title {
        text-align: center;
        font-size: 2.0rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        color: #1f2937;
    }
    .kpi-card {
        background-color: transparent;
        padding: 5px;
        border-radius: 5px;
    }
    .kpi-title {
        font-size: 0.85rem;
        color: #6b7280;
        font-weight: 600;
        margin-bottom: 2px;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #111827;
    }
    .question-box {
        border-left: 4px solid #1d4ed8;
        padding: 0.55rem 0.8rem;
        background: #f8fafc;
        margin: 0.4rem 0 1rem 0;
        font-size: 0.9rem;
    }
    hr {
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
"""


def configurar_pagina(titulo):
    st.set_page_config(
        page_title=titulo,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(CSS, unsafe_allow_html=True)


def titulo_pagina(titulo, subtitulo=None):
    st.markdown(
        f"<h1 class='main-title'>{titulo}</h1>",
        unsafe_allow_html=True
    )
    if subtitulo:
        st.caption(subtitulo)


def box_perguntas(texto):
    st.markdown(
        f"<div class='question-box'>{texto}</div>",
        unsafe_allow_html=True
    )


def kpi(label, valor):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{label}</div>
            <div class="kpi-value">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def aplicar_filtros(df, prefixo=""):
    st.sidebar.header("🔍 Filtros de Análise")

    anos = sorted(pd.Series(df["Ano"].dropna().unique()).astype(int).tolist())
    anos_sel = st.sidebar.multiselect(
        "Ano",
        options=anos,
        default=anos,
        key=f"{prefixo}_anos"
    )

    fases = sorted(pd.Series(df["Fase_num"].dropna().unique()).astype(int).tolist())
    fases_sel = st.sidebar.multiselect(
        "Fase",
        options=fases,
        default=fases,
        key=f"{prefixo}_fases"
    )

    generos = sorted(df["Gênero"].dropna().astype(str).unique().tolist())
    generos_sel = st.sidebar.multiselect(
        "Gênero",
        options=generos,
        default=generos,
        key=f"{prefixo}_generos"
    )

    # Registros sem Pedra também fazem parte da base analítica.
    # Representamos explicitamente esses casos no filtro para que
    # a seleção padrão (todas as opções) não os exclua silenciosamente.
    pedra_filtro = df["Pedra_analitica"].astype("object").where(
        df["Pedra_analitica"].notna(),
        "Sem classificação"
    )

    valores_pedra = set(pedra_filtro.astype(str).unique())
    pedras_existentes = [
        p for p in PEDRAS
        if p in valores_pedra
    ]

    pedras_sel = st.sidebar.multiselect(
        "Pedra",
        options=pedras_existentes,
        default=pedras_existentes,
        key=f"{prefixo}_pedras"
    )

    filtro = (
        df["Ano"].isin(anos_sel)
        & df["Fase_num"].isin(fases_sel)
        & df["Gênero"].isin(generos_sel)
    )

    if pedras_existentes:
        filtro &= pedra_filtro.isin(pedras_sel)

    return df.loc[filtro].copy()


def preparar_eixo(ax, titulo, xlabel="", ylabel=""):
    ax.set_title(titulo, fontsize=10, fontweight="bold", pad=9)
    ax.set_xlabel(xlabel, fontsize=8, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=8, fontweight="bold")
    ax.tick_params(axis="both", labelsize=8)
    ax.grid(axis="y", alpha=0.2)

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(0.6)


def scatter_tendencia(ax, x, y, titulo, xlabel, ylabel):
    dados = pd.DataFrame({"x": x, "y": y}).dropna()

    ax.scatter(
        dados["x"],
        dados["y"],
        alpha=0.45,
        s=18
    )

    corr = np.nan
    if len(dados) >= 3 and dados["x"].nunique() > 1 and dados["y"].nunique() > 1:
        corr = dados["x"].corr(dados["y"])
        z = np.polyfit(dados["x"], dados["y"], 1)
        xx = np.linspace(dados["x"].min(), dados["x"].max(), 100)
        ax.plot(xx, z[0] * xx + z[1], linewidth=1.5)

    preparar_eixo(ax, titulo, xlabel, ylabel)

    if pd.notna(corr):
        ax.text(
            0.02, 0.96,
            f"Correlação: {corr:.2f}",
            transform=ax.transAxes,
            va="top",
            fontsize=8,
            fontweight="bold"
        )

    return corr
