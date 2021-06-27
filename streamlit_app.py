import streamlit as st
from state import _get_state
import guardar
import consultar
import gerais
import db


def main():
    state = _get_state()

    dbx = db.get_dropbox_client()
    if state.df is None:
        try:
            state.df = db.download_dataframe(dbx, 'elefante', 'df.xlsx')
        except Exception:
            st.warning('Não foi possível extrair base de dados')
            st.stop()

    if state.teste is None:
        state.teste = db.download_dataframe(dbx, 'elefante', 'teste.xlsx')

    options = ['Guardar Documento', 'Consultar Documento', 'Consultar Gerais']

    option = st.sidebar.radio('', options)

    if option == 'Guardar Documento':
        guardar.show(state)
    elif option == 'Consultar Documento':
        consultar.show(state)
    else:
        gerais.show(state)

    state.sync()


if __name__ == '__main__':
    main()
