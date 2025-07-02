import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
from Funcoes import ler_tabela, incluir_servico, incluir_login, alterar_senha, excluir_login, excluir_lancamento
import json
from google.oauth2 import service_account

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\PROJETOS\Pagamento Terceirizado\Ignorar\pagamento-terceirizado-467d410b51b5.json"

# # Carrega a chave do Streamlit Secrets
# gcp_info = json.loads(st.secrets["gcp_service_account"])

# # Cria credencial a partir do dicionário
# credentials = service_account.Credentials.from_service_account_info(gcp_info)

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

st.title("🗑️ Excluir Lançamento")
st.write("")
st.write("")

df = ler_tabela(sheet_name="Pagamento_Terceirizado", worksheet_name="horas_colaborador")
df_logins = ler_tabela(sheet_name="Pagamento_Terceirizado", worksheet_name="login_colaborador")

recuperar_nome = df_logins.loc[df_logins["LOGIN"] == st.session_state.LOGIN, "NOME_COMPLETO"]
recuperar_nome = recuperar_nome.iloc[0]

periodo_usuario = df.loc[df["TERCEIRIZADO"] == recuperar_nome, "PERIODO"]

# Verifica se o usuário está logado
if "LOGIN" in st.session_state:
    if not periodo_usuario.empty:
        periodo_usuario = periodo_usuario.iloc[-1]
        st.write(f"Você tem certeza que deseja excluir o **ÚLTIMO** lançamento referente ao período: {periodo_usuario} ?")
        if st.button("🗑️ Excluir Lançamento"):
            excluir_lancamento(sheet_name="Pagamento_Terceirizado", 
                               worksheet_name="horas_colaborador", 
                               TERCEIRIZADO=recuperar_nome, 
                               PERIODO=periodo_usuario)
            
            st.success(f"✅ lançamento do período {periodo_usuario} excluído com sucesso!")

    else:
        st.write("❌ Não há nenhum período com lançamento registrado!")

    
    st.write("")
    st.write("")
    st.write("")

    # Botão para voltar à página principal
    if st.button("🔙 Voltar para a página de serviços"):
        st.switch_page("pages/Servico_Prestado.py")
else:
    st.warning("⚠️ Você precisa estar logado para excluir lançamentos.")