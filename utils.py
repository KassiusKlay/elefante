import streamlit as st
import pandas as pd
import datetime
import math


codigos = ['1-1', '1-2']
centros = ['Oeiras', 'Mem Martins']


def show_doc(df):
    df = df.drop('id', axis=1)
    styler = df.style.format({
        "data": lambda x: x.strftime('%m-%Y'),
        'valor': lambda x: '{:.2f}'.format(x),
        'iva': lambda x: '{:.2f}'.format(x),
        'total': lambda x: '{:.2f}'.format(x)})
    st.write(styler)


def save_doc(state, df):
    linhas_default = 1 if df.empty else len(df)
    mes_default = (
            datetime.date.today().month - 1 if df.empty
            else int(df.data.dt.month.unique()[0] - 1))
    ano_default = (
            datetime.date.today().year if df.empty
            else df.data.dt.year.unique()[0])
    linhas = st.number_input(
            'Quantas entradas?', min_value=1, value=linhas_default,
            step=1, key='linhas')

    if df.empty:
        codigos_default = centros_default = [0] * linhas
        valores_default = [''] * linhas
        iva_default = '0'
        df = pd.DataFrame(
                columns=['id', 'data', 'codigo', 'centro', 'valor', 'iva'])
        for i in range(linhas):
            df.loc[i] = [float('Nan')] * 6
    else:
        df = df.iloc[:linhas]
        for i in range(linhas):
            if i < len(df):
                codigos_default = [codigos.index(i) for i in df.codigo]
                centros_default = [centros.index(i) for i in df.centro]
                valores_default = [i for i in df.valor]
            else:
                codigos_default.append(0)
                centros_default.append(0)
                valores_default.append('')
        iva_default = df.iva.unique()[0]
    total_sem_iva = 0
    total_documento = 0

    cols = st.beta_columns(2)
    mes = cols[0].selectbox(
            'Mes Referência', range(1, 13),
            index=mes_default, key='mes')
    ano = cols[1].number_input(
            'Ano Referência', value=ano_default, step=1, key='ano')
    data = pd.to_datetime(str(ano) + str(mes), format='%Y%m')

    for i in range(linhas):
        cols = st.beta_columns(3)
        codigo = cols[0].selectbox(
                'Codigo',
                codigos,
                index=codigos_default[i],
                key=f'codigo_{i}')
        centro = cols[1].selectbox(
                'Centro',
                centros,
                index=centros_default[i],
                key=f'centro_{i}')
        valor = cols[2].text_input(
                'Valor S/IVA',
                value=valores_default[i],
                key=f'valor_{i}')
        if len(valor) == 0:
            valor = float('Nan')
        else:
            try:
                valor = float(valor)
                total_sem_iva += valor
            except ValueError:
                st.warning('Valor tem de ser numérico')
                st.stop()
        df.at[i, ['codigo', 'centro', 'valor']] = [codigo, centro, valor]

    cols = st.beta_columns(5)
    iva = cols[0].text_input(
            'Total IVA',
            value=iva_default,
            key='iva')
    if len(iva) == 0:
        iva = float('Nan')
    else:
        try:
            iva = float(iva)
        except ValueError:
            st.warning('Valor tem de ser numérico')
            st.stop()
    total_documento = total_sem_iva + iva
    st.write('### Total Documento', total_documento)

    df.data = data
    df.iva = iva
    if all(df.id.isna()):
        df.id.fillna(
                1 if state.df.empty
                else state.df.id.max() + 1,
                inplace=True)
    else:
        df.id = df.id.unique()[0]

    if not math.isnan(total_documento):
        st.write('### Documento')
        show_doc(df)
        placeholder = st.empty()
        guardar = placeholder.button('Guardar Documento')
        if guardar:
            if not state.df.empty:
                state.df = state.df.loc[~state.df.id.isin(df.id.unique())]
            state.df = pd.concat(
                    [state.df, df]
                    ).drop_duplicates().reset_index(drop=True)
            state.guardado = True
