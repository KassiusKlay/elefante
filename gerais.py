import streamlit as st
import pandas as pd
from utils import show_gerais


centros = [
        'Oeiras', 'Mem Martins', 'Maia', 'São João da Talha',
        'Alverca', 'Comuns']


def Insert_row_(row_number, df, row_value):
    df1 = df[0:row_number]
    df2 = df[row_number:]
    df1 = df1.append(row_value)
    df_result = pd.concat([df1, df2])
    return df_result


def show(state):
    st.write('# Consultar Gerais')
    cols = st.beta_columns(2)
    mes = cols[0].number_input(
            'Mes',
            state.teste.data.dt.month.min(),
            state.teste.data.dt.month.max(),
            step=1)
    ano = cols[1].number_input(
            'Ano',
            state.teste.data.dt.year.min(),
            state.teste.data.dt.year.max(),
            step=1)

    df = state.teste.loc[
            (state.teste.data.dt.month == mes) &
            (state.teste.data.dt.year == ano)]
    if df.empty:
        st.warning('Sem entradas para a data especificada')
        st.stop()

    iva = df.groupby('id').agg({'iva': 'max'}).sum()[0]
    df = df.drop(['id', 'data'], axis=1)
    df = df.pivot_table(index='codigo', columns='centro', values='valor')
    df.columns = [i for i in centros if i in df.columns]
    df['Total'] = df.sum(axis=1)
    total_despesas = pd.DataFrame(columns=df.columns)
    for i in ['1', '2', '3', '4']:
        teste = df.loc[df.index.str.startswith(i)]
        if teste.empty:
            continue
        if i == '4' and not total_despesas.empty:
            total_despesas = total_despesas.sum()
            total_despesas.name = 'TOTAL DESPESAS'
            index = df.index.get_loc(teste.iloc[0].name)
            df = Insert_row_(index, df, total_despesas.transpose())
        soma = teste.sum()
        soma.name = f'Despesas-{i}'
        if i != '4':
            total_despesas = total_despesas.append(soma.transpose())
        index = df.index.get_loc(teste.iloc[-1].name)
        df = Insert_row_(index + 1, df, soma.transpose())
    iva_row = pd.Series(iva, index=['Total'], name='IVA')
    df = df.append(iva_row)

    show_gerais(df)
