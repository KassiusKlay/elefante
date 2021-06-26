import streamlit as st
import pandas as pd
import datetime


def show(state):
    st.write('# Guardar Documento')

    linhas = st.number_input('Quantas entradas?', 1, step=1)

    df = pd.DataFrame(
            columns=['data', 'codigo', 'centro', 'valor', 'iva', 'total'])

    if state.df is None:
        state.df = df
        state.df.insert(loc=0, column='id', value=0)

    total_sem_iva = 0
    total_iva = 0
    total_documento = 0
    rows = list()
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
        total = 0
        cols = st.beta_columns(5)
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
                total += valor
            except ValueError:
                st.warning('Valor tem de ser um numero')
                st.stop()
        iva = cols[3].text_input(
                'IVA', value='', key=f'iva_{i}')
        if len(iva) == 0:
            iva = float('Nan')
        else:
            try:
                iva = float(iva)
                total_iva += iva
                total += iva
            except ValueError:
                st.warning('IVA tem de ser um numero')
                st.stop()
        cols[4].write('Total')
        cols[4].write(total)
        if all([data, codigo, centro, valor, iva, total]):
            rows.append([data, codigo, centro, valor, iva, total])

    st.write('### Total Documento')
    st.write('IVA:', total_iva)
    total_documento = total_sem_iva + total_iva
    st.write('Total:', total_documento)

    if len(rows) < linhas:
        st.warning('Entradas Incompletas')
    else:
        st.write('### Documento')
        for i in rows:
            df.loc[len(df)] = i
        styler = df.style.format({
            "data": lambda x: x.strftime('%m-%Y'),
            'valor': lambda x: '{:.2f}'.format(x),
            'iva': lambda x: '{:.2f}'.format(x),
            'total': lambda x: '{:.2f}'.format(x)})
        st.write(styler)

        placeholder = st.empty()
        guardar = placeholder.button('Guardar Documento')
        if guardar:
            state.df = pd.concat([state.df, df])
            state.df.id.fillna(
                    1 if all(state.df.id.isna())
                    else state.df.id.max() + 1,
                    inplace=True)

            placeholder.success(
                    f'Documento guardado com '
                    f'**ID {int(state.df.id.max())}**')
            st.write(state.df)
