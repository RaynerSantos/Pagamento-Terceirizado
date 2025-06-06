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

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\PROJETOS\Pagamento Terceirizado\Ignorar\pagamento-terceirizado-467d410b51b5.json"

# Carrega a chave do Streamlit Secrets
gcp_info = json.loads(st.secrets["gcp_service_account"])

# Cria credencial a partir do dicionário
credentials = service_account.Credentials.from_service_account_info(gcp_info)

# Usa ao inicializar o cliente
client = bigquery.Client(credentials=credentials, project=gcp_info["project_id"])

# Nome do projeto, dataset e tabela
project_id = "pagamento-terceirizado"
dataset_id = "pagamento_terceirizado"
table_id = "horas_colaborador"

# ===== Função para ler a tabela ===== #
def ler_tabela(project_id, dataset_id, table_id):
    if table_id == "login_colaborador":
        # Inicializa o cliente
        client = bigquery.Client(credentials=credentials, project=gcp_info["project_id"])

        # Consulta SQL para ler a tabela
        query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
        df = client.query(query).to_dataframe()

    elif table_id == "horas_colaborador":
        # Inicializa o cliente
        client = bigquery.Client(credentials=credentials, project=gcp_info["project_id"])

        # Consulta SQL para ler a tabela
        query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}` ORDER BY DATA_CRIACAO ASC"
        df = client.query(query).to_dataframe()

    return df

# ===== Função para incluir um novo serviço prestado ===== #
def incluir_servico(project_id, dataset_id, table_id, 
                    TERCEIRIZADO, SERVICO, DESCRICAO, PROJETO, PERIODO, HORAS_TOTAIS, VALOR, PAGAMENTO_TOTAL, 
                    TIPO_COLABORADOR, QUEM_EMITE_A_NF):
    # Inicializa o cliente
    client = bigquery.Client(credentials=credentials, project=gcp_info["project_id"])

    # DataFrame com dados novos
    novos_dados = pd.DataFrame({
        "TERCEIRIZADO": [TERCEIRIZADO],
        "SERVICO": [SERVICO],
        "DESCRICAO": [DESCRICAO],
        "PROJETO": [PROJETO],
        "PERIODO": [PERIODO],
        "HORAS_TOTAIS": [HORAS_TOTAIS],
        "VALOR": [VALOR],
        "PAGAMENTO_TOTAL": [PAGAMENTO_TOTAL],
        "TIPO_COLABORADOR": [TIPO_COLABORADOR],
        "QUEM_EMITE_A_NF": [QUEM_EMITE_A_NF],
        "DATA_CRIACAO": [datetime.now()]
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
    client = bigquery.Client(credentials=credentials, project=gcp_info["project_id"])

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
    client = bigquery.Client(credentials=credentials, project=gcp_info["project_id"])
    # client = bigquery.Client()
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
    client = bigquery.Client(credentials=credentials, project=gcp_info["project_id"])
    # client = bigquery.Client()
    tabela_destino = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")  # Sobrescreve
    job = client.load_table_from_dataframe(df_logins, tabela_destino, job_config=job_config)
    job.result()

    print("Login excluído com sucesso!")
    return


# ===== Função para apagar a tabela ===== #
def apagar_tabela(project_id, dataset_id, table_id):
    # Inicializa o cliente
    client = bigquery.Client(credentials=credentials, project=gcp_info["project_id"])

    # Consulta SQL para apagar a tabela
    query = f"TRUNCATE TABLE `{project_id}.{dataset_id}.{table_id}`"
    query_job = client.query(query)
    query_job.result()
    print("Tabela truncada com sucesso!")
    return



def excluir_lancamento_sql(project_id, dataset_id, table_id, LOGIN, periodo, df_logins):
    # client = bigquery.Client(project=project_id)
    client = bigquery.Client(credentials=credentials, project=gcp_info["project_id"])

    # Recupera o nome completo baseado no login
    recuperar_nome = df_logins.loc[df_logins["LOGIN"] == LOGIN, "NOME_COMPLETO"].iloc[0]

    # Cria a query DELETE
    query = f"""
        DELETE FROM `{project_id}.{dataset_id}.{table_id}`
        WHERE TERCEIRIZADO = @terceirizado AND PERIODO = @periodo
    """

    # Configura os parâmetros
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("terceirizado", "STRING", recuperar_nome),
            bigquery.ScalarQueryParameter("periodo", "STRING", periodo),
        ]
    )

    # Executa a query
    query_job = client.query(query, job_config=job_config)
    query_job.result()

    print(f"Lançamento de {recuperar_nome} no período {periodo} foi excluído com sucesso (via SQL).")



def atualizar_lancamento_sql(project_id, dataset_id, table_id,
                              LOGIN, periodo_antigo,
                              novo_projeto, novo_periodo, novas_horas, novo_valor, pagamento_total,
                              df_logins):
    # Conecta ao BigQuery
    client = bigquery.Client(credentials=credentials, project=gcp_info["project_id"])

    # Recupera o nome completo a partir do login
    recuperar_nome = df_logins.loc[df_logins["LOGIN"] == LOGIN, "NOME_COMPLETO"].iloc[0]

    # Cria a query UPDATE
    query = f"""
        UPDATE `{project_id}.{dataset_id}.{table_id}`
        SET 
            PROJETO = @novo_projeto,
            PERIODO = @novo_periodo,
            HORAS_TOTAIS = @novas_horas,
            VALOR = @novo_valor,
            PAGAMENTO_TOTAL = @pagamento_total
        WHERE TERCEIRIZADO = @terceirizado AND PERIODO = @periodo_antigo
    """

    # Configura os parâmetros
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("novo_projeto", "STRING", novo_projeto),
            bigquery.ScalarQueryParameter("novo_periodo", "STRING", novo_periodo),
            bigquery.ScalarQueryParameter("novas_horas", "STRING", novas_horas),
            bigquery.ScalarQueryParameter("novo_valor", "FLOAT64", novo_valor),
            bigquery.ScalarQueryParameter("pagamento_total", "FLOAT64", pagamento_total),
            bigquery.ScalarQueryParameter("terceirizado", "STRING", recuperar_nome),
            bigquery.ScalarQueryParameter("periodo_antigo", "STRING", periodo_antigo),
        ]
    )

    # Executa a query
    query_job = client.query(query, job_config=job_config)
    query_job.result()

    print(f"Lançamento de {recuperar_nome} atualizado com sucesso!")



# Função para salvar a tabela em um único Excel com formatação
def salvar_excel_com_formatacao(bd):
    output = BytesIO()
    #=== Salvar em uma planilha em excel ===#
    # Crie uma nova planilha Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Pagamento"

    # # Remover as linhas de grade do Excel
    # ws.sheet_view.showGridLines = False

    # Define o estilo de preenchimento para o fundo do cabeçalho
    header_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

    # Define o alinhamento centralizado sem quebra de texto
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=False)

    # Define o alinhamento centralizado
    center_alignment = Alignment(horizontal="center", vertical="center")

    # Define o tamanho da fonte para todas as células
    font_size = Font(size=10)

    # Define a fonte em negrito
    bold_font = Font(bold=True, size=10)

    # Loop pelos DataFrames e escrevendo na planilha
    row_offset = 1  # Inicializa a contagem de linhas na planilha

    # Converter o DataFrame para linhas que o openpyxl pode usar
    rows = dataframe_to_rows(bd, index=False, header=True)

    # Define a borda fina
    borda_fina = Border(
        left=Side(border_style="thin", color="000000"),
        right=Side(border_style="thin", color="000000"),
        top=Side(border_style="thin", color="000000"),
        bottom=Side(border_style="thin", color="000000")
    )

    bd["PAGAMENTO_TOTAL"] = pd.to_numeric(bd["PAGAMENTO_TOTAL"], errors="coerce")
    
    # Escreve os dados no Excel
    for j, row in enumerate(rows):
        ws.append(row)

        # Itera sobre todas as colunas e aplica centralização
        for col in range(1, len(row) + 1):  # Itera sobre as colunas
            cell = ws.cell(row=row_offset + j, column=col)
            cell.alignment = center_alignment  # Aplica alinhamento centralizado
            cell.font = font_size # Aplica o tamanho da fonte de 10 para todas as células
            cell.border = borda_fina  # adiciona borda a todas as células

            # Estiliza apenas o cabeçalho
            if j == 0:  # Cabeçalhos do multiíndice
                cell.fill = header_fill
                cell.font = bold_font
                cell.alignment = header_alignment # Estiliza o cabeçalho com quebra de texto

        # Formata como porcentagem colunas 6 e 7
        if (j > 0):  # Dados (exclui os cabeçalhos)
            for col in range(6, 9):  # Colunas 6 e 7
                cell = ws.cell(row=row_offset + j, column=col)
                if isinstance(cell.value, (int, float)):  # Verifica se é número
                    cell.number_format = 'R$ #,##0.00'  # Formato moeda brasileira (R$)
                    cell.value = float(cell.value)  # Converte o valor para floats
    
    # Salvar o Workbook no buffer
    wb.save(output)
    return output.getvalue()


