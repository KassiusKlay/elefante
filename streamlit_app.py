import streamlit as st
from state import _get_state
import guardar
import consultar
import gerais
import db


def login(state):
    with st.sidebar.form(key='my_form'):
        user = st.text_input('Utilizador', '')
        password = st.text_input('Password', '', type='password')
        submit_button = st.form_submit_button(label='Entrar')
    if submit_button:
        if user == st.secrets['user'] and password == st.secrets['password']:
            state.login = True
        else:
            st.sidebar.warning('Utilizador / Password errados')
            st.stop()


def main():
    state = _get_state()

    if not state.login:
        login(state)
    else:
        dbx = db.get_dropbox_client()
        if state.df is None:
            try:
                state.df = db.download_dataframe(dbx, 'elefante', 'df.xlsx')
            except Exception:
                st.warning('Não foi possível extrair base de dados')
                st.stop()

        options = [
                'Guardar Documento',
                'Consultar Documento',
                'Consultar Gerais']

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
