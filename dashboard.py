# app/pages/dashboard.py
import streamlit as st
import pandas as pd
from app.modules.chamados_repo import list_chamados, list_chamados_em_aberto, calcular_sla_do_chamado
from app.modules.ubs_repo import get_ubs_list

def render():
    st.title("Dashboard - OS900")
    chamados = list_chamados()
    if not chamados:
        st.info("Nenhum chamado registrado.")
        return
    df = pd.DataFrame(chamados)
    st.metric("Total Chamados", len(df))
    if 'hora_fechamento' in df.columns:
        st.metric("Em Aberto", int(df['hora_fechamento'].isna().sum()))
    st.markdown('---')
    st.markdown("### Chamados recentes")
    st.dataframe(df.sort_values(by='hora_abertura', ascending=False).head(30))
    st.markdown('---')
    st.markdown("### Chamados em aberto (SLA)")
    abertos = list_chamados_em_aberto()
    sla_rows = []
    for c in abertos:
        sla = calcular_sla_do_chamado(c)
        sla_rows.append({"protocolo": c.get("protocolo"), "ubs": c.get("ubs"), "status_sla": sla.get("status"), "horas_uteis": sla.get("horas_uteis")})
    if sla_rows:
        st.dataframe(pd.DataFrame(sla_rows))
    else:
        st.write("Nenhum aberto.")
