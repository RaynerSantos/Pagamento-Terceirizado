import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
from Funcoes import ler_tabela, incluir_servico, apagar_tabela, incluir_login, alterar_senha, excluir_login
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
        color: #FFFFFF;
        text-align: center;
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
    </style>
    """,
    unsafe_allow_html=True
)

if "login_sucesso" not in st.session_state or not st.session_state.login_sucesso:
    st.warning("❌ Você precisa fazer login!")
    st.stop()

#=== Título ===#
st.title("Pagamento Terceirizado")
st.write("")
st.write(f"Bem-vindo, **{st.session_state.LOGIN}**! 😊")
st.write("")
if st.button("🔒 Alterar minha senha"):
    st.switch_page("pages/Alterar_Senha.py")

st.write("")
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
    SERVICO = st.selectbox(label="Informe o tipo de serviço prestado", options=["MONITORIA", "TRANSCRIÇÃO/CORTE"])
    DESCRICAO = st.selectbox(label="Informe a descrição do tipo de serviço prestado", options=["EXAME DE DADOS", "TRANSCRIÇÃO/CORTE"])
    PROJETO = st.text_input(label="Informe o nome do projeto", placeholder="1217-1 - Cielo / CP / Satisfação 1ª onda_2025")
    PERIODO = st.text_input(label="Informe o período no qual o projeto ocorreu", placeholder="17/08/2024 A 16/09/2024")
    HORAS = st.text_input(label="Informe a quantidade de horas trabalhadas no formato hh:mm:ss", placeholder="162:36:00")
    VALOR = st.text_input(label="Informe o valor da hora trabalhada", placeholder="15,00")
    QUEM_EMITE = st.selectbox(label="Informe quem emite a NF", options=["MEI", "PJ"])
    OBSERVACAO = st.text_input(label="Caso outra pessoa emita a NF favor informar ou deixar em branco", 
                               placeholder="LUCAS SANTOS EMITE")
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
                        OBSERVACAO=OBSERVACAO)
        st.success("✅ Serviço incluído com sucesso!")
        st.write("Você já pode fechar a página.")

    except ValueError:
        st.error("❌ Valor da hora inválido. Use vírgula como separador decimal (Ex.: 15,00).")