# app/modules/setores_repo.py
from app.modules.supabase_client import supabase

def get_setores_list():
    try:
        resp = supabase.table("setores").select("nome_setor").execute()
        return [s["nome_setor"] for s in (resp.data or [])]
    except Exception as e:
        print(f"Erro get_setores_list: {e}")
        return []

def add_setor(nome):
    try:
        supabase.table("setores").insert({"nome_setor": nome}).execute()
        return True
    except Exception as e:
        print(f"Erro add_setor: {e}")
        return False
