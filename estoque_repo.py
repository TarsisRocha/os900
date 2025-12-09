# app/modules/estoque_repo.py
from datetime import datetime
from app.modules.supabase_client import supabase
from app.modules.logs_repo import registrar_log

def get_estoque():
    try:
        resp = supabase.table("estoque").select("*").execute()
        return resp.data or []
    except Exception as e:
        print(f"Erro get_estoque: {e}")
        return []

def add_peca(nome, quantidade, descricao="", nota_fiscal=None):
    try:
        data = {
            "nome": nome,
            "quantidade": quantidade,
            "descricao": descricao,
            "nota_fiscal": nota_fiscal,
            "data_adicao": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        supabase.table("estoque").insert(data).execute()
        registrar_log("sistema", "add_peca", {"nome": nome, "qtd": quantidade})
        return True
    except Exception as e:
        print(f"Erro add_peca: {e}")
        return False

def update_peca(id_peca, new_values: dict):
    try:
        supabase.table("estoque").update(new_values).eq("id", id_peca).execute()
        registrar_log("sistema", "update_peca", {"id": id_peca})
        return True
    except Exception as e:
        print(f"Erro update_peca: {e}")
        return False

def dar_baixa_estoque(peca_nome, quantidade_usada=1):
    try:
        resp = supabase.table("estoque").select("*").eq("nome", peca_nome).execute()
        if not resp.data:
            return False
        item = resp.data[0]
        nova = max(0, int(item.get("quantidade",0)) - int(quantidade_usada))
        supabase.table("estoque").update({"quantidade": nova}).eq("id", item["id"]).execute()
        registrar_log("sistema", "dar_baixa", {"nome": peca_nome, "quantia": quantidade_usada})
        return True
    except Exception as e:
        print(f"Erro dar_baixa_estoque: {e}")
        return False

def verificar_estoque_minimo(limite=3):
    try:
        resp = supabase.table("estoque").select("*").lte("quantidade", limite).execute()
        return resp.data or []
    except Exception as e:
        print(f"Erro verificar_estoque_minimo: {e}")
        return []
