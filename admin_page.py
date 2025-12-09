# app/pages/admin_page.py
import streamlit as st
from app.modules.auth import list_users, add_user, is_admin, force_change_password
from app.modules.ubs_repo import get_ubs_list, add_ubs
from app.modules.setores_repo import get_setores_list, add_setor

def render():
    st.title("Administração")
    st.subheader("Usuários")
    if st.button("Listar usuários"):
        st.write(list_users())
    with st.expander("Criar usuário"):
        u = st.text_input("Usuário (novo)")
        p = st.text_input("Senha", type="password")
        admin = st.checkbox("É admin?")
        if st.button("Criar usuário"):
            if u and p:
                ok = add_user(u, p, is_admin=admin)
                if ok:
                    st.success("Usuário criado.")
                else:
                    st.error("Falha ao criar (já existe?).")
    st.subheader("UBS / Setores")
    if st.button("Listar UBS"):
        st.write(get_ubs_list())
    if st.button("Listar Setores"):
        st.write(get_setores_list())
