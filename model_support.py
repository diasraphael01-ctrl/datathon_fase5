# ============================================================
# model_support.py
# Suporte para carregamento do artefato de Machine Learning
# ============================================================

import sys

import joblib
import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.validation import check_is_fitted


# ============================================================
# TRANSFORMERS PERSONALIZADOS
# ============================================================

class CreateTempoPrograma(
    BaseEstimator,
    TransformerMixin
):

    def fit(
        self,
        df,
        y=None
    ):
        return self


    def transform(
        self,
        df
    ):

        df = df.copy()

        df["Tempo_programa"] = (
            df["Ano"]
            - df["Ano ingresso"]
        )

        return df


# ============================================================

class CreateStatusHistorico(
    BaseEstimator,
    TransformerMixin
):

    def fit(
        self,
        df,
        y=None
    ):
        return self


    def transform(
        self,
        df
    ):

        df = df.copy()

        df["status_historico"] = np.where(
            df["Ano ingresso"] == df["Ano"],
            "Novo aluno",
            np.where(
                df["Pedra_anterior"]
                != "Sem histórico",

                "Com histórico",

                "Sem histórico"
            )
        )

        return df


# ============================================================

class DropFeatures(
    BaseEstimator,
    TransformerMixin
):

    def __init__(
        self,
        feature_to_drop=None
    ):

        if feature_to_drop is None:

            feature_to_drop = [
                "RA",
                "Nome",
                "Ano",
                "Ano ingresso",
                "Gênero"
            ]

        self.feature_to_drop = (
            feature_to_drop
        )


    def fit(
        self,
        df,
        y=None
    ):
        return self


    def transform(
        self,
        df
    ):

        df = df.copy()

        return df.drop(
            columns=self.feature_to_drop,
            errors="ignore"
        )


# ============================================================

class FillMissingWithMedian(
    BaseEstimator,
    TransformerMixin
):

    def __init__(
        self,
        colunas=None
    ):

        if colunas is None:

            colunas = [
                "Nº Av",
                "IAA",
                "IDA",
                "IEG",
                "IPP",
                "IPS",
                "IPV",
                "INDE_atual"
            ]

        self.colunas = colunas


    def fit(
        self,
        df,
        y=None
    ):

        self.medianas_ = (
            df[self.colunas]
            .median()
        )

        return self


    def transform(
        self,
        df
    ):

        df = df.copy()

        df[self.colunas] = (
            df[self.colunas]
            .fillna(
                self.medianas_
            )
        )

        return df


# ============================================================

class StandardScalerFeatures(
    BaseEstimator,
    TransformerMixin
):

    def __init__(
        self,
        colunas_escala=None
    ):

        if colunas_escala is None:

            colunas_escala = [
                "Idade",
                "Fase_num",
                "Nº Av",
                "IAA",
                "IDA",
                "IEG",
                "IPP",
                "IPS",
                "IPV",
                "Defasagem",
                "INDE_atual",
                "Tempo_programa"
            ]

        self.colunas_escala = (
            colunas_escala
        )

        self.scaler = (
            StandardScaler()
        )


    def fit(
        self,
        df,
        y=None
    ):

        self.scaler.fit(
            df[
                self.colunas_escala
            ]
        )

        return self


    def transform(
        self,
        df
    ):

        df = df.copy()

        df[
            self.colunas_escala
        ] = self.scaler.transform(
            df[
                self.colunas_escala
            ]
        )

        return df


# ============================================================

class OneHotEncodingNames(
    BaseEstimator,
    TransformerMixin
):

    def __init__(
        self,
        OneHotEncoding=None
    ):

        if OneHotEncoding is None:

            OneHotEncoding = [
                "Pedra_anterior",
                "status_historico"
            ]

        self.OneHotEncoding = (
            OneHotEncoding
        )

        self.encoder = (
            OneHotEncoder(
                sparse_output=False,
                handle_unknown="ignore"
            )
        )


    def fit(
        self,
        df,
        y=None
    ):

        self.encoder.fit(
            df[
                self.OneHotEncoding
            ]
        )

        self.is_fitted_ = True

        return self


    def transform(
        self,
        df
    ):

        check_is_fitted(
            self,
            "is_fitted_"
        )

        df = df.copy()

        encoded = (
            self.encoder
            .transform(
                df[
                    self.OneHotEncoding
                ]
            )
        )

        nomes = (
            self.encoder
            .get_feature_names_out(
                self.OneHotEncoding
            )
        )

        encoded = pd.DataFrame(
            encoded,
            columns=nomes,
            index=df.index
        )

        df = df.drop(
            columns=self.OneHotEncoding
        )

        df = pd.concat(
            [
                df,
                encoded
            ],
            axis=1
        )

        return df


# ============================================================
# REGISTRO DAS CLASSES NO __main__
# ============================================================

def registrar_classes_joblib():

    """
    O artefato foi originalmente serializado no notebook,
    portanto o pickle procura os transformers em:

        __main__.CreateTempoPrograma
        __main__.CreateStatusHistorico
        ...

    No Streamlit multipágina, o objeto associado a __main__
    pode mudar durante a execução.

    Por isso buscamos sys.modules["__main__"] no instante
    imediatamente anterior ao joblib.load().
    """

    main_module = (
        sys.modules.get(
            "__main__"
        )
    )


    if main_module is None:

        raise RuntimeError(
            "Não foi possível localizar "
            "o módulo __main__."
        )


    classes_customizadas = [
        CreateTempoPrograma,
        CreateStatusHistorico,
        DropFeatures,
        FillMissingWithMedian,
        StandardScalerFeatures,
        OneHotEncodingNames
    ]


    for classe in classes_customizadas:

        setattr(
            main_module,
            classe.__name__,
            classe
        )


# ============================================================
# CARREGAMENTO DO ARTEFATO
# ============================================================

def carregar_artefato_modelo(
    caminho
):

    # --------------------------------------------------------
    # 1. Registrar classes no __main__ atual
    # --------------------------------------------------------

    registrar_classes_joblib()


    # --------------------------------------------------------
    # 2. Validação preventiva
    # --------------------------------------------------------

    main_module = (
        sys.modules["__main__"]
    )


    classes_necessarias = [
        "CreateTempoPrograma",
        "CreateStatusHistorico",
        "DropFeatures",
        "FillMissingWithMedian",
        "StandardScalerFeatures",
        "OneHotEncodingNames"
    ]


    classes_ausentes = [
        nome
        for nome in classes_necessarias
        if not hasattr(
            main_module,
            nome
        )
    ]


    if classes_ausentes:

        raise RuntimeError(
            "Falha ao registrar as classes "
            "necessárias ao artefato: "
            + ", ".join(
                classes_ausentes
            )
        )


    # --------------------------------------------------------
    # 3. Carregar modelo
    # --------------------------------------------------------

    return joblib.load(
        caminho
    )