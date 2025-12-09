# app/modules/sla_utils.py
from datetime import datetime, timedelta, time
import pytz

FORTALEZA_TZ = pytz.timezone("America/Fortaleza")

def calculate_working_hours(start: datetime, end: datetime) -> timedelta:
    if start.tzinfo is None:
        start = FORTALEZA_TZ.localize(start)
    if end.tzinfo is None:
        end = FORTALEZA_TZ.localize(end)
    if end < start:
        return timedelta(0)
    work_start = time(8,0,0)
    work_end = time(18,0,0)
    total = timedelta(0)
    cur = start
    while cur.date() <= end.date():
        if cur.weekday() < 5:
            day_start = datetime.combine(cur.date(), work_start).replace(tzinfo=FORTALEZA_TZ)
            day_end = datetime.combine(cur.date(), work_end).replace(tzinfo=FORTALEZA_TZ)
            seg = max(day_start, start)
            end_seg = min(day_end, end)
            if end_seg > seg:
                total += (end_seg - seg)
        cur = (cur + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return total

def calcular_sla(chamado: dict, sla_hours: int = 48) -> dict:
    try:
        formato = "%d/%m/%Y %H:%M:%S"
        abertura = datetime.strptime(chamado.get("hora_abertura"), formato)
        fechamento = None
        if chamado.get("hora_fechamento"):
            fechamento = datetime.strptime(chamado.get("hora_fechamento"), formato)
        agora = datetime.now(FORTALEZA_TZ).replace(tzinfo=None)
        delta = calculate_working_hours(abertura, fechamento or agora)
        horas = delta.total_seconds() / 3600.0
        if horas <= sla_hours * 0.75:
            status = "OK"
        elif horas <= sla_hours:
            status = "ATENCAO"
        else:
            status = "VIOLADO"
        return {"horas_uteis": round(horas,2), "status": status}
    except Exception:
        return {"horas_uteis": None, "status": "UNKNOWN"}
