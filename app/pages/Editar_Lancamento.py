import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
from Funcoes import ler_tabela, incluir_servico, apagar_tabela, incluir_login, alterar_senha, excluir_login, excluir_lancamento_sql, atualizar_lancamento_sql
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

PERIODO_1 = "20/03/2025 A 31/03/2025"
PERIODO_2 = "01/04/2025 A 24/04/2025"
PERIODO_3 = "24/04/2025 A 04/05/2025"

df = ler_tabela(project_id="pagamento-terceirizado", 
                dataset_id="pagamento_terceirizado", 
                table_id="horas_colaborador")
df_logins = ler_tabela(project_id="pagamento-terceirizado", 
                    dataset_id="pagamento_terceirizado", 
                    table_id="login_colaborador")

recuperar_nome = df_logins.loc[df_logins["LOGIN"] == st.session_state.LOGIN, "NOME_COMPLETO"]
recuperar_nome = recuperar_nome.iloc[0]
periodo_usuario = df.loc[df["TERCEIRIZADO"] == recuperar_nome, "PERIODO"]

st.title("✏️ Editar Lançamento")  
st.write("")
st.write("")

# Verifica se o usuário está logado
if "LOGIN" in st.session_state:

    # if not periodo_usuario.empty:
    if PERIODO_2 in periodo_usuario.values:
        periodo_usuario = periodo_usuario.iloc[-1]
        df_usuario_periodo = df.loc[(df["TERCEIRIZADO"] == recuperar_nome) & (df["PERIODO"] == periodo_usuario)]

        # st.write("📋 Informações do último lançamento realizado")
        # st.dataframe(df_usuario_periodo[["TERCEIRIZADO","PROJETO","PERIODO","HORAS_TOTAIS","VALOR","PAGAMENTO_TOTAL"]], hide_index=True)
        # st.write("")

        st.write("📋 Informações do **ÚLTIMO** lançamento realizado")
        st.write(f"📌 Nome:\t**{df_usuario_periodo["TERCEIRIZADO"].iloc[0]}**")
        st.write(f"📌 Projeto:\t**{df_usuario_periodo["PROJETO"].iloc[0]}**")
        st.write(f"📌 Período:\t**{df_usuario_periodo["PERIODO"].iloc[0]}**")
        st.write(f"📌 Horas totais trabalhadas:\t**{df_usuario_periodo["HORAS_TOTAIS"].iloc[0]}**")
        st.write(f"📌 Valor da hora:\t**R${round(df_usuario_periodo['VALOR'].iloc[0], 2)}**")
        st.write(f"📌 Valor total a receber pelo período:\t**R${round(df_usuario_periodo["PAGAMENTO_TOTAL"].iloc[0], 2)}**")
        st.write("")
        st.write("")
        st.write("")

        st.markdown(
                    """
                    <h5 style="color: white; text-align: center;">
                        📝 Informe abaixo os dados corretos
                    </h5>
                    """,
                    unsafe_allow_html=True
        )

        with st.form(key="editar_lancamento"):
            NOVO_PROJETO = st.selectbox(label="Informe o nome do projeto", options=["1.217-1 CIELO/CP/SATISFAÇÃO 1ª ONDA_2025",
                                                                        #    "1.217-2 CIELO/CP/SATISFAÇÃO 2ª ONDA_2025",
                                                                        #    "1.217-3 CIELO/CP/SATISFAÇÃO 3ª ONDA_2025",
                                                                        # "1.216-1 CIELO/CP/TRACKING NPS MENSAL 1ª ONDA_2025"
                                                                        #    "1.216-2 CIELO/CP/TRACKING NPS MENSAL 2ª ONDA_2025",
                                                                           "1.216-3 CIELO/CP/TRACKING NPS MENSAL 3ª ONDA_2025",
                                                                        #    "1.216-4 CIELO/CP/TRACKING NPS MENSAL 4ª ONDA_2025",
                                                                        #    "1.216-5 CIELO/CP/TRACKING NPS MENSAL 5ª ONDA_2025",
                                                                        #    "1.216-6 CIELO/CP/TRACKING NPS MENSAL 6ª ONDA_2025",
                                                                        #    "1.216-7 CIELO/CP/TRACKING NPS MENSAL 7ª ONDA_2025",
                                                                        #    "1.216-8 CIELO/CP/TRACKING NPS MENSAL 8ª ONDA_2025",
                                                                        #    "1.216-9 CIELO/CP/TRACKING NPS MENSAL 9ª ONDA_2025"
                                                                        ])
            NOVO_PERIODO = st.selectbox(label="Informe o período no qual o projeto ocorreu", options=[PERIODO_2, PERIODO_3])
            NOVAS_HORAS_TOTAIS = st.text_input(label="Informe a quantidade TOTAL DE HORAS trabalhadas no formato hh:mm:ss", 
                                               placeholder="162:36:00")
            NOVO_VALOR = st.text_input(label="Informe o valor da hora trabalhada", placeholder="17,00")
            input_buttom_submit = st.form_submit_button("Enviar")

        if input_buttom_submit:
            # Converte o valor
            try:
                NOVO_VALOR = float(NOVO_VALOR.replace(",", "."))
                only_hour = NOVAS_HORAS_TOTAIS.split(":")[0]
                only_min = NOVAS_HORAS_TOTAIS.split(":")[1]
                min_para_calculo = int(int(only_min) * 100 / 60)
                total_horas_trabalhadas = float(only_hour + "." + str(min_para_calculo))
                PAGAMENTO_TOTAL = total_horas_trabalhadas * NOVO_VALOR

                st.write("")
                st.write("")
                atualizar_lancamento_sql(project_id="pagamento-terceirizado",
                                         dataset_id="pagamento_terceirizado",
                                         table_id="horas_colaborador",
                                         LOGIN=st.session_state.LOGIN,
                                         periodo_antigo=periodo_usuario,
                                         novo_projeto=NOVO_PROJETO,
                                         novo_periodo=NOVO_PERIODO,
                                         novas_horas=NOVAS_HORAS_TOTAIS,
                                         novo_valor=NOVO_VALOR,
                                         pagamento_total=PAGAMENTO_TOTAL,
                                         df_logins=df_logins
                                        )
                st.success("✅ Alteração realizada com sucesso!")

            except ValueError:
                st.error("❌ Valor total da hora inválido. Use vírgula como separador decimal (Ex.: 17,00).")
    else:
        st.warning(f"⚠️ Você ainda não possui nenhum lançamento no período {PERIODO_2}")

    st.write("")
    st.write("")
    st.write("")
    
    # Botão para voltar à página principal
    if st.button("🔙 Voltar para a página de serviços"):
        st.switch_page("pages/Servico_Prestado.py")
else:
    st.warning("⚠️ Você precisa estar logado!")