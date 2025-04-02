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


# Nome do projeto, dataset e tabela
project_id = "pagamento-terceirizado"
dataset_id = "pagamento_terceirizado"
table_id = "login_colaborador"  # "horas_colaborador" / "login_colaborador"

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


# Criar um estado de sessão para verificar login
if "login_sucesso" not in st.session_state:
    st.session_state.login_sucesso = False

# Criar um estado de sessão para verificar login de administrador
if "login_admin_sucesso" not in st.session_state:
    st.session_state.login_admin_sucesso = False

#=== Título ===#
st.title("Pagamento Transcrição/Corte")

# Formulário de login
with st.form(key="login"):
    LOGIN = st.text_input(label="Insira o seu login de acesso")
    SENHA = st.text_input(label="Insira a sua senha", type='password', placeholder="Senha padrão: 123")
    input_buttom_submit = st.form_submit_button("Entrar")

# Se o botão for pressionado, verifica login
if input_buttom_submit:
    df_logins = ler_tabela(project_id="pagamento-terceirizado", 
                           dataset_id="pagamento_terceirizado", 
                           table_id="login_colaborador")
    if ((df_logins['LOGIN'] == LOGIN) & (df_logins['SENHA'] == SENHA)).any():
        st.session_state.login_sucesso = True  # Define o estado do login como verdadeiro
        st.session_state.LOGIN = LOGIN  # Salva o usuário na sessão
        st.session_state.SENHA = SENHA # Salva a senha do usuário na sessão
        if LOGIN == 'admin':
            st.session_state.login_admin_sucesso = True
        st.rerun()  # Recarrega a página para aplicar a mudança
    else:
        st.warning("❌ Login ou senha incorretos!")

# Se login for bem-sucedido, redireciona para a página de Servico_Prestado ou página do Administrador
if st.session_state.login_admin_sucesso:
    st.switch_page("pages/Administrador.py")
elif st.session_state.login_sucesso:
    st.switch_page("pages/Servico_Prestado.py")
