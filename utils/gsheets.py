# utils/gsheets.py
import os, json, gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def get_client():
    # Lê o JSON da service account da env var GCP_SA_JSON
    info = json.loads(os.environ["GCP_SA_JSON"])
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return gspread.authorize(creds)
