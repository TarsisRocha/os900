# app/pages/login.py
import streamlit as st
from app.modules.auth import authenticate

def render():
    st.subheader("Login")
    u = st.text_input("Usuário")
    p = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if not u or not p:
            st.error("Preencha usuário e senha.")
            return
        ok = authenticate(u, p)
        if ok:
            st.session_state["logged_in"] = True
            st.session_state["username"] = u
            st.success("Logado.")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")
