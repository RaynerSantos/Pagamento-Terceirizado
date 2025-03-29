import os
from google.cloud import bigquery
import pandas as pd
import numpy as np
import streamlit as st
import json
from google.oauth2 import service_account

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\PROJETOS\Pagamento Terceirizado\Ignorar\pagamento-terceirizado-467d410b51b5.json"

# Carrega a chave do Streamlit Secrets
gcp_info = json.loads(st.secrets["gcp_service_account"])

# Cria credencial a partir do dicionário
credentials = service_account.Credentials.from_service_account_info(gcp_info)

# Usa ao inicializar o cliente
client = bigquery.Client(credentials=credentials, project=gcp_info["pagamento-terceirizado"])

# Nome do projeto, dataset e tabela
project_id = "pagamento-terceirizado"
dataset_id = "pagamento_terceirizado"
table_id = "horas_colaborador"

# ===== Função para ler a tabela ===== #
def ler_tabela(project_id, dataset_id, table_id):
    # Inicializa o cliente
    client = bigquery.Client(credentials=credentials, project=gcp_info["pagamento-terceirizado"])

    # Consulta SQL para ler a tabela
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    df = client.query(query).to_dataframe()

    return df

# ===== Função para incluir um novo serviço prestado ===== #
def incluir_servico(project_id, dataset_id, table_id, 
                    TERCEIRIZADO, SERVICO, DESCRICAO, PROJETO, PERIODO, HORAS, VALOR, TOTAL, QUEM_EMITE, OBSERVACAO):
    # Inicializa o cliente
    client = bigquery.Client(credentials=credentials, project=gcp_info["pagamento-terceirizado"])

    # DataFrame com dados novos
    novos_dados = pd.DataFrame({
        "TERCEIRIZADO": [TERCEIRIZADO],
        "SERVICO": [SERVICO],
        "DESCRICAO": [DESCRICAO],
        "PROJETO": [PROJETO],
        "PERIODO": [PERIODO],
        "HORAS": [HORAS],
        "VALOR": [VALOR],
        "TOTAL": [TOTAL],
        "QUEM EMITE A NF": [QUEM_EMITE],
        "OBSERVACAO": [OBSERVACAO]
    })

    # Define a tabela completa
    tabela_destino = f"{project_id}.{dataset_id}.{table_id}"

    # Insere no modo append
    job = client.load_table_from_dataframe(novos_dados, tabela_destino)
    job.result()  # Espera o job terminar
    print("Dados inseridos com sucesso!")
    return

# ===== Função para incluir um novo login ===== #
def incluir_login(project_id, dataset_id, table_id, LOGIN, SENHA, NOME_COMPLETO):
    # Inicializa o cliente
    client = bigquery.Client(credentials=credentials, project=gcp_info["pagamento-terceirizado"])

    # DataFrame com dados novos
    novos_dados = pd.DataFrame({
        "LOGIN": [LOGIN],
        "SENHA": [SENHA],
        "NOME_COMPLETO": [NOME_COMPLETO]
    })

    # Define a tabela completa
    tabela_destino = f"{project_id}.{dataset_id}.{table_id}"

    # Insere no modo append
    job = client.load_table_from_dataframe(novos_dados, tabela_destino)
    job.result()  # Espera o job terminar
    print("Dados inseridos com sucesso!")
    return

# ===== Função para alterar a senha ===== #
def alterar_senha(project_id, dataset_id, table_id, LOGIN, SENHA, df_logins):
    # Atualiza a senha
    df_logins.loc[df_logins["LOGIN"] == LOGIN, "SENHA"] = SENHA

    # Envia a tabela inteira novamente, substituindo a antiga
    # client = bigquery.Client(credentials=credentials, project=gcp_info["pagamento-terceirizado"])
    client = bigquery.Client()
    tabela_destino = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")  # Sobrescreve
    job = client.load_table_from_dataframe(df_logins, tabela_destino, job_config=job_config)
    job.result()

    print("Senha alterada com sucesso!")
    return

# ===== Função para excluir login ===== #
def excluir_login(project_id, dataset_id, table_id, LOGIN, df_logins):
    # Exclui o login desejado
    df_logins = df_logins.loc[df_logins["LOGIN"] != LOGIN]

    # Envia a tabela inteira novamente, substituindo a antiga
    # client = bigquery.Client(credentials=credentials, project=gcp_info["pagamento-terceirizado"])
    client = bigquery.Client()
    tabela_destino = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")  # Sobrescreve
    job = client.load_table_from_dataframe(df_logins, tabela_destino, job_config=job_config)
    job.result()

    print("Login excluído com sucesso!")
    return


# ===== Função para apagar a tabela ===== #
def apagar_tabela(project_id, dataset_id, table_id):
    # Inicializa o cliente
    client = bigquery.Client(credentials=credentials, project=gcp_info["pagamento-terceirizado"])

    # Consulta SQL para apagar a tabela
    query = f"TRUNCATE TABLE `{project_id}.{dataset_id}.{table_id}`"
    query_job = client.query(query)
    query_job.result()
    print("Tabela truncada com sucesso!")
    return

# df_logins = ler_tabela(project_id="pagamento-terceirizado", dataset_id="pagamento_terceirizado", table_id="login_colaborador")
# print(df_logins)

# alterar_senha(project_id="pagamento-terceirizado", dataset_id="pagamento_terceirizado", table_id="login_colaborador", 
#               LOGIN='alice.ribeiro', SENHA='123', df_logins=df_logins)

# df_logins = ler_tabela(project_id="pagamento-terceirizado", dataset_id="pagamento_terceirizado", table_id="login_colaborador")
# print(df_logins)
