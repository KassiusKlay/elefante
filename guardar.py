import streamlit as st
import pandas as pd
import datetime
import math
from utils import show_doc, save_doc


def guardar_doc(state):
    linhas = st.number_input('Quantas entradas?', 1, step=1)

    df = pd.DataFrame(
            columns=['codigo', 'centro', 'valor'])
    total_sem_iva = 0
    total_documento = 0
    codigos = ['1-1', '1-2']
    centros = ['Oeiras', 'Mem Martins']

    cols = st.beta_columns(2)
    mes = cols[0].selectbox(
            'Mes Referencia', range(1, 13),
            index=datetime.date.today().month)
    ano = cols[1].number_input(
            'Ano Referencia', value=datetime.date.today().year, step=1)
    data = pd.to_datetime(str(ano) + str(mes), format='%Y%m')

    for i in range(linhas):
        cols = st.beta_columns(3)
        codigo = cols[0].selectbox('Codigo', codigos, key=f'codigo_{i}')
        centro = cols[1].selectbox('Centro', centros, key=f'centro_{i}')
        valor = cols[2].text_input(
                'Valor S/IVA', value='', key=f'valor_{i}')
        if len(valor) == 0:
            valor = float('Nan')
        else:
            try:
                valor = float(valor)
                total_sem_iva += valor
            except ValueError:
                st.warning('Valor tem de ser um numero')
                st.stop()
        df.loc[len(df)] = [codigo, centro, valor]

    st.write('### Total Documento')
    cols = st.beta_columns(5)
    iva = cols[0].text_input('Total IVA')
    if len(iva) == 0:
        iva = float('Nan')
    else:
        try:
            iva = float(iva)
        except ValueError:
            st.warning('IVA tem de ser um numero')
            st.stop()
    total_documento = total_sem_iva + iva
    st.write('Total:', total_documento)

    df['data'] = data
    df['iva'] = iva
    df = df[['data', 'codigo', 'centro', 'valor', 'iva']]
    if not math.isnan(total_documento):
        st.write('### Documento')
        show_doc(df)

        placeholder = st.empty()
        guardar = placeholder.button('Guardar Documento')
        if guardar:
            state.df = pd.concat([state.df, df])
            state.df.id.fillna(
                    1 if all(state.df.id.isna())
                    else state.df.id.max() + 1,
                    inplace=True)
            st.write(state.df)
            state.guardado = True


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
