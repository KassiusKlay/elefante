import streamlit as st
from state import _get_state
import guardar
import consultar
import gerais


def main():
    state = _get_state()

    options = ['Guardar Documento', 'Consultar Documento', 'Consultar Gerais']

    option = st.sidebar.radio('', options)

    if option == 'Guardar Documento':
        guardar.show(state)
    elif option == 'Consultar Documento':
        consultar.show(state)
    else:
        gerais.show(state)



if __name__ == '__main__':
    main()
