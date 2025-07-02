import streamlit as st
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Autenticação
json_path = "C:\PROJETOS\Pagamento Terceirizado\pagamento-terceirizado-464719-cc762ff27770.json"
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


# # Autenticação
# credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
# client = gspread.authorize(credentials)

# Carregar credenciais do Streamlit Secrets
gcp_credentials = st.secrets["GCP_SERVICE_ACCOUNT"]

# Converter a string JSON em um dicionário Python
credentials_dict = json.loads(gcp_credentials)

# Criar credenciais a partir do dicionário JSON e Autenticar no Google Sheets
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(credentials)

PERIODO_1 = "06/05/2025 A 31/05/2025"
PERIODO_2 = "01/07/2025 A 19/07/2025"
