import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
import json
from google.oauth2 import service_account
from datetime import datetime
from Funcoes import ler_tabela, incluir_horas, salvar_excel_com_formatacao

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\PROJETOS\Pagamento Terceirizado\Ignorar\pagamento-terceirizado-467d410b51b5.json"

# Nome do projeto, dataset e tabela
project_id = "pagamento-terceirizado"
dataset_id = "pagamento_terceirizado"
table_id = "horas_diaria_colaborador"  # "horas_diaria_colaborador" / "login_colaborador"

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

PROJETO_ATUAL = "1.217-1 CIELO/CP/SATISFAÇÃO 1ª ONDA_2025"
# PERIODO_ATUAL = "01/04/2025 A 24/04/2025"
PERIODO_ATUAL = "01/03/2025 A 08/03/2025"

st.title("🔍 Conferir e Enviar")  # "🔍 Conferir informações a serem registradas"
st.write("")
st.write("")

# Verifica se o usuário está logado
if "LOGIN" in st.session_state and st.session_state.conferir_editar:
    df = st.session_state.df
    df_usuario = df.loc[~(df["NOME_COMPLETO"] == st.session_state.recuperar_nome) & (df["DATA"] >= st.session_state.data_inicial) & (df["DATA"] <= st.session_state.data_final)]

    df_usuario_edited = st.session_state.df_usuario_edited
    df_usuario_edited['VALOR_TOTAL'] = df_usuario_edited['VALOR_HORA'] * df_usuario_edited['QTD_HORAS']

    st.dataframe(df_usuario_edited, hide_index=True, column_config={
        #  "VALOR_TOTAL": "VALOR_TOTAL",
         "VALOR_TOTAL": st.column_config.NumberColumn(
            "VALOR_TOTAL",
            help="Number decimal",
             format="R$ %.2f"
         ) } )

    # # Converte o valor
    # try:
    #     VALOR_HORA = float(st.session_state.VALOR_HORA.replace(",", "."))
    #     QTD_HORAS = float(st.session_state.QTD_HORAS.replace(",", "."))
    #     lista_data = st.session_state.DATA.split("/")
    #     ano = lista_data[2]
    #     mes = lista_data[1]
    #     dia = lista_data[0]
    #     DATA = f"{ano}-{mes}-{dia}"
    #     print(f'Data: {DATA}')

    #     st.write(f"📌 Nome:\t**{st.session_state.recuperar_nome}**")
    #     st.write(f"📌 Projeto:\t**{st.session_state.PROJETO}**")
    #     st.write(f"📌 Valor da hora:\t**{st.session_state.VALOR_HORA}**")
    #     st.write(f"📌 Data:\t**{st.session_state.DATA}**")
    #     st.write(f"📌 Horas trabalhadas:\t**R${st.session_state.QTD_HORAS}**")
    #     st.write(f"📌 Banco:\t**{st.session_state.BANCO}**")
    #     st.write(f"📌 Agência:\t**{st.session_state.AGENCIA}**")
    #     st.write(f"📌 Tipo PIX:\t**{st.session_state.TIPO_PIX}**")
    #     st.write(f"📌 Chave PIX:\t**{st.session_state.CHAVE_PIX}**")

    #     st.write("")
    #     st.write("")
    #     # st.write("Se as informações estão OK, clique em \"**Realizar lançamento**\" abaixo, caso contrário volte a página de serviços")
    #     st.markdown(
    #                 """
    #                 <h5 style="color: white; text-align: center;">
    #                     🔍 Se as informações estão OK, clique em \"<strong>Realizar lançamento</strong>\", caso contrário, volte para página de serviços.
    #                 </h5>
    #                 """,
    #                 unsafe_allow_html=True
    #             )
    #     if st.button("✔️ Realizar lançamento"):
    #         incluir_horas(project_id="pagamento-terceirizado", dataset_id="pagamento_terceirizado", table_id="horas_diaria_colaborador",
    #                   PROJETO=st.session_state.PROJETO,
    #                   NOME_COMPLETO=st.session_state.NOME_COMPLETO,
    #                   CPF=st.session_state.CPF,
    #                   TELEFONE=st.session_state.TELEFONE,
    #                   VALOR_HORA=VALOR_HORA,
    #                   DATA=DATA, 
    #                   QTD_HORAS=QTD_HORAS,
    #                   BANCO=st.session_state.BANCO,
    #                   AGENCIA=st.session_state.AGENCIA,
    #                   CONTA=st.session_state.CONTA,
    #                   TIPO_PIX=st.session_state.TIPO_PIX,
    #                   CHAVE_PIX=st.session_state.CHAVE_PIX)
    #         st.success("✅ Horas trabalhadas incluída com sucesso!")

    # except ValueError:
    #     st.error("❌ Valor da hora inválido. Por favor, insira um número válido.")

    st.write("")
    st.write("")
    st.write("")
    
    # Botão para voltar à página principal
    if st.button("🔙 Voltar para a página principal"):
        st.switch_page("pages/Lancamento_horas.py")
    st.write("")
    if st.button("🔄 Recarregar página"):
        st.rerun()
else:
    st.warning("⚠️ Você precisa estar logado!")
