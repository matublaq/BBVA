#sqlite3
import sqlite3
import nbformat

#PostgreSQL Is not working on Streamlit yet
#import psycopg2
#from psycopg2 import sql

#General
import numpy as np
import pandas as pd 
import time

#Execute shell commands
import subprocess

import streamlit as st
import streamlit.components.v1 as components

#Google sheed API
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials


#########################################################################################################################
##################################### SQLite3, PostgreSQL LOCAL, Render(PostgreSQL) #####################################

def create_database_testing():
    ################################################################################
    conn1 = sqlite3.connect("BBVA_testing.db")
    cursor1 = conn1.cursor()
    cursor1.execute("PRAGMA foreign_keys = ON") #In sqlite3 foreign keys are disabled by default

    ################################################################################
    # Crear la tabla Peticion
    query = '''
        CREATE TABLE IF NOT EXISTS Peticion (
            petition_code VARCHAR(64) PRIMARY KEY,
            DQDP_code VARCHAR(64),
            sdatool VARCHAR(64),
            feature VARCHAR(64),
            petition_arq VARCHAR(64),
            fecha_in DATE,
            fecha_out DATE,
            duration_time NUMERIC(4, 2), 
            description VARCHAR(255)
        );
    '''
    cursor1.execute(query)
    
    #Create a UUAA table
    query = '''
        CREATE TABLE IF NOT EXISTS UUAA (
            UUAA VARCHAR(4) PRIMARY KEY,
            description VARCHAR(255)
        );
    '''
    cursor1.execute(query)

    # Crear la tabla Geography
    query = '''
        CREATE TABLE IF NOT EXISTS Geography (
            geography VARCHAR(32) PRIMARY KEY, 
            description VARCHAR(255)
        );
    '''
    cursor1.execute(query)

    # Crear la tabla DDBB
    query = '''
        CREATE TABLE IF NOT EXISTS DDBB (
            DDBB VARCHAR(32) PRIMARY KEY,
            description VARCHAR(255)
        );
    '''
    cursor1.execute(query)

    # Crear la tabla Power_Design
    query = '''
        CREATE TABLE IF NOT EXISTS Power_Design (
            UUAA VARCHAR(4),
            geography VARCHAR(32),
            DDBB VARCHAR(32),
            dev_master VARCHAR(10) CHECK (dev_master IN ('Dev', 'Master', 'None')),
            version VARCHAR(64),
            version_date DATE,
            description VARCHAR(255),
            PRIMARY KEY (UUAA, geography, dev_master, DDBB),
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA),
            FOREIGN KEY (geography) REFERENCES Geography(geography), 
            FOREIGN KEY (DDBB) REFERENCES DDBB(DDBB)
        );
    '''
    cursor1.execute(query)

    # Crear la tabla Peticion_PWD 
    query = '''
        CREATE TABLE IF NOT EXISTS Peticion_PWD (
            petition_code VARCHAR(64),
            UUAA VARCHAR(4),
            geography VARCHAR(32),
            DDBB VARCHAR(32),
            dev_master VARCHAR(10) CHECK (dev_master IN ('Dev', 'Master', 'None')),
            version VARCHAR(64),
            description VARCHAR(255),
            PRIMARY KEY (petition_code, UUAA, geography, DDBB, dev_master),
            FOREIGN KEY (petition_code) REFERENCES Peticion(petition_code), 
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA),
            FOREIGN KEY (geography) REFERENCES Geography(geography), 
            FOREIGN KEY (DDBB) REFERENCES DDBB(DDBB), 
            FOREIGN KEY (UUAA, geography, DDBB, dev_master) REFERENCES Power_Design(UUAA, geography, DDBB, dev_master)
        );
    '''
    cursor1.execute(query)

########################
    conn1.commit()
    cursor1.close()
    conn1.close()

def drop_tables_testing():
    ################################################################################
    conn1 = sqlite3.connect("BBVA_testing.db")
    cursor1 = conn1.cursor()
    cursor1.execute("PRAGMA foreign_keys = ON") #In sqlite3 foreign keys are disabled by default

    ################################################################################
    tables = ["Peticion_PWD", "Power_Design", "DDBB", "Geography", "UUAA", "Peticion"]
    for table in tables:
        cursor1.execute(f"DROP TABLE IF EXISTS {table}")

    ########################
    conn1.commit()
    cursor1.close()
    conn1.close()

def insert_data_testing(petition_info): 
    ##########################################################################################################################################
    ######################################################## RELATIONAL DATABASE #############################################################
    ################################################################################
    conn1 = sqlite3.connect("BBVA_testing.db")
    cursor1 = conn1.cursor()
    cursor1.execute("PRAGMA foreign_keys = ON") #In sqlite3 foreign keys are disabled by default

    ################################################################################
    #Data validation
    petition_info["petition_code"] = petition_info["petition_code"].strip().upper()
    petition_info["DQDP_code"] = petition_info["DQDP_code"].strip().upper()
    petition_info["sdatool"] = petition_info["sdatool"].strip().upper()
    petition_info["feature"] = petition_info["feature"].strip().upper()
    petition_info["UUAA"] = petition_info["UUAA"].strip().upper()
    petition_info["geography"] = petition_info["geography"].strip()
    #petition_info["DDBB"]
    #petition_info["dev_master"]
    petition_info["version"] = petition_info["version"].strip()
    petition_info["petition_arq"] = petition_info["petition_arq"].strip().upper()
    #petition_info["version_date"]
    #petition_info["fecha_in"]
    #petition_info["fecha_out"]
    #petition_info["duration_time"]
    petition_info["description"] = petition_info["description"].strip().capitalize()

    #Limpiamos datos del DDBB y de la geography
    for key in petition_info.keys():
        if petition_info[key] == "Nan" or petition_info[key] == None or petition_info[key] == "" or petition_info[key] == "None" or petition_info[key] == np.nan: 
            petition_info[key] = None
        
        if key == "DDBB": 
            if petition_info[key] == "ORACLE Physics" or petition_info[key] == "ORACLE PHYSICS":
                petition_info[key] = "Oracle Physics"
            elif petition_info[key] == "ELASTICSEARCH" or petition_info[key] == "ElasTICSEARCH" or petition_info[key] == "ElaSTICSEARCH": 
                petition_info[key] = "Elastic Search"
            elif petition_info[key] == "ORACLE R2" or petition_info[key] == "oracle r2": 
                petition_info[key] = "Oracle R2"
            elif petition_info[key] == "DB2 HOST": 
                petition_info[key] = "DB2 Host"
            elif petition_info[key] == "TERADATA" or petition_info[key] == "teradata": 
                petition_info[key] = "Teradata"
            elif petition_info[key] == "MongoDB" or petition_info[key] == "MONGO DB" or petition_info[key] == "MongoDB" or petition_info[key] == "MONGODB": 
                petition_info[key] = "Mongo DB"
            elif petition_info[key] == "POSTGRESS R2" or petition_info[key] == "POSTGRESS Physics" or petition_info[key] == "PosgreSQL": 
                petition_info[key] = "PostgreSQL"
            elif petition_info[key] == "NETEZZA": 
                petition_info[key] = "Netezza"

        if key == "geography": 
            if petition_info[key] == "España-CIB" or petition_info[key] == "España/CIB": 
                petition_info[key] = "CIB"

    ################################################################################
    try:
        ###########################################################################################################################
        #Insert data into Peticion table
        cursor1.execute("SELECT petition_code FROM Peticion")
        petition_records = cursor1.fetchall()
        if not petition_info['petition_code'] in [record[0] for record in petition_records]:
            cursor1.execute("INSERT INTO Peticion (petition_code, DQDP_code, sdatool, feature, petition_arq, fecha_in, fecha_out, duration_time, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (petition_info['petition_code'], petition_info['DQDP_code'], petition_info['sdatool'], petition_info['feature'], petition_info['petition_arq'], petition_info['fecha_in'], petition_info['fecha_out'], petition_info['duration_time'], petition_info['description'], )) #SQLite3

        ###########################################################################################################################
        #If UUAA  already exists? Insert data into UUAA table
        cursor1.execute("SELECT UUAA FROM UUAA")
        uuaa_records = cursor1.fetchall()
        if not petition_info['UUAA'] in [record[0] for record in uuaa_records]:
            cursor1.execute("INSERT INTO UUAA (UUAA) VALUES (?)", (petition_info['UUAA'], )) #SQLite3

        ###########################################################################################################################
        #If geography already exists? Insert data into Geography table
        cursor1.execute("SELECT geography FROM Geography")
        geography_records = cursor1.fetchall()
        if not petition_info['geography'] in [record[0] for record in geography_records]:
            cursor1.execute("INSERT INTO Geography (geography) VALUES (?)", (petition_info['geography'], )) #SQLite3

        ###########################################################################################################################
        #If DDBB already exists? Insert data into DDBB table
        cursor1.execute("SELECT DDBB FROM DDBB")
        ddbb_records = cursor1.fetchall()
        if not petition_info['DDBB'] in [record[0] for record in ddbb_records]:
            cursor1.execute("INSERT INTO DDBB (DDBB) VALUES (?)", (petition_info['DDBB'], )) #SQLite3

        ###########################################################################################################################      
        #If UUAA, geography_id, dev_master already exists? Insert data into Power_Design table
        cursor1.execute("SELECT UUAA, geography, DDBB, dev_master FROM Power_Design")
        pwd_records = cursor1.fetchall()
        if not [petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master']] in [record[0] for record in pwd_records]:
            cursor1.execute("INSERT INTO Power_Design (UUAA, geography, DDBB, dev_master, version, version_date, description) VALUES (?, ?, ?, ?, ?, ?, ?)", (petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version'], petition_info['version_date'], petition_info['description'], )) #SQLite3

        ###########################################################################################################################
        #If petition_code, UUAA, geography_id, dev_master already exists? Insert data into Peticion_PWD table
        cursor1.execute("SELECT petition_code, UUAA, geography, DDBB, dev_master FROM Peticion_PWD")
        pwd_records = cursor1.fetchall()
        if not [petition_info['petition_code'], petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version']] in [record[0] for record in pwd_records]:
            cursor1.execute("INSERT INTO Peticion_PWD (petition_code, UUAA, geography, DDBB, dev_master, version, description) VALUES (?, ?, ?, ?, ?, ?, ?)", (petition_info['petition_code'], petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version'], petition_info['description'], )) #SQLite3
    
        #Confirm the transaction
        conn1.commit()

    finally:
        ########################
        if cursor1: 
            cursor1.close()
        if conn1:
            conn1.close()
    ##########################################################################################################################################
    ######################################################## PETITION EXCEL ##################################################################
    
    if st.runtime.exists(): 
        # Email service account that need to share the google sheet
        #email that need to share the google sheet = matiasblaquier@theta-voyager-406314.iam.gserviceaccount.com
        service_account_email = "matiasblaquier@theta-voyager-406314.iam.gserviceaccount.com"

        scope = [
            'https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
            ]

        credentials = "credentials.json"

        #Cargar credenciales
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)

        #Autorizar gspread con las credenciales
        client = gspread.authorize(creds)

        # ID de la hoja de cálculo 
        srpeadsheet_id = "1biaKHw0fV5w5HBWsAto2Q-WCLkXe4bwc72hoS6BNDe8" #petitions file

        # Open the Google Sheet file by ID
        spreadsheet = client.open_by_key(srpeadsheet_id)

        # Select worksheet
        worksheet = spreadsheet.worksheet('All petitions')

        #new row
        new_row_list = list(petition_info.values()) 
        worksheet.append_row(new_row_list)


