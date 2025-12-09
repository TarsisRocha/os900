# app/modules/ubs_repo.py
from app.modules.supabase_client import supabase

def get_ubs_list():
    try:
        resp = supabase.table("ubs").select("nome_ubs").execute()
        return [u["nome_ubs"] for u in (resp.data or [])]
    except Exception as e:
        print(f"Erro get_ubs_list: {e}")
        return []

def add_ubs(nome_ubs):
    try:
        supabase.table("ubs").insert({"nome_ubs": nome_ubs}).execute()
        return True
    except Exception as e:
        print(f"Erro add_ubs: {e}")
        return False
