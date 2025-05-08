import os
from google.cloud import bigquery
import pandas as pd
import streamlit as st
import numpy as np
import json
from google.oauth2 import service_account
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import PatternFill, Alignment, Font, Border, Side
from openpyxl.styles.numbers import BUILTIN_FORMATS
from io import BytesIO
from datetime import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\PROJETOS\Pagamento Terceirizado\Ignorar\pagamento-terceirizado-467d410b51b5.json"

# Nome do projeto, dataset e tabela
project_id = "pagamento-terceirizado"
dataset_id = "pagamento_terceirizado"
table_id = "login_colaborador"  # "horas_diaria_colaborador" / "login_colaborador"

# ===== Função para ler a tabela ===== #
def ler_tabela(project_id, dataset_id, table_id):
    # Inicializa o cliente
    client = bigquery.Client(project=project_id)

    # Consulta SQL para ler a tabela
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    df = client.query(query).to_dataframe()

    return df

LOGIN = 'andreia.goncalves'
PERIODO_ATUAL = "01/04/2025 A 24/04/2025"

df = pd.DataFrame({
    "LOGIN": ['andreia.goncalves', 'alice.ribeiro', 'joao.silva', 'andreia.goncalves', 'andreia.goncalves'],
    "SENHA": ['123', '123', '123', '123', '123'],
    "NOME_COMPLETO": ['ANDREIA GONCALVES', 'ALICE RIBEIRO', 'JOAO SILVA', 'ANDREIA GONCALVES', 'ANDREIA GONCALVES'],
    "VALOR_HORA": [17.00, 17.00, 17.00, 17.00, 17.00],
    "QTD_HORAS": [6, 5, 8, 3.5, 4.5],
    "PROJETO": ["1.217-1 CIELO/CP/SATISFAÇÃO 1ª ONDA_2025", "1.217-1 CIELO/CP/SATISFAÇÃO 1ª ONDA_2025", "Cielo NPS fevereiro 2025", "Cielo NPS fevereiro 2025", "Cielo NPS fevereiro 2025"],
    "DATA": ["2025-03-01", "2025-03-25", "2025-04-01", "2025-04-01", "2025-04-02"]
})

# # Exibindo a tabela editável
# edited_df = st.data_editor(df, hide_index=True, num_rows='dynamic')

# st.metric(label="Vendas Totais", value="R$ 10.000", delta="+5%", delta_color="normal")

# st.header("Este é um cabeçalho")
# st.subheader("Este é um subcabeçalho")
# st.text("Este é um texto simples")
# st.write("Este é um texto com write")

# st.image("images/SaberMaisQueroSaberMais.png", caption="Esta é uma imagem")

# valor = st.slider("Selecione um valor", 0, 100, 50)
# st.write("O valor selecionado é:", valor)

# if st.checkbox("Mostrar tabela"):
#     # Aplicar estilo
#     styled_df = df.style.set_properties(**{
#                 'background-color': 'black',  # Cor do fundo
#                 'color': 'white',             # Cor da fonte
#                 'border-color': 'black'       # Cor da borda
#             })

#     # Mostrar no Streamlit
#     st.dataframe(styled_df)

# col1, col2 = st.columns([2, 3])
# with col1:
#     st.metric(label="Métrica 1", value=123)
#     st.caption("Esta é alguma informação adicional sobre a Métrica 1.")
# with col2:
#     st.metric(label="Métrica 2", value=456)
#     st.caption("Esta é alguma informação adicional sobre a Métrica 2.")

# st.write("")
# st.write("")


print(f'dados:\n{df}')

recuperar_nome = df.loc[df["LOGIN"] == LOGIN, "NOME_COMPLETO"]

# Convertendo a coluna "DATA" para datetime
df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d')

# Separando o intervalo do PERIODO_ATUAL
intervalo_periodo_atual = PERIODO_ATUAL.split(" A ")
data_inicial = pd.to_datetime(intervalo_periodo_atual[0], dayfirst=True)
data_final = pd.to_datetime(intervalo_periodo_atual[1], dayfirst=True)

print(f'\nIntervalo de datas:\nData Inicial: {data_inicial}\nData Final: {data_final}')

# Agora filtrando:
resultado = df.loc[(df["LOGIN"] == LOGIN) & (df["DATA"] >= data_inicial) & (df["DATA"] <= data_final)]
resultado = resultado.reset_index(drop=True)
resultado = resultado.iloc[0:len(resultado), 0:resultado.shape[1]-1]
print("\nResultado final filtrado:")
print(resultado)

# st.data_editor(resultado, hide_index=True, num_rows='dynamic')



