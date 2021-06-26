import streamlit as st
import pandas as pd
import datetime


def show(state):
    st.write('# Consultar Documento')

    st.write(state.df)

    doc_id = st.number_input(
            'ID',
            min_value=state.df.id.min(),
            max_value=state.df.id.max(),
            step=1)
    st.write(state.df.loc[state.df.id == doc_id])

