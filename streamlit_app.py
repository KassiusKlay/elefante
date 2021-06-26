import streamlit as st
import pandas as pd
from state import _get_state
import datetime


def main():
    state = _get_state()

    st.write('# Guardar Documento')

    linhas = st.number_input('Quantas entradas?', 1, step=1)

    df = pd.DataFrame(
            columns=['codigo', 'centro', 'valor', 'iva', 'total'])
    rows = list()

    codigos = ['1-1', '1-2']
    centros = ['Oeiras', 'Mem Martins']

    cols = st.beta_columns(2)
    state.mes = cols[0].selectbox(
            'Mes Referencia', range(1, 13),
            index=datetime.date.today().month)
    state.ano = cols[1].number_input(
            'Ano Referencia', value=datetime.date.today().year, step=1)

    for i in range(linhas):
        cols = st.beta_columns(5)
        codigo = cols[0].selectbox('Codigo', codigos, key=f'codigo_{i}')
        centro = cols[1].selectbox('Centro', centros, key=f'centro_{i}')
        valor = cols[2].text_input(
                'Valor S/IVA', value='', key=f'valor_{i}')
        if len(valor) > 0:
            try:
                valor = float(valor)
            except ValueError:
                st.warning('Valor tem de ser um numero')
                st.stop()
        iva = cols[3].text_input(
                'IVA', value='', key=f'iva_{i}')
        if len(iva) > 0:
            try:
                iva = float(iva)
            except ValueError:
                st.warning('IVA tem de ser um numero')
                st.stop()
        if valor and iva:
            total = valor + iva
            cols[4].write('Total')
            cols[4].write(total)
            rows.append([codigo, centro, valor, iva, total])

    st.write('Total Documento: ', sum(i[4] for i in rows))

    if len(rows) < linhas:
        st.warning('Entradas Incompletas')
    else:
        st.button('Guardar Documento')


if __name__ == '__main__':
    main()
