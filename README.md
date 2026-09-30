# Datathon - Fase 5 - Passos Mágicos

Projeto desenvolvido para o **Datathon da Fase 5 da Pós Tech em Data Analytics - FIAP**, utilizando o case da **Associação Passos Mágicos**.

## Aluno

- **Nome:** Raphael Dias de Souza
- **RM:** 369750
- **Grupo:** 26
- **Ano:** 2026

## Sobre o projeto

A aplicação apresenta dashboards analíticos com indicadores educacionais e um modelo preditivo para sinalização de risco de perda de posição do aluno no ano seguinte.

O projeto utiliza dados do PEDE 2022–2024 e combina análise exploratória, análise longitudinal e Machine Learning.

## Modelo preditivo

O modelo final utilizado é um **Random Forest Classifier** com balanceamento de classes e threshold de **0,25**.

A previsão deve ser interpretada como apoio à priorização de acompanhamento, e não como decisão automática.

## Tecnologias

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Matplotlib
- Joblib

## Como executar localmente

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
streamlit run app.py
```

## Estrutura principal

```text
app.py
pages/
src/
data/
modelo/
requirements.txt
```

## Deploy

A aplicação foi preparada para publicação no **Streamlit Community Cloud**.
