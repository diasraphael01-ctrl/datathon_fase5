import streamlit as st

st.set_page_config(
    page_title="Datathon | Passos Mágicos",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.html("""
<style>

    .block-container {
        max-width: 1180px;

        padding-top: 3.2rem;
        padding-bottom: 0.8rem;
    }


    [data-testid="stAppViewContainer"] {
        background:
            linear-gradient(
                180deg,
                #f8fafc 0%,
                #ffffff 100%
            );
    }


    [data-testid="stVerticalBlock"] {
        gap: 0.55rem;
    }

    .hero {
        position: relative;

        overflow: hidden;

        background:
            linear-gradient(
                135deg,
                #315a9e 0%,
                #3f6eb3 55%,
                #5a82bd 100%
            );

        border-radius: 20px;

        padding:
            24px
            38px
            22px
            38px;

        margin-bottom: 14px;

        box-shadow:
            0 10px 28px
            rgba(30, 64, 120, 0.12);
    }


    .hero::before {
        content: "";

        position: absolute;

        width: 240px;
        height: 240px;

        right: -80px;
        top: -130px;

        border:
            1px solid
            rgba(255, 255, 255, 0.12);

        border-radius: 50%;
    }


    .hero::after {
        content: "";

        position: absolute;

        width: 150px;
        height: 150px;

        right: 120px;
        bottom: -120px;

        border:
            1px solid
            rgba(255, 255, 255, 0.07);

        border-radius: 50%;
    }


    .hero-content {
        position: relative;

        z-index: 2;
    }


    .hero-kicker {
        color: #dbeafe;

        font-size: 0.76rem;

        font-weight: 700;

        letter-spacing: 0.11em;

        text-transform: uppercase;

        margin-bottom: 6px;
    }


    .hero-title {
        color: #ffffff;

        font-size: 2.1rem;

        line-height: 1.08;

        font-weight: 800;

        margin: 0;
    }


    .hero-case {
        color: #eef6ff;

        font-size: 1.08rem;

        font-weight: 500;

        margin-top: 6px;
    }


    .hero-line {
        width: 60px;

        height: 3px;

        background: #bfdbfe;

        border-radius: 5px;

        margin-top: 11px;

        margin-bottom: 16px;
    }

    .student-grid {
        display: grid;

        grid-template-columns:
            2fr
            0.8fr
            0.8fr
            1fr;

        gap: 10px;
    }


    .student-item {
        background:
            rgba(255, 255, 255, 0.13);

        border:
            1px solid
            rgba(255, 255, 255, 0.18);

        border-radius: 10px;

        padding:
            9px
            13px;
    }


    .student-label {
        color: #dbeafe;

        font-size: 0.62rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.06em;

        margin-bottom: 2px;
    }


    .student-value {
        color: #ffffff;

        font-size: 0.90rem;

        font-weight: 700;

        line-height: 1.2;
    }

    .project-description {
        background: #eff6ff;

        border-left:
            4px solid
            #4f76ae;

        border-radius: 8px;

        padding:
            12px
            18px;

        color: #334155;

        font-size: 0.91rem;

        line-height: 1.4;

        margin-bottom: 14px;
    }

    .pages-header {
        display: flex;

        align-items: baseline;

        justify-content: space-between;

        gap: 20px;

        margin-bottom: 8px;
    }


    .section-title {
        color: #0f172a;

        font-size: 1.18rem;

        font-weight: 800;
    }


    .section-subtitle {
        color: #64748b;

        font-size: 0.78rem;

        text-align: right;
    }

    .pages-card {
        background: #ffffff;

        border:
            1px solid
            #e2e8f0;

        border-radius: 14px;

        padding:
            3px
            20px;

        box-shadow:
            0 5px 18px
            rgba(15, 23, 42, 0.035);
    }


    .page-item {
        display: flex;

        align-items: center;

        min-height: 47px;

        border-bottom:
            1px solid
            #f1f5f9;
    }


    .page-item:last-child {
        border-bottom: none;
    }


    .page-number {
        width: 29px;

        height: 29px;

        display: flex;

        align-items: center;

        justify-content: center;

        flex-shrink: 0;

        margin-right: 11px;

        background: #edf3fb;

        color: #315a9e;

        border-radius: 8px;

        font-size: 0.76rem;

        font-weight: 800;
    }


    .page-name {
        color: #334155;

        font-size: 0.89rem;

        font-weight: 600;
    }

    .footer {
        text-align: center;

        color: #94a3b8;

        font-size: 0.70rem;

        margin-top: 10px;

        padding-top: 7px;

        border-top:
            1px solid
            #e2e8f0;
    }

    @media (max-width: 900px) {

        .student-grid {
            grid-template-columns:
                repeat(2, 1fr);
        }


        .pages-header {
            display: block;
        }


        .section-subtitle {
            text-align: left;

            margin-top: 3px;
        }

    }


    @media (max-width: 600px) {

        .block-container {
            padding-top: 3rem;
        }


        .hero {
            padding:
                22px
                22px;
        }


        .hero-title {
            font-size: 1.8rem;
        }


        .student-grid {
            grid-template-columns: 1fr;
        }

    }

</style>
""")

st.html("""
<div class="hero">

    <div class="hero-content">

        <div class="hero-kicker">
            FIAP • Pós Tech em Data Analytics
        </div>

        <div class="hero-title">
            Datathon - Fase 5
        </div>

        <div class="hero-case">
            Case: Passos Mágicos
        </div>

        <div class="hero-line"></div>


        <div class="student-grid">

            <div class="student-item">

                <div class="student-label">
                    Aluno
                </div>

                <div class="student-value">
                    Raphael Dias de Souza
                </div>

            </div>


            <div class="student-item">

                <div class="student-label">
                    RM
                </div>

                <div class="student-value">
                    369750
                </div>

            </div>


            <div class="student-item">

                <div class="student-label">
                    Grupo
                </div>

                <div class="student-value">
                    26
                </div>

            </div>


            <div class="student-item">

                <div class="student-label">
                    Ano de realização
                </div>

                <div class="student-value">
                    2026
                </div>

            </div>

        </div>

    </div>

</div>
""")

st.html("""
<div class="project-description">

    Projeto apresentado para composição da nota final de aprovação
    e conclusão da
    <strong>Pós Tech em Data Analytics da FIAP</strong>,
    desenvolvido a partir do case da
    <strong>Associação Passos Mágicos</strong>.

</div>
""")

st.html("""
<div class="pages-header">

    <div class="section-title">
        Páginas do projeto
    </div>

    <div class="section-subtitle">
        Utilize o menu lateral para navegar pelas análises e pelo modelo preditivo.
    </div>

</div>
""")

coluna_1, coluna_2 = st.columns(
    2,
    gap="medium"
)

with coluna_1:

    st.html("""
    <div class="pages-card">

        <div class="page-item">

            <div class="page-number">
                1
            </div>

            <div class="page-name">
                Dashboard (pág 1): Panorama de Adequação de Desempenho
            </div>

        </div>


        <div class="page-item">

            <div class="page-number">
                2
            </div>

            <div class="page-name">
                Dashboard (pág 2): Engajamento e Autopercepção
            </div>

        </div>


        <div class="page-item">

            <div class="page-number">
                3
            </div>

            <div class="page-name">
                Dashboard (pág 3): Desenvolvimento Psicossocial
            </div>

        </div>

    </div>
    """)

with coluna_2:

    st.html("""
    <div class="pages-card">

        <div class="page-item">

            <div class="page-number">
                4
            </div>

            <div class="page-name">
                Dashboard (pág 4): IPV e Indicadores Multidimensionais
            </div>

        </div>


        <div class="page-item">

            <div class="page-number">
                5
            </div>

            <div class="page-name">
                Dashboard (pág 1): Risco, Evolução e Impacto
            </div>

        </div>


        <div class="page-item">

            <div class="page-number">
                6
            </div>

            <div class="page-name">
                Modelo Preditivo - Detectar Risco de Defasagem
            </div>

        </div>

    </div>
    """)

st.html("""
<div class="footer">

    Datathon • Fase 5 • FIAP Pós Tech em Data Analytics • 2026

</div>
""")