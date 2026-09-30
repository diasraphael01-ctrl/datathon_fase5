from pathlib import Path

import pandas as pd

from model_support import carregar_artefato_modelo


# ============================================================
# CAMINHO DO MODELO FINAL
# ============================================================

CAMINHO_MODELO = (
    Path(__file__).resolve().parent.parent
    / "modelo"
    / "random_forest_balanceado_threshold_025.joblib"
)


# ============================================================
# CARREGAR ARTEFATO UMA ÚNICA VEZ
# ============================================================

artefato = carregar_artefato_modelo(
    CAMINHO_MODELO
)

preprocessador = artefato["preprocessador"]
modelo = artefato["modelo"]
threshold = artefato["threshold"]

features_entrada = artefato["features_entrada"]


# ============================================================
# FUNÇÃO DE PREDIÇÃO
# ============================================================

def prever_risco(dados_aluno: dict):

    """
    Recebe os dados brutos de um aluno e retorna
    a estimativa produzida pelo modelo.

    A classificação positiva significa:
    risco estimado de perder uma ou mais posições
    de fase no ano seguinte.
    """

    # --------------------------------------------------------
    # Montar DataFrame
    # --------------------------------------------------------

    df_entrada = pd.DataFrame(
        [dados_aluno]
    )


    # --------------------------------------------------------
    # Validar colunas obrigatórias
    # --------------------------------------------------------

    colunas_ausentes = [
        coluna
        for coluna in features_entrada
        if coluna not in df_entrada.columns
    ]

    if colunas_ausentes:

        raise ValueError(
            "Estão faltando as seguintes features "
            f"de entrada: {colunas_ausentes}"
        )


    # --------------------------------------------------------
    # Garantir mesma ordem usada no treinamento
    # --------------------------------------------------------

    df_entrada = df_entrada[
        features_entrada
    ].copy()


    # --------------------------------------------------------
    # Pré-processamento
    # --------------------------------------------------------

    dados_processados = (
        preprocessador
        .transform(df_entrada)
    )


    # --------------------------------------------------------
    # Probabilidade da classe positiva
    # --------------------------------------------------------

    probabilidade = float(
        modelo.predict_proba(
            dados_processados
        )[0, 1]
    )


    # --------------------------------------------------------
    # Aplicação do threshold final
    # --------------------------------------------------------

    classe = int(
        probabilidade >= threshold
    )


    # --------------------------------------------------------
    # Resultado estruturado
    # --------------------------------------------------------

    resultado = {
        "probabilidade": probabilidade,
        "probabilidade_percentual": (
            probabilidade * 100
        ),
        "threshold": float(threshold),
        "threshold_percentual": (
            float(threshold) * 100
        ),
        "classe": classe,
        "risco": (
            "Risco sinalizado"
            if classe == 1
            else "Risco não sinalizado"
        )
    }

    return resultado