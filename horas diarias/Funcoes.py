import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
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

# ===== Função para incluir um novo serviço prestado ===== #
def incluir_horas(project_id, dataset_id, table_id, 
                  PROJETO, NOME_COMPLETO, CPF, TELEFONE, VALOR_HORA, DATA, QTD_HORAS, BANCO, AGENCIA, CONTA, TIPO_PIX, CHAVE_PIX):
    # Inicializa o cliente
    client = bigquery.Client(project=project_id)

    # DataFrame com dados novos
    novos_dados = pd.DataFrame({
        "PROJETO": [PROJETO],
        "NOME_COMPLETO": [NOME_COMPLETO],
        "CPF": [CPF],
        "TELEFONE": [TELEFONE],
        "VALOR_HORA": [VALOR_HORA],
        "DATA": [DATA],
        "QTD_HORAS": [QTD_HORAS],
        "VALOR_TOTAL": [round(VALOR_HORA * QTD_HORAS, 2)],
        "BANCO": [BANCO],
        "AGENCIA": [AGENCIA],
        "CONTA": [CONTA],
        "TIPO_PIX": [TIPO_PIX],
        "CHAVE_PIX": [CHAVE_PIX]
    })

    # Define a tabela completa
    tabela_destino = f"{project_id}.{dataset_id}.{table_id}"

    # Insere no modo append
    job = client.load_table_from_dataframe(novos_dados, tabela_destino)
    job.result()  # Espera o job terminar
    print("Dados inseridos com sucesso!")
    return