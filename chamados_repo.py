# app/modules/chamados_repo.py
from datetime import datetime
from app.modules.supabase_client import supabase
from app.modules.logs_repo import registrar_log
from app.modules.sla_utils import calcular_sla as calcular_sla_fn

def gerar_protocolo_sequencial():
    try:
        resp = supabase.table("chamados").select("protocolo").execute()
        protocolos = [int(item["protocolo"]) for item in (resp.data or []) if item.get("protocolo")]
        return (max(protocolos) + 1) if protocolos else 1
    except Exception as e:
        print(f"Erro gerar_protocolo: {e}")
        return None

def add_chamado(username, ubs, setor, tipo_defeito, problema, patrimonio=None, machine=None):
    protocolo = gerar_protocolo_sequencial()
    if protocolo is None:
        return None
    hora_local = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data = {
        "username": username,
        "ubs": ubs,
        "setor": setor,
        "tipo_defeito": tipo_defeito,
        "problema": problema,
        "hora_abertura": hora_local,
        "protocolo": protocolo,
        "patrimonio": patrimonio,
        "machine": machine,
        "status_chamado": None,
        "peca_necessaria": None,
        "tecnico_responsavel": None
    }
    try:
        supabase.table("chamados").insert(data).execute()
        registrar_log(username, "abrir_chamado", {"protocolo": protocolo, "ubs": ubs})
        return protocolo
    except Exception as e:
        print(f"Erro add_chamado: {e}")
        return None

def list_chamados():
    try:
        resp = supabase.table("chamados").select("*").execute()
        return resp.data or []
    except Exception as e:
        print(f"Erro list_chamados: {e}")
        return []

def list_chamados_em_aberto():
    try:
        resp = supabase.table("chamados").select("*").is_("hora_fechamento", None).execute()
        return resp.data or []
    except Exception as e:
        print(f"Erro list_chamados_em_aberto: {e}")
        return []

def get_chamado_by_protocolo(protocolo):
    try:
        resp = supabase.table("chamados").select("*").eq("protocolo", protocolo).execute()
        return resp.data[0] if (resp.data and len(resp.data)>0) else None
    except Exception as e:
        print(f"Erro get_chamado_by_protocolo: {e}")
        return None

def atribuir_chamado(id_chamado, tecnico):
    try:
        supabase.table("chamados").update({"tecnico_responsavel": tecnico}).eq("id", id_chamado).execute()
        registrar_log(tecnico or "sistema", "atribuir_chamado", {"id": id_chamado})
        return True
    except Exception as e:
        print(f"Erro atribuir_chamado: {e}")
        return False

def marcar_aguardando_peca(id_chamado, peca=None, tecnico=None):
    try:
        supabase.table("chamados").update({
            "status_chamado": "Aguardando Peça",
            "peca_necessaria": peca,
            "tecnico_responsavel": tecnico
        }).eq("id", id_chamado).execute()
        registrar_log(tecnico or "sistema", "aguardando_peca", {"id": id_chamado, "peca": peca})
        return True
    except Exception as e:
        print(f"Erro marcar_aguardando_peca: {e}")
        return False

def limpar_status(id_chamado):
    try:
        supabase.table("chamados").update({
            "status_chamado": None,
            "peca_necessaria": None,
            "tecnico_responsavel": None
        }).eq("id", id_chamado).execute()
        registrar_log("sistema", "limpar_status", {"id": id_chamado})
        return True
    except Exception as e:
        print(f"Erro limpar_status: {e}")
        return False

def finalizar_chamado(id_chamado, solucao, pecas_usadas=None):
    try:
        hora_fechamento = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        supabase.table("chamados").update({
            "solucao": solucao,
            "hora_fechamento": hora_fechamento,
            "status_chamado": None,
            "peca_necessaria": None,
            "tecnico_responsavel": None
        }).eq("id", id_chamado).execute()

        if pecas_usadas:
            for p in pecas_usadas:
                supabase.table("pecas_usadas").insert({
                    "chamado_id": id_chamado,
                    "peca_nome": p,
                    "data_uso": hora_fechamento
                }).execute()
        registrar_log("sistema", "finalizar_chamado", {"id": id_chamado})
        return True
    except Exception as e:
        print(f"Erro finalizar_chamado: {e}")
        return False

def calcular_sla_do_chamado(chamado):
    return calcular_sla_fn(chamado)
