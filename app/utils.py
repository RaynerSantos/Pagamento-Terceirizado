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

PERIODO_1 = "01/07/2025 A 19/07/2025"
PERIODO_2 = "11/08/2025 A 05/09/2025"

PROJETOS = [
            # "1.217-1 CIELO/CP/SATISFAÇÃO 1ª ONDA_2025",
                # "1.217-2 CIELO/CP/SATISFAÇÃO 2ª ONDA_2025",
            #    "1.217-3 CIELO/CP/SATISFAÇÃO 3ª ONDA_2025",
            #    "1.216-1 CIELO/CP/TRACKING NPS MENSAL 1ª ONDA_2025"
            #    "1.216-2 CIELO/CP/TRACKING NPS MENSAL 2ª ONDA_2025",
            #    "1.216-3 CIELO/CP/TRACKING NPS MENSAL 3ª ONDA_2025",
            #    "1.216-4 CIELO/CP/TRACKING NPS MENSAL 4ª ONDA_2025",
            #    "1.216-5 CIELO/CP/TRACKING NPS MENSAL 5ª ONDA_2025",
               "1.216-6 CIELO/CP/TRACKING NPS MENSAL 6ª ONDA_2025",
            #    "1.216-7 CIELO/CP/TRACKING NPS MENSAL 7ª ONDA_2025",
            #    "1.216-8 CIELO/CP/TRACKING NPS MENSAL 8ª ONDA_2025",
            #    "1.216-9 CIELO/CP/TRACKING NPS MENSAL 9ª ONDA_2025"
                ]
