import streamlit as st
from utils import show_doc, save_doc


def show(state):
    st.write('# Consultar Documento')
    if state.df.empty:
        st.warning('Não há ficheiros guardados')
        st.stop()

    cols = st.beta_columns(3)
    doc_id = cols[0].number_input(
            'ID',
            min_value=int(state.df.id.min()),
            max_value=int(state.df.id.max()),
            step=1)
    df = state.df.loc[state.df.id == doc_id].reset_index(drop=True)
    show_doc(df)
    placeholder = st.empty()
    alterar = placeholder.button('Alterar Documento?')
    if alterar:
        state.alterar = True
        state.guardado = None
    if state.alterar:
        cancelar = placeholder.button('Cancelar Alteração')
        if cancelar:
            state.alterar = None
        save_doc(state, df)
        if state.guardado:
            state.alterar = None
            state.guardado = None
