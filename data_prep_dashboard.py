from pathlib import Path
import numpy as np
import pandas as pd

ARQUIVO_XLSX = Path("data/BASE DE DADOS PEDE 2024 - DATATHON.xlsx")
CSV_ANALITICO = Path("data/base_analitica_dashboard.csv")
CSV_LONGITUDINAL = Path("data/base_longitudinal_dashboard.csv")


def _corrigir_idade_2023(valor):
    try:
        return valor.day
    except Exception:
        return valor


def _fase_num_2023(valor):
    if pd.isna(valor):
        return np.nan
    if str(valor).strip().upper() == "ALFA":
        return 0
    return int(str(valor).upper().replace("FASE ", "").strip())


def _fase_num_2024(valor):
    if pd.isna(valor):
        return np.nan
    texto = str(valor).strip().upper()
    if texto == "ALFA":
        return 0
    # mesma estratégia adotada no notebook: primeiro algarismo
    for ch in texto:
        if ch.isdigit():
            return int(ch)
    return np.nan


def _classificar_pedra_por_inde(inde):
    if pd.isna(inde):
        return pd.NA
    valor = round(float(inde), 1)
    if valor <= 6.0:
        return "Quartzo"
    if valor <= 7.1:
        return "Ágata"
    if valor <= 8.1:
        return "Ametista"
    return "Topázio"


def _classificar_defasagem(valor):
    if pd.isna(valor):
        return pd.NA
    if valor >= 0:
        return "Sem defasagem / adiantado"
    if valor == -1:
        return "Defasagem moderada (-1)"
    return "Defasagem severa (≤ -2)"


def preparar_base_analitica(caminho_xlsx=ARQUIVO_XLSX):
    """
    Reconstrói a base analítica a partir das três abas do arquivo oficial.

    Esta base NÃO é o df_longitudinal do modelo.
    Ela preserva 2022, 2023 e 2024 e mantém IAN, Pedra_atual e demais
    indicadores necessários aos dashboards.
    """
    caminho_xlsx = Path(caminho_xlsx)

    df_2022 = pd.read_excel(caminho_xlsx, sheet_name="PEDE2022").copy()
    df_2023 = pd.read_excel(caminho_xlsx, sheet_name="PEDE2023").copy()
    df_2024 = pd.read_excel(caminho_xlsx, sheet_name="PEDE2024").copy()

    # ---------------------------------------------------------
    # 1) Padronização de nomes
    # ---------------------------------------------------------
    df_2022.rename(columns={
        "Idade 22": "Idade",
        "Matem": "Mat",
        "Portug": "Por",
        "Inglês": "Ing",
        "Fase ideal": "Fase Ideal",
        "Defas": "Defasagem"
    }, inplace=True)

    df_2023.rename(columns={
        "Nome Anonimizado": "Nome",
        "Data de Nasc": "Ano nasc"
    }, inplace=True)

    df_2024.rename(columns={
        "Nome Anonimizado": "Nome",
        "Data de Nasc": "Ano nasc"
    }, inplace=True)

    # ---------------------------------------------------------
    # 2) INDE e Pedra correntes
    # ---------------------------------------------------------
    df_2022["INDE_atual"] = df_2022["INDE 22"]
    df_2022["Pedra_atual"] = df_2022["Pedra 22"]

    df_2023["INDE_atual"] = df_2023["INDE 23"]
    df_2023["Pedra_atual"] = df_2023["Pedra 23"]

    df_2024["INDE_atual"] = df_2024["INDE 2024"]
    df_2024["Pedra_atual"] = df_2024["Pedra 2024"]

    # ---------------------------------------------------------
    # 3) Padronização estrutural
    # ---------------------------------------------------------
    df_2023["Ano nasc"] = pd.to_datetime(
        df_2023["Ano nasc"], format="mixed", errors="coerce"
    ).dt.year

    df_2024["Ano nasc"] = pd.to_datetime(
        df_2024["Ano nasc"], errors="coerce"
    ).dt.year

    df_2022["Gênero"] = df_2022["Gênero"].map({
        "Menina": "Feminino",
        "Menino": "Masculino"
    }).fillna(df_2022["Gênero"])

    df_2023["Idade"] = (
        df_2023["Idade"]
        .apply(_corrigir_idade_2023)
        .pipe(pd.to_numeric, errors="coerce")
    )

    # ---------------------------------------------------------
    # 4) Reconstrução de IPP de 2022 para Fases 0 a 7
    # ---------------------------------------------------------
    if "IPP" not in df_2022.columns:
        df_2022["IPP"] = np.nan

    fase_2022_num = pd.to_numeric(df_2022["Fase"], errors="coerce")
    mascara_ipp = fase_2022_num < 8

    df_2022.loc[mascara_ipp, "IPP"] = (
        df_2022.loc[mascara_ipp, "INDE 22"]
        - (
            df_2022.loc[mascara_ipp, "IAN"] * 0.1
            + df_2022.loc[mascara_ipp, "IDA"] * 0.2
            + df_2022.loc[mascara_ipp, "IEG"] * 0.2
            + df_2022.loc[mascara_ipp, "IAA"] * 0.1
            + df_2022.loc[mascara_ipp, "IPS"] * 0.1
            + df_2022.loc[mascara_ipp, "IPV"] * 0.2
        )
    ) / 0.1

    # ---------------------------------------------------------
    # 5) Fase numérica e Ano
    # ---------------------------------------------------------
    df_2022["Fase_num"] = pd.to_numeric(df_2022["Fase"], errors="coerce")
    df_2023["Fase_num"] = df_2023["Fase"].apply(_fase_num_2023)
    df_2024["Fase_num"] = df_2024["Fase"].apply(_fase_num_2024)

    df_2022["Ano"] = 2022
    df_2023["Ano"] = 2023
    df_2024["Ano"] = 2024

    # ---------------------------------------------------------
    # 6) Consolidação
    # ---------------------------------------------------------
    df = pd.concat(
        [df_2022, df_2023, df_2024],
        ignore_index=True,
        sort=False
    )

    df.drop(
        columns=["Destaque IPV.1", "Ativo/ Inativo.1"],
        inplace=True,
        errors="ignore"
    )

    # "INCLUIR" -> ausente
    if "INDE 2024" in df.columns:
        df["INDE 2024"] = pd.to_numeric(df["INDE 2024"], errors="coerce")

    df["INDE_atual"] = pd.to_numeric(df["INDE_atual"], errors="coerce")

    for col in ["Pedra 2024", "Pedra_atual"]:
        if col in df.columns:
            df[col] = df[col].replace("INCLUIR", pd.NA)

    # padronização Ágata
    for col in [
        "Pedra 20", "Pedra 21", "Pedra 22",
        "Pedra 23", "Pedra 2023", "Pedra 2024",
        "Pedra_atual"
    ]:
        if col in df.columns:
            df[col] = df[col].replace("Agata", "Ágata")

    if "Nº Av" in df.columns:
        df["Nº Av"] = pd.to_numeric(df["Nº Av"], errors="coerce").astype("Int64")

    # ---------------------------------------------------------
    # 7) INDE calculado conforme regra do notebook
    # ---------------------------------------------------------
    df["INDE_calculado"] = np.nan

    mask_0_7 = df["Fase_num"].between(0, 7)
    df.loc[mask_0_7, "INDE_calculado"] = (
        df.loc[mask_0_7, "IAN"] * 0.1
        + df.loc[mask_0_7, "IDA"] * 0.2
        + df.loc[mask_0_7, "IEG"] * 0.2
        + df.loc[mask_0_7, "IAA"] * 0.1
        + df.loc[mask_0_7, "IPS"] * 0.1
        + df.loc[mask_0_7, "IPP"] * 0.1
        + df.loc[mask_0_7, "IPV"] * 0.2
    )

    # O notebook trata especificamente Fase 8 nesta regra.
    mask_8 = df["Fase_num"] == 8
    df.loc[mask_8, "INDE_calculado"] = (
        df.loc[mask_8, "IAN"] * 0.1
        + df.loc[mask_8, "IDA"] * 0.4
        + df.loc[mask_8, "IEG"] * 0.2
        + df.loc[mask_8, "IAA"] * 0.1
        + df.loc[mask_8, "IPS"] * 0.2
    )

    # Base de dashboard: preserva o valor oficial quando existe.
    # Só usa o calculado para completar ausência quando a fórmula é computável.
    df["INDE_analitico"] = df["INDE_atual"].combine_first(df["INDE_calculado"])
    df["fonte_INDE"] = np.where(
        df["INDE_atual"].notna(),
        "Original",
        np.where(df["INDE_calculado"].notna(), "Reconstruído", "Ausente")
    )

    pedra_calculada = df["INDE_analitico"].apply(_classificar_pedra_por_inde)
    df["Pedra_analitica"] = df["Pedra_atual"].combine_first(pedra_calculada)

    # ---------------------------------------------------------
    # 8) Features analíticas úteis
    # ---------------------------------------------------------
    df["Tempo_programa"] = df["Ano"] - pd.to_numeric(
        df["Ano ingresso"], errors="coerce"
    )
    df["Severidade_defasagem"] = df["Defasagem"].apply(_classificar_defasagem)

    # Pedra anterior:
    # 2022 usa Pedra 21; 2023/2024 usam Pedra_analitica do ano anterior.
    df = df.sort_values(["RA", "Ano"]).copy()
    df["Pedra_anterior"] = "Sem histórico"

    mask_2022 = df["Ano"] == 2022
    if "Pedra 21" in df.columns:
        df.loc[mask_2022, "Pedra_anterior"] = (
            df.loc[mask_2022, "Pedra 21"].fillna("Sem histórico")
        )

    pedras_prev = df[["RA", "Ano", "Pedra_analitica"]].copy()
    pedras_prev["Ano"] = pedras_prev["Ano"] + 1
    pedras_prev.rename(
        columns={"Pedra_analitica": "_Pedra_anterior_merge"},
        inplace=True
    )

    df = df.merge(
        pedras_prev,
        on=["RA", "Ano"],
        how="left"
    )

    mask_pos_2022 = df["Ano"] > 2022
    df.loc[mask_pos_2022, "Pedra_anterior"] = (
        df.loc[mask_pos_2022, "_Pedra_anterior_merge"]
    )
    df["Pedra_anterior"] = df["Pedra_anterior"].fillna("Sem histórico")
    df.drop(columns=["_Pedra_anterior_merge"], inplace=True)

    return df.sort_values(["Ano", "RA"]).reset_index(drop=True)


def criar_base_longitudinal_analitica(df_analitico):
    """
    Cria pares de anos consecutivos do mesmo aluno.
    Usada para perguntas sobre antecedência, evolução e transição.
    """
    atual = df_analitico.sort_values(["RA", "Ano"]).copy()

    proximos = atual[
        [
            "RA", "Ano", "IDA", "IEG", "IPS", "IPP", "IPV",
            "INDE_analitico", "Defasagem", "Pedra_analitica", "Fase_num"
        ]
    ].copy()

    proximos["Ano"] = proximos["Ano"] - 1
    proximos.rename(columns={
        "IDA": "IDA_prox",
        "IEG": "IEG_prox",
        "IPS": "IPS_prox",
        "IPP": "IPP_prox",
        "IPV": "IPV_prox",
        "INDE_analitico": "INDE_prox",
        "Defasagem": "Defasagem_prox",
        "Pedra_analitica": "Pedra_prox",
        "Fase_num": "Fase_prox"
    }, inplace=True)

    pares = atual.merge(
        proximos,
        on=["RA", "Ano"],
        how="inner"
    )

    pares["delta_IDA"] = pares["IDA_prox"] - pares["IDA"]
    pares["delta_IEG"] = pares["IEG_prox"] - pares["IEG"]
    pares["delta_IPV"] = pares["IPV_prox"] - pares["IPV"]
    pares["delta_INDE"] = pares["INDE_prox"] - pares["INDE_analitico"]
    pares["delta_defasagem"] = pares["Defasagem_prox"] - pares["Defasagem"]

    ordem_pedra = {
        "Quartzo": 1,
        "Ágata": 2,
        "Ametista": 3,
        "Topázio": 4
    }
    atual_rank = pares["Pedra_analitica"].map(ordem_pedra)
    prox_rank = pares["Pedra_prox"].map(ordem_pedra)
    delta_pedra = prox_rank - atual_rank

    pares["Transicao_Pedra"] = np.select(
        [delta_pedra > 0, delta_pedra == 0, delta_pedra < 0],
        ["Avançou", "Manteve", "Caiu"],
        default="Sem classificação"
    )

    return pares.reset_index(drop=True)


def gerar_arquivos_dashboard(
    caminho_xlsx=ARQUIVO_XLSX,
    csv_analitico=CSV_ANALITICO,
    csv_longitudinal=CSV_LONGITUDINAL
):
    df = preparar_base_analitica(caminho_xlsx)
    pares = criar_base_longitudinal_analitica(df)

    Path(csv_analitico).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_analitico, index=False)
    pares.to_csv(csv_longitudinal, index=False)

    return df, pares


def carregar_base_analitica():
    if CSV_ANALITICO.exists():
        return pd.read_csv(CSV_ANALITICO)
    return preparar_base_analitica(ARQUIVO_XLSX)


def carregar_base_longitudinal():
    if CSV_LONGITUDINAL.exists():
        return pd.read_csv(CSV_LONGITUDINAL)

    df = carregar_base_analitica()
    return criar_base_longitudinal_analitica(df)


if __name__ == "__main__":
    df, pares = gerar_arquivos_dashboard()
    print("Base analítica:", df.shape)
    print("Base longitudinal:", pares.shape)
    print(f"Salvo em: {CSV_ANALITICO}")
    print(f"Salvo em: {CSV_LONGITUDINAL}")
