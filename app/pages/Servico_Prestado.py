import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
from Funcoes import ler_tabela, incluir_servico, apagar_tabela, incluir_login, alterar_senha, excluir_login, salvar_excel_com_formatacao
import json
from google.oauth2 import service_account

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\PROJETOS\Pagamento Terceirizado\Ignorar\pagamento-terceirizado-467d410b51b5.json"

# Carrega a chave do Streamlit Secrets
gcp_info = json.loads(st.secrets["gcp_service_account"])

# Cria credencial a partir do dicionário
credentials = service_account.Credentials.from_service_account_info(gcp_info)

# CSS personalizado
st.markdown(
    """
    <style>
    /* Cor de fundo da página */
    [data-testid="stAppViewContainer"] {
        background-color: #000000;
    }

    /* Cor de fundo do cabeçalho */
    [data-testid="stHeader"] {
        background-color: #000000;
    }

    /* Esconde o menu lateral */
    [data-testid="stSidebar"] {
        display: none;  /* 👈 Esconde o menu lateral */
    }

    /* Remove o espaço lateral */
    [data-testid="stAppViewContainer"] > .main {
        margin-left: 0;  /* 👈 Remove o espaço lateral */
    }

    /* Cor de fundo da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #333333;
    }

    /* Cor do título */
    h1 {
    color: white !important;
    text-align: center;
    font-weight: bold;
}

    /* Cor do subtítulo */
    h2 {
        color: #FFD700;
    }

    /* Cor do texto normal */
    p, span {
        color: #FFFFFF;
    }

    /* Cor dos botões */
    button {
        background-color: #20541B !important;
        color: white !important;
    }

    /* Caixa do formulário */
    div[data-testid="stForm"] {
        background-color: #1e1e1e;  /* cinza escuro */
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #444444;
        max-width: 600px;
        margin: auto;
    }

    /* Campos de texto */
    input, select, textarea {
        /* background-color: #2e2e2e !important; */
        /* color: white !important; */
        border: none !important;
        border-radius: 6px !important;
    }

    /* Botão */
    button[kind="primary"] {
        background-color: #20541B !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* table {
    background-color: #000000;
    color: white;
    border-collapse: collapse;
    width: 100%;
    border-radius: 10px;
    overflow: hidden;
    font-size: 14px;
    }
    th, td {
        border: 1px solid #333;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #111111;
        color: #FFFFFF;
    }
    tr:nth-child(even) {
        background-color: #1c1c1c;
    } */
    </style>
    """,
    unsafe_allow_html=True
)

if "login_sucesso" not in st.session_state or not st.session_state.login_sucesso:
    st.warning("❌ Você precisa fazer login!")
    st.stop()

#=== Título ===#
st.title("Horas e Serviços Prestados")
st.write("")
st.write(f"Bem-vindo, **{st.session_state.LOGIN}**! 😊")
st.write("")
if st.button("🔒 Alterar minha senha"):
    st.switch_page("pages/Alterar_Senha.py")



df = ler_tabela(project_id="pagamento-terceirizado", 
                dataset_id="pagamento_terceirizado", 
                table_id="horas_colaborador")
df_logins = ler_tabela(project_id="pagamento-terceirizado", 
                       dataset_id="pagamento_terceirizado", 
                       table_id="login_colaborador")
recuperar_nome = df_logins.loc[df_logins["LOGIN"] == st.session_state.LOGIN, "NOME_COMPLETO"]
df_usuario = df.loc[df["TERCEIRIZADO"] == recuperar_nome]

# Link para download
excel_data = salvar_excel_com_formatacao(df_usuario)
st.download_button(
    label="📥 Lançamentos passados",
    data=excel_data,
    file_name="Horas Colaborador.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.write("")
st.write("")
st.write("")

st.markdown(
    """
    <h5 style="color: white; text-align: center;">
        📝 Informe abaixo os dados sobre o serviço prestado
    </h5>
    """,
    unsafe_allow_html=True
)


# Formulário de preenchimento do serviço prestado
with st.form(key="servico"):
    TERCEIRIZADO = st.text_input(label="Informe o nome completo")
    SERVICO = st.selectbox(label="Informe o tipo de serviço prestado", options=["TRANSCRIÇÃO/CORTE"])
    DESCRICAO = st.selectbox(label="Informe a descrição do tipo de serviço prestado", options=["COMPILAÇÃO E FORNECIMENTO DE DADOS"])
    PROJETO = st.selectbox(label="Informe o nome do projeto", options=["1.217-1 CIELO/CP/SATISFAÇÃO 1ª ONDA_2025",
                                                                       "1.217-2 CIELO/CP/SATISFAÇÃO 2ª ONDA_2025",
                                                                       "1.217-3 CIELO/CP/SATISFAÇÃO 3ª ONDA_2025",
                                                                       "1.216-1 CIELO/CP/TRACKING NPS MENSAL 1ª ONDA_2025",
                                                                       "1.216-2 CIELO/CP/TRACKING NPS MENSAL 2ª ONDA_2025",
                                                                       "1.216-3 CIELO/CP/TRACKING NPS MENSAL 3ª ONDA_2025",
                                                                       "1.216-4 CIELO/CP/TRACKING NPS MENSAL 4ª ONDA_2025",
                                                                       "1.216-5 CIELO/CP/TRACKING NPS MENSAL 5ª ONDA_2025",
                                                                       "1.216-6 CIELO/CP/TRACKING NPS MENSAL 6ª ONDA_2025",
                                                                       "1.216-7 CIELO/CP/TRACKING NPS MENSAL 7ª ONDA_2025",
                                                                       "1.216-8 CIELO/CP/TRACKING NPS MENSAL 8ª ONDA_2025",
                                                                       "1.216-9 CIELO/CP/TRACKING NPS MENSAL 9ª ONDA_2025"])
    PERIODO = st.text_input(label="Informe o período no qual o projeto ocorreu", placeholder="17/08/2024 A 16/09/2024")
    HORAS = st.text_input(label="Informe a quantidade de horas trabalhadas no formato hh:mm:ss", placeholder="162:36:00")
    VALOR = st.text_input(label="Informe o valor da hora trabalhada", placeholder="15,00")
    QUEM_EMITE = st.selectbox(label="Informe quem emite a NF", options=["MEI"])
    # OBSERVACAO = st.text_input(label="Caso outra pessoa emita a NF favor informar ou deixar em branco", 
    #                            placeholder="LUCAS SANTOS EMITE")
    input_buttom_submit = st.form_submit_button("Enviar")

if input_buttom_submit:
    # Converte o valor
    try:
        VALOR = float(VALOR.replace(",", "."))
        only_hour = HORAS.split(":")[0]
        only_min = HORAS.split(":")[1]
        min_para_calculo = int(int(only_min) * 100 / 60)
        total_horas_trabalhadas = float(only_hour + "." + str(min_para_calculo))
        TOTAL = total_horas_trabalhadas * VALOR

        incluir_servico(project_id="pagamento-terceirizado",
                        dataset_id="pagamento_terceirizado",
                        table_id="horas_colaborador",
                        TERCEIRIZADO=TERCEIRIZADO, 
                        SERVICO=SERVICO, 
                        DESCRICAO=DESCRICAO, 
                        PROJETO=PROJETO, 
                        PERIODO=PERIODO, 
                        HORAS=HORAS, 
                        VALOR=round(VALOR,2), 
                        TOTAL=round(TOTAL,2),
                        QUEM_EMITE=QUEM_EMITE, 
                        OBSERVACAO="")
        st.success("✅ Serviço incluído com sucesso!")
        st.write("Você já pode fechar a página.")

    except ValueError:
        st.error("❌ Valor da hora inválido. Use vírgula como separador decimal (Ex.: 15,00).")