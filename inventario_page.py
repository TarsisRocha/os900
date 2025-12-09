# app/pages/inventario_page.py
import streamlit as st
import pandas as pd
from app.modules.inventario_repo import get_machines_from_inventory, export_inventory_csv, export_inventory_excel

def render():
    st.title("Inventário")
    machines = get_machines_from_inventory()
    if not machines:
        st.info("Nenhum item no inventário.")
        return
    df = pd.DataFrame(machines)
    st.dataframe(df)
    st.markdown('---')
    if st.button("Exportar CSV"):
        csv = export_inventory_csv(df)
        st.download_button("Download CSV", csv, file_name="inventario.csv", mime="text/csv")
    try:
        excel = export_inventory_excel(df)
        st.download_button("Download Excel", excel, file_name="inventario.xlsx", mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception:
        st.info("Instale openpyxl para exportar Excel.")
