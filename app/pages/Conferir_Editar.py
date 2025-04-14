import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
from Funcoes import ler_tabela, incluir_servico, apagar_tabela, incluir_login, alterar_senha, excluir_login, excluir_lancamento_sql
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

st.title("🔍 Conferir e Editar")  # "🔍 Conferir informações a serem registradas"
st.write("")
st.write("")

# Verifica se o usuário está logado
if "LOGIN" in st.session_state:

    # Converte o valor
    try:
        VALOR = float(st.session_state.VALOR.replace(",", "."))
        only_hour = st.session_state.HORAS_TOTAIS.split(":")[0]
        only_min = st.session_state.HORAS_TOTAIS.split(":")[1]
        min_para_calculo = int(int(only_min) * 100 / 60)
        total_horas_trabalhadas = float(only_hour + "." + str(min_para_calculo))
        PAGAMENTO_TOTAL = total_horas_trabalhadas * VALOR

        st.write(f"📌 Nome:\t**{st.session_state.recuperar_nome}**")
        st.write(f"📌 Projeto:\t**{st.session_state.PROJETO}**")
        st.write(f"📌 Período:\t**{st.session_state.PERIODO}**")
        st.write(f"📌 Horas totais trabalhadas:\t**{st.session_state.HORAS_TOTAIS}**")
        st.write(f"📌 Valor da hora:\t**R${st.session_state.VALOR}**")
        st.write(f"📌 Valor total a receber pelo período:\t**R${PAGAMENTO_TOTAL}**")

        st.write("")
        st.write("")
        # st.write("Se as informações estão OK, clique em \"**Realizar lançamento**\" abaixo, caso contrário volte a página de serviços")
        st.markdown(
                    """
                    <h5 style="color: white; text-align: center;">
                        🔍 Se as informações estão OK, clique em \"<strong>Realizar lançamento</strong>\", caso contrário, volte para página de serviços.
                    </h5>
                    """,
                    unsafe_allow_html=True
                )
        if st.button("✔️ Realizar lançamento"):
            incluir_servico(project_id="pagamento-terceirizado",
                            dataset_id="pagamento_terceirizado",
                            table_id="horas_colaborador",
                            TERCEIRIZADO=st.session_state.recuperar_nome, 
                            SERVICO=st.session_state.SERVICO, 
                            DESCRICAO=st.session_state.DESCRICAO, 
                            PROJETO=st.session_state.PROJETO, 
                            PERIODO=st.session_state.PERIODO, 
                            HORAS_TOTAIS=st.session_state.HORAS_TOTAIS, 
                            VALOR=round(VALOR,2), 
                            PAGAMENTO_TOTAL=round(PAGAMENTO_TOTAL,2),
                            TIPO_COLABORADOR=st.session_state.TIPO_COLABORADOR, 
                            QUEM_EMITE_A_NF=st.session_state.QUEM_EMITE_A_NF)
            st.success("✅ Serviço incluído com sucesso!")
            st.write("Você já pode fechar a página ou retornar para a página de serviços.")

    except ValueError:
        st.error("❌ Valor total da hora inválido. Use vírgula como separador decimal (Ex.: 17,00).")

    st.write("")
    st.write("")
    st.write("")
    
    # Botão para voltar à página principal
    if st.button("🔙 Voltar para a página de serviços"):
        st.switch_page("pages/Servico_Prestado.py")
else:
    st.warning("⚠️ Você precisa estar logado!")