from datetime import datetime
import streamlit as st
from src.inferencia import prever_risco

st.set_page_config(
    page_title="Avaliador de Risco de Perda de Posição",
    layout="centered"
)

def calcular_inde(
    fase_num,
    ian,
    ida,
    ieg,
    iaa,
    ips,
    ipp=None,
    ipv=None
):
    """
    Calcula o INDE conforme a fase informada.

    Fases 0 a 7:
        IAN*0.1
        + IDA*0.2
        + IEG*0.2
        + IAA*0.1
        + IPS*0.1
        + IPP*0.1
        + IPV*0.2

    Fases 8 ou superiores:
        IAN*0.1
        + IDA*0.4
        + IEG*0.2
        + IAA*0.1
        + IPS*0.2
    """

    if fase_num >= 8:

        return (
            ian * 0.1
            + ida * 0.4
            + ieg * 0.2
            + iaa * 0.1
            + ips * 0.2
        )

    return (
        ian * 0.1
        + ida * 0.2
        + ieg * 0.2
        + iaa * 0.1
        + ips * 0.1
        + ipp * 0.1
        + ipv * 0.2
    )

ANO_ATUAL = datetime.now().year

st.markdown(
    """
    <h1 style="
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        line-height: 1.4;
        margin-top: 0px;
        padding-top: 5px;
    ">
        AVALIADOR DE RISCO DE DEFASAGEM DE FASE DO ALUNO
    </h1>
    """,
    unsafe_allow_html=True
)


st.warning(
    "Preencha os dados do aluno no formulário abaixo "
    "e clique no botão **ENVIAR** no final da página."
)

st.write("#### DADOS DO ALUNO")


input_ano = st.number_input(
    "**Ano de referência dos indicadores**",
    value=ANO_ATUAL,
    step=1,
    disabled=True
)


st.caption(
    "O ano de referência é definido automaticamente "
    "com base no ano atual do sistema."
)


input_ano_ingresso = st.number_input(
    "**É aluno da Passos Mágicos desde de que ano? (ano de ingresso)**",
    min_value=2010,
    max_value=ANO_ATUAL,
    value=None,
    step=1,
    placeholder="Informe o ano de ingresso"
)


input_idade = st.number_input(
    "**Idade**",
    min_value=7,
    max_value=27,
    value=None,
    step=1,
    placeholder="Informe a idade do aluno"
)

dict_fase = {
    "ALFA": 0,
    "Fase 1": 1,
    "Fase 2": 2,
    "Fase 3": 3,
    "Fase 4": 4,
    "Fase 5": 5,
    "Fase 6": 6,
    "Fase 7": 7,
    "Fase 8": 8,
    "Fase 9": 9
}


input_fase_texto = st.radio(
    "**Fase atual**",
    options=list(dict_fase.keys()),
    index=None,
    horizontal=True
)


input_fase = (
    dict_fase[input_fase_texto]
    if input_fase_texto is not None
    else None
)

input_num_av = st.number_input(
    "**Número de avaliações realizadas (Nº Av)**",
    min_value=0,
    max_value=6,
    value=None,
    step=1,
    placeholder="Informe a quantidade de avaliações"
)

input_defasagem = st.number_input(
    "**Qual é o nível de defasagem atual do aluno?** (-1 = uma fase atrasado; 0 = está na fase ideal; 1 = uma fase adiantado)",
    value=None,
    step=1,
    placeholder=(
        "Informe o nível de defasagem do aluno"
    )
)

st.write("#### HISTÓRICO DO ALUNO")


if (
    input_ano_ingresso is not None
    and int(input_ano) == int(input_ano_ingresso)
):

    input_pedra_anterior = "Sem histórico"

    st.info(
        "Como o aluno ingressou no próprio ano de referência, "
        "a Pedra anterior será definida automaticamente como "
        "**Sem histórico**."
    )

else:

    opcoes_pedra = [
        "Sem histórico",
        "Quartzo",
        "Ágata",
        "Ametista",
        "Topázio"
    ]

    input_pedra_anterior = st.selectbox(
        "**No ano passado, qual pedra o aluno terminou o ano?** (Informe a pedra do ano passado)",
        options=opcoes_pedra,
        index=None,
        placeholder=(
            "Selecione a Pedra ou informe "
            "que não há histórico..."
        )
    )

st.write("#### INDICADORES EDUCACIONAIS")


st.caption(
    "Informe os valores mais recentes dos indicadores "
    "de avaliação e conselho do aluno."
)


input_ian = st.number_input(
    "**IAN — Indicador de Adequação ao Nível**",
    min_value=2.5,
    max_value=10.0,
    value=None,
    step=0.01,
    format="%.3f",
    placeholder="Informe o IAN"
)

input_ida = st.number_input(
    "**IDA — Indicador de Desempenho Acadêmico**",
    min_value=0.0,
    max_value=10.0,
    value=None,
    step=0.01,
    format="%.3f",
    placeholder="Informe o IDA"
)

input_ieg = st.number_input(
    "**IEG — Indicador de Engajamento**",
    min_value=0.0,
    max_value=10.0,
    value=None,
    step=0.01,
    format="%.3f",
    placeholder="Informe o IEG"
)

input_iaa = st.number_input(
    "**IAA — Indicador de Autoavaliação**",
    min_value=0.0,
    max_value=10.01,
    value=None,
    step=0.01,
    format="%.3f",
    placeholder="Informe o IAA"
)

input_ips = st.number_input(
    "**IPS — Indicador Psicossocial**",
    min_value=2.5,
    max_value=10.0,
    value=None,
    step=0.01,
    format="%.3f",
    placeholder="Informe o IPS"
)

if (
    input_fase is not None
    and input_fase < 8
):

    input_ipp = st.number_input(
        "**IPP — Indicador Psicopedagógico**",
        min_value=-0.10,
        max_value=10.0,
        value=None,
        step=0.01,
        format="%.3f",
        placeholder="Informe o IPP"
    )


    input_ipv = st.number_input(
        "**IPV — Indicador de Ponto de Virada**",
        min_value=2.5,
        max_value=10.01,
        value=None,
        step=0.01,
        format="%.3f",
        placeholder="Informe o IPV"
    )


elif (
    input_fase is not None
    and input_fase >= 8
):

    input_ipp = None
    input_ipv = None

    st.info(
        "Para alunos da **Fase 8 ou superior**, o INDE é calculado "
        "sem os indicadores IPP e IPV. Por isso, esses campos não "
        "precisam ser informados."
    )


else:

    input_ipp = None
    input_ipv = None

inde_atual = None


indicadores_base_preenchidos = all(
    valor is not None
    for valor in [
        input_fase,
        input_ian,
        input_ida,
        input_ieg,
        input_iaa,
        input_ips
    ]
)


if indicadores_base_preenchidos:

    if input_fase >= 8:

        inde_atual = calcular_inde(
            fase_num=input_fase,
            ian=input_ian,
            ida=input_ida,
            ieg=input_ieg,
            iaa=input_iaa,
            ips=input_ips
        )

    elif (
        input_ipp is not None
        and input_ipv is not None
    ):

        inde_atual = calcular_inde(
            fase_num=input_fase,
            ian=input_ian,
            ida=input_ida,
            ieg=input_ieg,
            iaa=input_iaa,
            ips=input_ips,
            ipp=input_ipp,
            ipv=input_ipv
        )


if inde_atual is not None:

    st.success(
        f"**INDE atual calculado automaticamente: "
        f"{inde_atual:.4f}**"
    )

else:

    st.caption(
        "O **INDE atual** será calculado automaticamente "
        "quando todos os indicadores necessários forem preenchidos."
    )

if st.button(
    "ENVIAR",
    type="primary",
    use_container_width=True
):

    campos = {
        "Ano de referência": input_ano,
        "Ano de ingresso": input_ano_ingresso,
        "Idade": input_idade,
        "Fase": input_fase,
        "Número de avaliações": input_num_av,
        "IAN": input_ian,
        "IAA": input_iaa,
        "IDA": input_ida,
        "IEG": input_ieg,
        "IPS": input_ips,
        "Defasagem atual": input_defasagem,
        "Pedra anterior": input_pedra_anterior,
        "INDE calculado": inde_atual
    }


    if (
        input_fase is not None
        and input_fase < 8
    ):

        campos["IPP"] = input_ipp
        campos["IPV"] = input_ipv


    campos_faltantes = [
        nome
        for nome, valor in campos.items()
        if valor is None
    ]


    if campos_faltantes:

        st.error(
            "Preencha todos os campos necessários antes de enviar. "
            "Campos pendentes: "
            + ", ".join(campos_faltantes)
        )


    elif input_ano_ingresso > input_ano:

        st.error(
            "O ano de ingresso não pode ser posterior "
            "ao ano de referência."
        )


    else:

        try:

            ipp_para_modelo = (
                float(input_ipp)
                if input_ipp is not None
                else float("nan")
            )


            ipv_para_modelo = (
                float(input_ipv)
                if input_ipv is not None
                else float("nan")
            )

            dados_aluno = {

                "RA": "STREAMLIT",

                "Nome": "Aluno avaliado",

                "Gênero": "Não informado",

                "Ano": int(
                    input_ano
                ),

                "Idade": int(
                    input_idade
                ),

                "Ano ingresso": int(
                    input_ano_ingresso
                ),

                "Fase_num": int(
                    input_fase
                ),

                "Nº Av": int(
                    input_num_av
                ),

                "IAA": float(
                    input_iaa
                ),

                "IDA": float(
                    input_ida
                ),

                "IEG": float(
                    input_ieg
                ),

                "IPP": ipp_para_modelo,

                "IPS": float(
                    input_ips
                ),

                "IPV": ipv_para_modelo,

                "Pedra_anterior": (
                    input_pedra_anterior
                ),

                "Defasagem": int(
                    input_defasagem
                ),

                "INDE_atual": float(
                    inde_atual
                )
            }


            resultado = prever_risco(
                dados_aluno
            )


            score_risco = resultado[
                "probabilidade"
            ]


            threshold = resultado[
                "threshold"
            ]


            predicao = resultado[
                "classe"
            ]

            st.divider()

            st.write(
                "#### RESULTADO"
            )


            st.metric(
                "INDE atual calculado",
                f"{inde_atual:.4f}"
            )


            st.metric(
                "Risco estimado pelo modelo",
                f"{score_risco * 100:.1f}%"
            )

            if predicao == 0:

                st.success(
                    "### Risco de defasagem "
                    "não sinalizado pelo modelo."
                )


            else:

                st.error(
                    "### Risco de pdefasagem "
                    "sinalizado pelo modelo."
                )

                st.warning(
                    "O resultado indica necessidade de atenção "
                    "e acompanhamento. A previsão não determina "
                    "que o aluno necessariamente entrará em defasagem."
                )

        except Exception as erro:

            st.error(
                "Não foi possível realizar a previsão."
            )

            st.exception(
                erro
            )