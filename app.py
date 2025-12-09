import streamlit as st
from importlib import import_module

st.set_page_config(page_title="OS900 Modular", layout="wide")
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

st.markdown("<h1>OS900 - InfocusLoc (Modular)</h1>", unsafe_allow_html=True)

# Simple navbar
pages = {
    "Login": "app.pages.login",
    "Dashboard": "app.pages.dashboard",
    "Chamados": "app.pages.chamados_page",
    "Inventário": "app.pages.inventario_page",
    "Estoque": "app.pages.estoque_page",
    "Admin": "app.pages.admin_page",
}

menu = list(pages.keys())
choice = st.sidebar.selectbox("Menu", menu)

module_path = pages[choice]
try:
    mod = import_module(module_path)
    if hasattr(mod, "render"):
        mod.render()
    else:
        st.warning(f'Módulo {module_path} não implementa função render()')
except Exception as e:
    st.error(f"Erro ao carregar página {choice}: {e}")
