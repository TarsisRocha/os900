# app/modules/inventario_repo.py
import io
import pandas as pd
from app.modules.supabase_client import supabase
from app.modules.logs_repo import registrar_log

def get_machines_from_inventory():
    try:
        resp = supabase.table("inventario").select("*").execute()
        return resp.data or []
    except Exception as e:
        print(f"Erro get_machines_from_inventory: {e}")
        return []

def add_machine(payload: dict):
    try:
        supabase.table("inventario").insert(payload).execute()
        registrar_log(payload.get("usuario","sistema"), "add_machine", {"patrimonio": payload.get("numero_patrimonio")})
        return True
    except Exception as e:
        print(f"Erro add_machine: {e}")
        return False

def update_machine(patrimonio, new_values: dict):
    try:
        supabase.table("inventario").update(new_values).eq("numero_patrimonio", patrimonio).execute()
        registrar_log(new_values.get("usuario","sistema"), "update_machine", {"patrimonio": patrimonio})
        return True
    except Exception as e:
        print(f"Erro update_machine: {e}")
        return False

def delete_machine(patrimonio):
    try:
        supabase.table("inventario").delete().eq("numero_patrimonio", patrimonio).execute()
        registrar_log("sistema", "delete_machine", {"patrimonio": patrimonio})
        return True
    except Exception as e:
        print(f"Erro delete_machine: {e}")
        return False

def export_inventory_csv(df: pd.DataFrame):
    return df.to_csv(index=False).encode("utf-8")

def export_inventory_excel(df: pd.DataFrame):
    import io
    with io.BytesIO() as buffer:
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Inventario")
        return buffer.getvalue()
