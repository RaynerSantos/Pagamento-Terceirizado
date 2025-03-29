import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
from Funcoes import ler_tabela, incluir_servico, apagar_tabela, incluir_login, alterar_senha, excluir_login

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\PROJETOS\Pagamento Terceirizado\Ignorar\pagamento-terceirizado-467d410b51b5.json"

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

    [data-testid="stSidebar"] {
        display: none;  /* 👈 Esconde o menu lateral */
    }

    [data-testid="stAppViewContainer"] > .main {
        margin-left: 0;  /* 👈 Remove o espaço lateral */
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