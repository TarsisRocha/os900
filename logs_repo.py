# app/modules/logs_repo.py
import json
from datetime import datetime
from app.modules.supabase_client import supabase

def registrar_log(usuario: str, acao: str, detalhes: dict = None):
    try:
        payload = {
            "usuario": usuario,
            "acao": acao,
            "detalhes": json.dumps(detalhes or {}),
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        supabase.table("logs").insert(payload).execute()
    except Exception as e:
        print(f"Erro registrar_log: {e}")
