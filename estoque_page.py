# app/pages/estoque_page.py
import streamlit as st
import pandas as pd
from app.modules.estoque_repo import get_estoque, add_peca, dar_baixa_estoque, verificar_estoque_minimo

def render():
    st.title("Estoque")
    action = st.selectbox("Ação", ["Listar", "Adicionar", "Dar Baixa", "Verificar minimos"])
    if action == "Listar":
        data = get_estoque()
        if not data:
            st.info("Estoque vazio.")
            return
        st.dataframe(pd.DataFrame(data))
    elif action == "Adicionar":
        nome = st.text_input("Nome da Peça")
        qtd = st.number_input("Quantidade", min_value=0, step=1)
        desc = st.text_area("Descrição")
        if st.button("Adicionar"):
            if nome:
                add_peca(nome, int(qtd), desc)
                st.success("Peça adicionada.")
            else:
                st.error("Nome obrigatório.")
    elif action == "Dar Baixa":
        pecas = get_estoque()
        if not pecas:
            st.info("Estoque vazio.")
            return
        nomes = [p['nome'] for p in pecas]
        sel = st.selectbox("Peça", nomes)
        qtd = st.number_input("Quantidade a baixar", min_value=1, step=1)
        if st.button("Dar Baixa"):
            dar_baixa_estoque(sel, int(qtd))
            st.success("Baixa efetuada.")
    else:
        low = verificar_estoque_minimo()
        if not low:
            st.success("Nenhuma peça abaixo do mínimo.")
        else:
            st.dataframe(pd.DataFrame(low))
