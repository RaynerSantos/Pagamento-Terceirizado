import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
from Funcoes import ler_tabela, incluir_servico, apagar_tabela, incluir_login, alterar_senha, excluir_login, salvar_excel_com_formatacao
import json
from google.oauth2 import service_account
from datetime import datetime

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

df = ler_tabela(project_id="pagamento-terceirizado", 
                dataset_id="pagamento_terceirizado", 
                table_id="horas_colaborador")
df_logins = ler_tabela(project_id="pagamento-terceirizado", 
                    dataset_id="pagamento_terceirizado", 
                    table_id="login_colaborador")

PERIODO_1 = "20/03/2025 A 31/03/2025"
PERIODO_2 = "01/04/2025 A 24/04/2025"
PERIODO_3 = ""

recuperar_nome = df_logins.loc[df_logins["LOGIN"] == st.session_state.LOGIN, "NOME_COMPLETO"]
recuperar_nome = recuperar_nome.iloc[0]

periodo_usuario = df.loc[df["TERCEIRIZADO"] == recuperar_nome, "PERIODO"]

recuperar_ult_pagamento = df.loc[df["TERCEIRIZADO"] == recuperar_nome, "PAGAMENTO_TOTAL"]


#=== Título ===#
st.title("Pagamento Transcrição/Corte")
st.write("")
st.write(f"Bem-vindo, **{recuperar_nome}**! 😊")
if not recuperar_ult_pagamento.empty:
    df_usuario_periodo = df.loc[(df["TERCEIRIZADO"] == recuperar_nome) & ((df["PERIODO"] == PERIODO_1) | (df["PERIODO"] == PERIODO_2))]
    recuperar_ult_pagamento = df_usuario_periodo["PAGAMENTO_TOTAL"].sum()
    # recuperar_ult_pagamento = round(recuperar_ult_pagamento.iloc[-1], 2)
    recuperar_ult_pagamento = str(recuperar_ult_pagamento)
    recuperar_ult_pagamento = recuperar_ult_pagamento.replace(".", ",")
    st.write(f"Valor a receber no período: **R${recuperar_ult_pagamento}**")
else: 
    st.write("")
st.write("")
if st.button("🔒 Alterar minha senha"):
    st.switch_page("pages/Alterar_Senha.py")


# if not recuperar_nome.empty:
    # recuperar_nome = recuperar_nome.iloc[0]
df_usuario = df.loc[df["TERCEIRIZADO"] == recuperar_nome]

# Link para download
excel_data = salvar_excel_com_formatacao(df_usuario)
st.download_button(
    label="📥 Lançamentos passados",
    data=excel_data,
    file_name="Horas Colaborador.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# else: 
#     st.warning("⚠️ Não foi possível encontrar seu nome completo no banco de dados.")

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
                                                                    #    "1.217-2 CIELO/CP/SATISFAÇÃO 2ª ONDA_2025",
                                                                    #    "1.217-3 CIELO/CP/SATISFAÇÃO 3ª ONDA_2025",
                                                                       "1.216-1 CIELO/CP/TRACKING NPS MENSAL 1ª ONDA_2025"
                                                                    #    "1.216-2 CIELO/CP/TRACKING NPS MENSAL 2ª ONDA_2025",
                                                                    #    "1.216-3 CIELO/CP/TRACKING NPS MENSAL 3ª ONDA_2025",
                                                                    #    "1.216-4 CIELO/CP/TRACKING NPS MENSAL 4ª ONDA_2025",
                                                                    #    "1.216-5 CIELO/CP/TRACKING NPS MENSAL 5ª ONDA_2025",
                                                                    #    "1.216-6 CIELO/CP/TRACKING NPS MENSAL 6ª ONDA_2025",
                                                                    #    "1.216-7 CIELO/CP/TRACKING NPS MENSAL 7ª ONDA_2025",
                                                                    #    "1.216-8 CIELO/CP/TRACKING NPS MENSAL 8ª ONDA_2025",
                                                                    #    "1.216-9 CIELO/CP/TRACKING NPS MENSAL 9ª ONDA_2025"
                                                                       ])
    PERIODO = st.selectbox(label="Informe o período no qual o projeto ocorreu", options=[PERIODO_1, PERIODO_2])
    HORAS_TOTAIS = st.text_input(label="Informe a quantidade TOTAL DE HORAS trabalhadas no formato hh:mm:ss", placeholder="162:36:00")
    VALOR = st.text_input(label="Informe o valor da hora trabalhada", placeholder="17,00")
    TIPO_COLABORADOR = st.selectbox(label="Tipo de Colaborador", options=["MEI"])
    QUEM_EMITE_A_NF = st.text_input(label="Informe quem irá emitir a Nota", placeholder="FULANO DA SILVA")
    input_buttom_submit = st.form_submit_button("Enviar")

if input_buttom_submit:
    # Converte o valor
    try:
        VALOR = float(VALOR.replace(",", "."))
        only_hour = HORAS_TOTAIS.split(":")[0]
        only_min = HORAS_TOTAIS.split(":")[1]
        min_para_calculo = int(int(only_min) * 100 / 60)
        total_horas_trabalhadas = float(only_hour + "." + str(min_para_calculo))
        PAGAMENTO_TOTAL = total_horas_trabalhadas * VALOR

        incluir_servico(project_id="pagamento-terceirizado",
                        dataset_id="pagamento_terceirizado",
                        table_id="horas_colaborador",
                        TERCEIRIZADO=recuperar_nome, 
                        SERVICO=SERVICO, 
                        DESCRICAO=DESCRICAO, 
                        PROJETO=PROJETO, 
                        PERIODO=PERIODO, 
                        HORAS_TOTAIS=HORAS_TOTAIS, 
                        VALOR=round(VALOR,2), 
                        PAGAMENTO_TOTAL=round(PAGAMENTO_TOTAL,2),
                        TIPO_COLABORADOR=TIPO_COLABORADOR, 
                        QUEM_EMITE_A_NF=QUEM_EMITE_A_NF)
        st.success("✅ Serviço incluído com sucesso!")
        st.write("Você já pode fechar a página.")

    except ValueError:
        st.error("❌ Valor da hora inválido. Use vírgula como separador decimal (Ex.: 15,00).")

st.write("")
st.write("")
if st.button("🔄 Recarregar página"):
    st.rerun()