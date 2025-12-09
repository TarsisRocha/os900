# app/pages/chamados_page.py
import streamlit as st
from app.modules.chamados_repo import add_chamado, list_chamados_em_aberto, get_chamado_by_protocolo, finalizar_chamado, marcar_aguardando_peca
from app.modules.ubs_repo import get_ubs_list
from app.modules.setores_repo import get_setores_list

def render():
    st.title("Chamados")
    tab = st.tabs(["Abrir Chamado","Lista / Ações"])
    with tab[0]:
        usuario = st.session_state.get("username","anon")
        patrimonio = st.text_input("Patrimônio (opcional)")
        ubs = st.selectbox("UBS", ["-"] + get_ubs_list())
        setor = st.selectbox("Setor", ["-"] + get_setores_list())
        tipo = st.selectbox("Tipo de Defeito", ["Computador não liga","Impressora não imprime","Outro"])
        problema = st.text_area("Descrição")
        if st.button("Abrir Chamado"):
            protocolo = add_chamado(usuario, ubs if ubs!="- " else None, setor if setor!="- " else None, tipo, problema, patrimonio or None)
            if protocolo:
                st.success(f"Chamado aberto: {protocolo}")
            else:
                st.error("Erro ao abrir chamado.")
    with tab[1]:
        st.subheader("Chamados em aberto")
        abertos = list_chamados_em_aberto()
        if not abertos:
            st.info("Nenhum em aberto.")
            return
        protocolos = [str(c.get("protocolo")) for c in abertos]
        sel = st.selectbox("Protocolo", protocolos)
        if sel:
            chamado = get_chamado_by_protocolo(sel)
            st.write(chamado)
            if st.button("Finalizar chamado"):
                ok = finalizar_chamado(chamado.get("id"), "Resolvido via app", pecas_usadas=[])
                if ok:
                    st.success("Finalizado.")
            if st.button("Marcar aguardando peça"):
                marcar_aguardando_peca(chamado.get("id"), peca=None, tecnico=st.session_state.get("username"))
                st.success("Marcado como aguardando peça.")
