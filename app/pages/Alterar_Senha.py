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
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔐 Alterar Senha")
# Verifica se o usuário está logado
if "LOGIN" in st.session_state:
    st.write(f"Olá, **{st.session_state.LOGIN}**! Digite sua nova senha abaixo:")
    
    with st.form("form_alterar_senha"):
        nova_senha = st.text_input("Nova senha", type="password")
        confirmar_senha = st.text_input("Confirme a nova senha", type="password")
        btn_alterar = st.form_submit_button("Alterar senha")
    
    if btn_alterar:
        if nova_senha != confirmar_senha:
            st.error("❌ As senhas não coincidem.")
        elif nova_senha.strip() == "":
            st.warning("⚠️ A nova senha não pode estar em branco.")
        else:
            df_logins = ler_tabela(project_id="pagamento-terceirizado", 
                                   dataset_id="pagamento_terceirizado", 
                                   table_id="login_colaborador")
            alterar_senha(project_id="pagamento-terceirizado", 
                          dataset_id="pagamento_terceirizado", 
                          table_id="login_colaborador", 
                          LOGIN=st.session_state.LOGIN, 
                          SENHA=nova_senha, 
                          df_logins=df_logins)
            st.success("✅ Senha alterada com sucesso!")
else:
    st.warning("⚠️ Você precisa estar logado para alterar sua senha.")