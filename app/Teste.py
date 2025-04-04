import os
from google.cloud import bigquery
import pandas as pd
# from Funcoes import ler_tabela, incluir_login

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\PROJETOS\Pagamento Terceirizado\Ignorar\pagamento-terceirizado-467d410b51b5.json"

# Nome do projeto, dataset e tabela
project_id = "pagamento-terceirizado"
dataset_id = "pagamento_terceirizado"
table_id = "horas_colaborador"

# # Inicializa o cliente
# client = bigquery.Client(project=project_id)

# # Consulta SQL para ler a tabela
# query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
# df = client.query(query).to_dataframe()
# # Exibe os dados
# print(df)


# # DataFrame com dados novos
# novos_dados = pd.DataFrame({
#     "TERCEIRIZADO": ["ANDREIA GONZAGA DOS SANTOS"],
#     "SERVICO": ["MONITORIA"],
#     "DESCRICAO": ["EXAME DE DADOS"],
#     "PROJETO": ["Cielo NPS"],
#     "PERIODO": ["17/02/2025 A 16/03/2025"],
#     "HORAS": ["160:36:00"],
#     "VALOR": [15.00],
#     "TOTAL": [2409.00],
#     "QUEM EMITE A NF": ["MEI"],
#     "OBSERVACAO": [""]
# })

# # Define a tabela completa
# tabela_destino = f"{project_id}.{dataset_id}.{table_id}"

# # Insere no modo append
# job = client.load_table_from_dataframe(novos_dados, tabela_destino)
# job.result()  # Espera o job terminar
# print("Dados inseridos com sucesso!")

# # Consulta SQL para ler a tabela
# query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
# df = client.query(query).to_dataframe()
# print(f'banco:\n{df}')

# # Consulta SQL para apagar a tabela
# query = f"TRUNCATE TABLE `{project_id}.{dataset_id}.{table_id}`"
# query_job = client.query(query)
# query_job.result()
# print("Tabela truncada com sucesso!")

# # Consulta SQL para ler a tabela
# query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
# df = client.query(query).to_dataframe()
# print(f'banco:\n{df}')


# incluir_login(project_id = "pagamento-terceirizado",
#               dataset_id = "pagamento_terceirizado",
#               table_id = "login_colaborador", 
#               LOGIN="admin", SENHA="Exp2025$", NOME_COMPLETO="ADMINISTRADOR")

HORAS = '160:36:00'
VALOR = '15,00'
VALOR = float(VALOR.replace(",", "."))
print(f'VALOR:\t{VALOR}')

only_hour = HORAS.split(":")[0]
print(f'only_hour:\t{only_hour}')
only_min = HORAS.split(":")[1]
print(f'only_min:\t{only_min}')
min_para_calculo = int(int(only_min) * 100 / 60)
print(f'min_para_calculo:\t{min_para_calculo}')
total_horas_trabalhadas = float(only_hour + "." + str(min_para_calculo))
print(f'total_horas_trabalhadas:\t{total_horas_trabalhadas}')
TOTAL = total_horas_trabalhadas * VALOR
print(f'TOTAL:\t{TOTAL}')

df = pd.DataFrame({
    "LOGIN": ['andreia.goncalves', 'alice.ribeiro', 'joao.silva', 'andreia.goncalves'],
    "SENHA": ['123', '123', '123', '123'],
    "NOME_COMPLETO": ['ANDREIA GONCALVES', 'ALICE RIBEIRO', 'JOAO SILVA', 'ANDREIA GONCALVES'],
    "PAGAMENTO_TOTAL": [780.00, 1090.00, 1530.00, 647.00]
})

recuperar_nome = df.loc[df["LOGIN"] == 'andreia.goncalves', "NOME_COMPLETO"]
recuperar_nome = recuperar_nome.iloc[0]
print(f'\nnome: {recuperar_nome}')

recuperar_pagamento = df.loc[df["NOME_COMPLETO"] == recuperar_nome, "PAGAMENTO_TOTAL"]
recuperar_pagamento = recuperar_pagamento.iloc[-1]
print(f'\nrecuperar_pagamento:\n{recuperar_pagamento}')

# new_df = df.loc[df["LOGIN"] == 'andreia.goncalves']
# print(f'\nnew_df\n{new_df}')

# from datetime import datetime 
# print(datetime.now().date())