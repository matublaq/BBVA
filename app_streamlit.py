import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit.components.v1 as components

# Page configuration
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .main {
        max-width: 100%;
        padding-left: 0;
        padding-right: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("<h1 style='font-size: 50px; text-align: center; color: #E5E1DA'>Petición</p>", unsafe_allow_html=True)
st.markdown('''
    <p style='font-size: 30px;'>Datos necesatios:</p>
    <p style='text-align: center; font-size: 20px;'>petition_code, DQDP_code, sdatool, feature, UUAA, geography_id, petition_arq, estado, fecha_in, fecha_out, time_duration, descripcion</p>
    ''',unsafe_allow_html=True)

st.markdown('---')

with st.form(key='petition_form'):

    col1, col2 = st.columns(2)
    with col1: 
        estado = st.selectbox('Estado', ['Pendiente', 'En Proceso', 'Finalizado'])  
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            UUAA = st.text_input('UUAA')
            fecha_in = st.date_input('Fecha In')
            timer_duration = st.number_input('Time Duration', min_value=0.5, max_value=20.0, step=0.5, value=1.0)
        with col1_2:
            geography_id = st.text_input('Geography ID')
            fecha_out = st.date_input('Fecha Out')
            time_duration = st.slider('Time Duration', min_value=0.0, max_value=20.0, step=0.5, value=1.0)
        
    with col2:
        petition_code = st.text_input('Petition Code')
        col2_1, col2_2 = st.columns(2)
        with col2_1: 
            sdatool = st.text_input('SDA Tool')
        with col2_2:
            feature = st.text_input('Feature')
        DQDP_code = st.text_input('DQDP Code')
        petition_arq = st.text_input('Petition ARQ')
        
        

    descripcion = st.text_area('Descripción')

    # Botón para enviar el formulario
    submit_button = st.form_submit_button(label='Enviar')

# Procesar los datos del formulario
if submit_button:
    st.write('Petition Code:', petition_code)
    st.write('DQDP Code:', DQDP_code)
    st.write('SDA Tool:', sdatool)
    st.write('Feature:', feature)
    st.write('UUAA:', UUAA)
    st.write('Geography ID:', geography_id)
    st.write('Petition ARQ:', petition_arq)
    st.write('Estado:', estado)
    st.write('Fecha In:', fecha_in)
    st.write('Fecha Out:', fecha_out)
    st.write('Time Duration:', time_duration)
    st.write('Descripción:', descripcion)
