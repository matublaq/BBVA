import numpy as np
import pandas as pd
import sqlite3

import streamlit as st
import streamlit.components.v1 as components

from DataBase_functions import *
from DataBase_functions_testing import *

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
st.markdown('---')

with st.form(key='petition_info'):

    col1, col2 = st.columns(2)
    with col1: # Petition table
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            estado = st.selectbox('Estado', ['Pendiente', 'En Proceso', 'Finalizado'])
            petition_code = st.text_input('Petition Code (CHAR 64)')
            sdatool = st.text_input('SDA Tool (CHAR 64)')
            fecha_in = st.date_input('Fecha In')
            duration_time = st.number_input('Time Duration', min_value=0.5, max_value=20.0, step=0.5, value=1.0)
        with col1_2:
            DQDP_code = st.text_input('DQDP Code (CHAR 64)')
            petition_arq = st.text_input('Petition ARQ (CHAR 64)')
            feature = st.text_input('Feature (CHAR 64)')
            fecha_out = st.date_input('Fecha Out')
            duration_time = st.slider('Time Duration', min_value=0.0, max_value=20.0, step=0.5, value=1.0)

    with col2: # Petition_PWD table
        DDBB = st.selectbox('DDBB', ['Oracle Physics', 'Oracle R2', 'Elasticsearch', 'Mongo DB', 'PostgreSQL'])
        col2_1a, col2_2a, col2_3a = st.columns(3)
        with col2_1a: 
            UUAA = st.text_input('UUAA (CHAR 4)')
        with col2_2a:
            geography = st.selectbox('Geography', ['Argentina', 'Global', 'Spain', 'Holding'])
        with col2_3a:
            dev_master = st.selectbox('Dev Master', ['Dev', 'Master', 'None'])
        
        col2_1b, col2_2b = st.columns([1, 2])
        with col2_1b:
            version_date = st.date_input('Fecha de la versión')
        with col2_2b:
            version = st.text_input('Version + desc (CHAR 64). Ej: v1 dev + Posible master v1')
        descripcion = st.text_area('Descripción')
        

    

    # Botón para enviar el formulario
    submit_button = st.form_submit_button(label='Enviar')

# Procesar los datos del formulario
if submit_button:
    st.write('Petition Code:', petition_code.strip().upper())
    st.write('DQDP Code:', DQDP_code.strip().upper())
    st.write('SDA Tool:', sdatool.strip().upper())
    st.write('Feature:', feature.strip().upper())
    st.write('UUAA:', UUAA.strip().upper())
    st.write('Geography:', geography)
    st.write('DDBB:', DDBB)
    st.write('Dev Master:', dev_master)
    st.write('Version:', version)
    st.write('Petition ARQ:', petition_arq.strip().upper())
    st.write('Estado:', estado)
    st.write('Version date:', version_date)
    st.write('Fecha In:', fecha_in)
    st.write('Fecha Out:', fecha_out)
    st.write('Time Duration:', duration_time)
    st.write('Descripción:', descripcion.capitalize())

    petition_info = {
        'petition_code': petition_code,
        'DQDP_code': DQDP_code,
        'sdatool': sdatool,
        'feature': feature,
        'UUAA': UUAA,
        'geography': geography,
        'DDBB': DDBB,
        'dev_master': dev_master, 
        'version': version,
        'petition_arq': petition_arq,
        'estado': estado,
        'version_date': version_date,
        'fecha_in': fecha_in,
        'fecha_out': fecha_out,
        'duration_time': duration_time,
        'description': descripcion
    }
    
    insert_data(petition_info)

###################################################################################################################################
st.markdown("<h1 style='font-size: 40px; text-align: center; color: #E5E1DA'>Statics</p>", unsafe_allow_html=True)
st.markdown('---')

################################################################################
conn1 = sqlite3.connect("BBVA_testing.db")
cursor1 = conn1.cursor()
cursor1.execute("PRAGMA foreign_keys = ON") #In sqlite3 foreign keys are disabled by default

#######
cursor1.execute("SELECT UUAA FROM UUAA")
all_uuaa = [x[0] for x in cursor1.fetchall()]
uuaa_selected = st.selectbox("UUAA: ", all_uuaa)
st.write(uuaa_selected)

cursor1.execute("SELECT geography FROM Geography")
all_geography = [x[0] for x in cursor1.fetchall()]
geography_selected = st.selectbox("Geography: ", all_geography)
st.write(geography_selected)

query = f"""
    SELECT pd.version, pd.version_date, p.*
    FROM Power_Design pd
    JOIN Peticion_PWD pp ON pd.UUAA = pp.uuaa
                        AND pd.geography = pp.geography
                        AND pd.dev_master = pp.dev_master 
                        AND pd.DDBB = pp.DDBB
                        AND pd.version = pp.version
    JOIN Peticion p ON pp.petition_code = p.petition_code
    WHERE pd.UUAA = '{uuaa_selected}'
    AND pd.geography = '{geography_selected}';
"""
cursor1.execute(query)
resultado = cursor1.fetchall()
st.write(resultado)

rta = [x[0] for x in cursor1.fetchall()]
st.write(rta)

#######
conn1.commit()
cursor1.close()
conn1.close()

