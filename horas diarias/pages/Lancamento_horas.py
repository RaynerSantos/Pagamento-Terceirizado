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
    </style>
    """,
    unsafe_allow_html=True
)

PROJETO_ATUAL = "1.217-1 CIELO/CP/SATISFAÇÃO 1ª ONDA_2025"
# PERIODO_ATUAL = "01/04/2025 A 24/04/2025"
PERIODO_ATUAL = "01/03/2025 A 31/03/2025"

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
        📝 Preencha a tabela abaixo com o lançamento de suas horas para cada dia trabalhado
    </h5>
    """,
    unsafe_allow_html=True
)

# # Formulário de preenchimento do serviço prestado
# with st.form(key="hora_diaria"):
#     PROJETO = st.selectbox(label="Informe o nome do projeto", options=["1.217-1 CIELO/CP/SATISFAÇÃO 1ª ONDA_2025", 
#                                                                        "1.216-1 CIELO/CP/TRACKING NPS MENSAL 1ª ONDA_2025"])
#     NOME_COMPLETO = st.text_input(label="Informe seu nome completo")
#     CPF = st.text_input(label="Informe o seu CPF", placeholder="xxx.xxx.xxx-xx")
#     TELEFONE = st.text_input(label="Informe o seu telefone", placeholder="(xx)xxxxx-xxxx")
#     VALOR_HORA = st.text_input(label="Informe o valor da hora trabalhada", placeholder="17,00")
#     DATA = st.selectbox(label="Informe a data referente ao dia trabalhado", options=["07/03/2025", "08/03/2025", "09/03/2025",
#                                                                                      "10/03/2025", "11/03/2025", "12/03/2025",
#                                                                                      "13/03/2025", "14/03/2025", "15/03/2025",
#                                                                                      "16/03/2025", "17/03/2025", "18/03/2025",
#                                                                                      "19/03/2025", "20/03/2025", "21/03/2025",
#                                                                                      "22/03/2025", "23/03/2025", "24/03/2025",
#                                                                                      "25/03/2025", "26/03/2025", "27/03/2025",
#                                                                                      "28/03/2025", "29/03/2025", "30/03/2025", "31/03/2025"])
#     QTD_HORAS = st.text_input(label="Informe a quantidade de horas trabalhadas referente ao dia informado acima")
#     st.write("")
#     st.markdown(
#     """
#     <h5 style="color: white; text-align: center;">
#         Informe os dados bancários abaixo
#     </h5>
#     """,
#     unsafe_allow_html=True
# )
#     # st.write("Informe os dados bancários abaixo")
#     BANCO = st.text_input(label="Informe o Banco que deseja receber o pagamento")
#     AGENCIA = st.text_input(label="Informe a agência")
#     CONTA = st.text_input(label="Informe o número da conta")
#     TIPO_PIX = st.selectbox(label="Pix", options=["Telefone", "CPF", "E-mail"])
#     CHAVE_PIX = st.text_input(label="Informe a chave pix")
#     input_buttom_submit = st.form_submit_button("Enviar")


# if input_buttom_submit:
#     st.session_state.conferir_editar = True
#     st.session_state.PROJETO = PROJETO
#     st.session_state.NOME_COMPLETO = NOME_COMPLETO
#     st.session_state.CPF = CPF
#     st.session_state.TELEFONE = TELEFONE
#     st.session_state.VALOR_HORA = VALOR_HORA
#     st.session_state.DATA = DATA
#     st.session_state.QTD_HORAS = QTD_HORAS
#     st.session_state.BANCO = BANCO
#     st.session_state.AGENCIA = AGENCIA
#     st.session_state.CONTA = CONTA
#     st.session_state.TIPO_PIX = TIPO_PIX
#     st.session_state.CHAVE_PIX = CHAVE_PIX

#     st.switch_page("pages/Conferir_Editar.py")


st.write("")
st.write("")

df_logins = ler_tabela(project_id="pagamento-terceirizado",  
                       dataset_id="pagamento_terceirizado", 
                       table_id="login_colaborador")
df = ler_tabela(project_id="pagamento-terceirizado", 
                dataset_id="pagamento_terceirizado", 
                table_id="horas_diaria_colaborador")
st.session_state.df = df
recuperar_nome = df_logins.loc[df_logins["LOGIN"] == st.session_state.LOGIN, "NOME_COMPLETO"]

if not recuperar_nome.empty:
    recuperar_nome = recuperar_nome.iloc[0]
    st.session_state.recuperar_nome = recuperar_nome

    # Convertendo a coluna "DATA" para datetime
    df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d')
    # Separando o intervalo do PERIODO_ATUAL
    intervalo_periodo_atual = PERIODO_ATUAL.split(" A ")
    data_inicial = pd.to_datetime(intervalo_periodo_atual[0], dayfirst=True)
    data_final = pd.to_datetime(intervalo_periodo_atual[1], dayfirst=True)
    st.session_state.data_inicial = data_inicial
    st.session_state.data_final = data_final

    df_usuario = df.loc[(df["NOME_COMPLETO"] == recuperar_nome) & (df["DATA"] >= data_inicial) & (df["DATA"] <= data_final)]
    df_usuario = df_usuario.reset_index(drop=True)
    df_usuario_excel = df_usuario.iloc[0:len(df_usuario), 0:df_usuario.shape[1]-1]
    df_usuario = df_usuario[['PROJETO','NOME_COMPLETO','CPF','TELEFONE','VALOR_HORA','DATA','QTD_HORAS']]
    # df_usuario['DATA'] = df_usuario['DATA'].dt.strftime('%d/%m/%Y')

    def highlight_projeto_column(val):
        return 'background-color: #E8E8E8'  # cinza claro

    # Aplica o estilo apenas à coluna "PROJETO"
    styled_df = df_usuario.style.applymap(highlight_projeto_column, subset=['PROJETO'])

    # Agora configurar o editor:
    df_usuario_edited = st.data_editor(styled_df, 
                                       hide_index=True,  # Esconder coluna de índices
                                       num_rows='dynamic',  # Usuário poderá adicionar ou remover linhas
                                       disabled=["PROJETO"],  # Travar o valor do Projeto para o usuário não alterar
                                       column_config={"DATA": st.column_config.DateColumn(label="DATA", 
                                                                                          format="DD/MM/YYYY",  # formato de exibição
                                                                                          step=1,               # passo de 1 dia ao escolher
                                                                                          ),
                                                      "VALOR_HORA": st.column_config.NumberColumn("VALOR_HORA",
                                                                                                   help="Number decimal",
                                                                                                   format="R$ %.2f"
         )
                                                                                        }
                                                                                    )
    # Link para download
    excel_data = salvar_excel_com_formatacao(df_usuario_excel)
    st.download_button(
        label="📥 Baixar em Excel",
        data=excel_data,
        file_name="Horas Colaborador.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    st.write("")
    if st.button("💾 Salvar dados"):
        df_usuario_edited["DATA"] = pd.to_datetime(df_usuario_edited["DATA"]).dt.date
        st.session_state.df_usuario_edited = df_usuario_edited
        st.session_state.conferir_editar = True
        st.switch_page("pages/Conferir_Editar.py")


st.write("")
st.write("")
st.write("")
if st.button("🔄 Recarregar página"):
    st.rerun()

    