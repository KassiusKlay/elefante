import streamlit as st
import pandas as pd
from utils import save_doc


def show(state):
    st.write('# Guardar Documento')

    if state.guardado is None:
        save_doc(state, pd.DataFrame())
    else:
        st.success(
                f'Documento guardado com '
                f'**ID {int(state.df.id.max())}**')
        novo = st.button('Novo Documento')
        if novo:
            state.guardado = None
    return
