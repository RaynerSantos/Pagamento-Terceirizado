import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
import json
from google.oauth2 import service_account
from datetime import datetime
from Funcoes import ler_tabela, incluir_horas

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

#=== Título ===#
st.title("Lançamento de horas")
st.write("")
st.write(f"Bem-vindo, **{st.session_state.LOGIN}**! 😊")

st.write("")
st.write("")
st.write("")

st.markdown(
    """
    <h5 style="color: white; text-align: center;">
        📝 Preencha o formulário abaixo para realizar o lançamento de suas horas
    </h5>
    """,
    unsafe_allow_html=True
)

# Formulário de preenchimento do serviço prestado
with st.form(key="hora_diaria"):
    PROJETO = st.selectbox(label="Informe o nome do projeto", options=["1.217-1 CIELO/CP/SATISFAÇÃO 1ª ONDA_2025", 
                                                                       "1.216-1 CIELO/CP/TRACKING NPS MENSAL 1ª ONDA_2025"])
    NOME_COMPLETO = st.text_input(label="Informe seu nome completo")
    CPF = st.text_input(label="Informe o seu CPF", placeholder="xxx.xxx.xxx-xx")
    TELEFONE = st.text_input(label="Informe o seu telefone", placeholder="(xx)xxxxx-xxxx")
    VALOR_HORA = st.text_input(label="Informe o valor da hora trabalhada", placeholder="17,00")
    DATA = st.selectbox(label="Informe a data referente ao dia trabalhado", options=["07/03/2025", "08/03/2025", "09/03/2025",
                                                                                     "10/03/2025", "11/03/2025", "12/03/2025",
                                                                                     "13/03/2025", "14/03/2025", "15/03/2025",
                                                                                     "16/03/2025", "17/03/2025", "18/03/2025",
                                                                                     "19/03/2025", "20/03/2025", "21/03/2025",
                                                                                     "22/03/2025", "23/03/2025", "24/03/2025",
                                                                                     "25/03/2025", "26/03/2025", "27/03/2025",
                                                                                     "28/03/2025", "29/03/2025", "30/03/2025", "31/03/2025"])
    QTD_HORAS = st.text_input(label="Informe a quantidade de horas trabalhadas")
    st.write("")
    st.write("Informe os dados bancários abaixo")
    BANCO = st.text_input(label="Informe o Banco que deseja receber o pagamento")
    AGENCIA = st.text_input(label="Informe a agência")
    CONTA = st.text_input(label="Informe o número da conta")
    TIPO_PIX = st.selectbox(label="Pix", options=["Telefone", "CPF", "E-mail"])
    CHAVE_PIX = st.text_input(label="Informe a chave pix")
    input_buttom_submit = st.form_submit_button("Enviar")


if input_buttom_submit:
    # Converte o valor
    try:
        VALOR_HORA = float(VALOR_HORA.replace(",", "."))
        QTD_HORAS = float(QTD_HORAS.replace(",", "."))
        lista_data = DATA.split("/")
        ano = lista_data[2]
        mes = lista_data[1]
        dia = lista_data[0]
        DATA = f"{ano}-{mes}-{dia}"
        print(f'Data: {DATA}')

        incluir_horas(project_id="pagamento-terceirizado", dataset_id="pagamento_terceirizado", table_id="horas_diaria_colaborador",
                      PROJETO=PROJETO,
                      NOME_COMPLETO=NOME_COMPLETO,
                      CPF=CPF,
                      TELEFONE=TELEFONE,
                      VALOR_HORA=VALOR_HORA,
                      DATA=DATA, 
                      QTD_HORAS=QTD_HORAS,
                      BANCO=BANCO,
                      AGENCIA=AGENCIA,
                      CONTA=CONTA,
                      TIPO_PIX=TIPO_PIX,
                      CHAVE_PIX=CHAVE_PIX)
        st.success("✅ Serviço incluído com sucesso!")

    except ValueError:
        st.error("❌ Valor da hora inválido. Por favor, insira um número válido.")

st.write("")
st.write("")

df = ler_tabela(project_id="pagamento-terceirizado", 
                dataset_id="pagamento_terceirizado", 
                table_id="horas_diaria_colaborador")
st.dataframe(df, hide_index=True)

st.write("")
st.write("")
if st.button("🔄 Recarregar página"):
    st.rerun()

    