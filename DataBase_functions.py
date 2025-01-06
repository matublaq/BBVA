#sqlite3
import sqlite3
import nbformat

#PostgreSQL
import psycopg2
from psycopg2 import sql

#General
import numpy as np
import pandas as pd 
import time

#Execute shell commands
import subprocess


#########################################################################################################################
##################################### SQLite3, PostgreSQL LOCAL, Render(PostgreSQL) #####################################

def create_database():
    ################################################################################
    conn1 = sqlite3.connect("BBVA.db")
    cursor1 = conn1.cursor()
    cursor1.execute("PRAGMA foreign_keys = ON") #In sqlite3 foreign keys are disabled by default

    ################################################################################
    '''
    conn2 =  psycopg2.connect(
        dbname = "pwd_control", 
        user = "postgres", 
        password = "Matias123!", 
        host = "localhost",
        port = "5432"
    )
    cursor2 = conn2.cursor()
    '''

    ################################################################################
    conn3 =  psycopg2.connect(
        dbname = "pwd_control_plnk", 
        user = "matublaq",
        password = "SF19KOpSPMl8Ru51ONQ33AHOf0RuZnne", 
        host = "dpg-ctevf3t6l47c73b4jadg-a.oregon-postgres.render.com",
        port = "5432"
    )
    cursor3 = conn3.cursor()	

    ################################################################################
    # Crear la tabla Peticion
    query = '''
        CREATE TABLE IF NOT EXISTS Peticion (
            petition_code VARCHAR(64) PRIMARY KEY,
            DQDP_code VARCHAR(64) NOT NULL,
            sdatool VARCHAR(64) NOT NULL,
            feature VARCHAR(64) NOT NULL,
            petition_arq VARCHAR(64) NOT NULL,
            estado VARCHAR(20) NOT NULL CHECK (estado IN ('Pendiente', 'En Proceso', 'Finalizado')),
            fecha_in DATE NOT NULL,
            fecha_out DATE NOT NULL,
            duration_time NUMERIC(4, 2) NOT NULL, 
            description VARCHAR(255) NOT NULL
        );
    '''
    cursor1.execute(query)
    #cursor2.execute(query)
    cursor3.execute(query)
    
    #Create a UUAA table
    query = '''
        CREATE TABLE IF NOT EXISTS UUAA (
            UUAA VARCHAR(4) PRIMARY KEY,
            description VARCHAR(255)
        );
    '''
    cursor1.execute(query)
    #cursor2.execute(query)
    cursor3.execute(query)

    # Crear la tabla Geography
    query = '''
        CREATE TABLE IF NOT EXISTS Geography (
            geography VARCHAR(32) PRIMARY KEY, 
            description VARCHAR(255)
        );
    '''
    cursor1.execute(query)
    #cursor2.execute(query)
    cursor3.execute(query)

    # Crear la tabla DDBB
    query = '''
        CREATE TABLE IF NOT EXISTS DDBB (
            DDBB VARCHAR(32) PRIMARY KEY,
            description VARCHAR(255)
        );
    '''
    cursor1.execute(query)
    #cursor2.execute(query)
    cursor3.execute(query)

    # Crear la tabla Power_Design
    query = '''
        CREATE TABLE IF NOT EXISTS Power_Design (
            UUAA VARCHAR(4) NOT NULL,
            geography VARCHAR(32) NOT NULL,
            DDBB VARCHAR(32) NOT NULL,
            dev_master VARCHAR(10) NOT NULL CHECK (dev_master IN ('Dev', 'Master', 'None')),
            version VARCHAR(64) NOT NULL,
            date DATE NOT NULL,
            description VARCHAR(255),
            PRIMARY KEY (UUAA, geography, dev_master, DDBB),
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA),
            FOREIGN KEY (geography) REFERENCES Geography(geography), 
            FOREIGN KEY (DDBB) REFERENCES DDBB(DDBB)
        );
    '''
    cursor1.execute(query)
    #cursor2.execute(query)
    cursor3.execute(query)

    # Crear la tabla Peticion_PWD 
    query = '''
        CREATE TABLE IF NOT EXISTS Peticion_PWD (
            petition_code VARCHAR(64) NOT NULL,
            UUAA VARCHAR(4) NOT NULL,
            geography VARCHAR(32) NOT NULL,
            DDBB VARCHAR(32) NOT NULL,
            dev_master VARCHAR(10) NOT NULL CHECK (dev_master IN ('Dev', 'Master', 'None')),
            version VARCHAR(64) NOT NULL,
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
    #cursor2.execute(query)
    cursor3.execute(query)

########################
    conn1.commit()
    cursor1.close()
    conn1.close()

########################
    #conn2.commit()
    #cursor2.close()
    #conn2.close()

########################
    conn3.commit()
    cursor3.close()
    conn3.close()

def drop_tables():
    ################################################################################
    conn1 = sqlite3.connect("BBVA.db")
    cursor1 = conn1.cursor()
    cursor1.execute("PRAGMA foreign_keys = ON") #In sqlite3 foreign keys are disabled by default

    ################################################################################
    '''
    conn2 =  psycopg2.connect(
        dbname = "pwd_control", 
        user = "postgres", 
        password = "Matias123!", 
        host = "localhost",
        port = "5432"
    )
    cursor2 = conn2.cursor()
    '''

    ################################################################################
    conn3 =  psycopg2.connect(
        dbname = "pwd_control_plnk", 
        user = "matublaq",
        password = "SF19KOpSPMl8Ru51ONQ33AHOf0RuZnne", 
        host = "dpg-ctevf3t6l47c73b4jadg-a.oregon-postgres.render.com",
        port = "5432"
    )
    cursor3 = conn3.cursor()

    ################################################################################
    tables = ["Peticion_PWD", "Power_Design", "DDBB", "Geography", "UUAA", "Peticion"]
    for table in tables:
        cursor1.execute(f"DROP TABLE IF EXISTS {table}")
    query = '''
        DROP TABLE IF EXISTS Peticion_PWD CASCADE;
        DROP TABLE IF EXISTS Power_Design CASCADE;
        DROP TABLE IF EXISTS DDBB CASCADE;
        DROP TABLE IF EXISTS Geography CASCADE;
        DROP TABLE IF EXISTS UUAA CASCADE;
        DROP TABLE IF EXISTS Peticion CASCADE;
    '''
    #cursor2.execute(query)
    cursor3.execute(query)

    ########################
    conn1.commit()
    cursor1.close()
    conn1.close()

    ########################
    #conn2.commit()
    #cursor2.close()
    #conn2.close()

    ########################
    conn3.commit()
    cursor3.close()
    conn3.close()

def insert_data(petition_info): 
    ################################################################################
    conn1 = sqlite3.connect("BBVA.db")
    cursor1 = conn1.cursor()
    cursor1.execute("PRAGMA foreign_keys = ON") #In sqlite3 foreign keys are disabled by default

    ################################################################################
    '''
    conn2 =  psycopg2.connect(
        dbname = "pwd_control", 
        user = "postgres", 
        password = "Matias123!", 
        host = "localhost",
        port = "5432"
    )
    cursor2 = conn2.cursor()
    '''

    ################################################################################
    conn3 =  psycopg2.connect(
        dbname = "pwd_control_plnk", 
        user = "matublaq",
        password = "SF19KOpSPMl8Ru51ONQ33AHOf0RuZnne", 
        host = "dpg-ctevf3t6l47c73b4jadg-a.oregon-postgres.render.com",
        port = "5432"
    )
    cursor3 = conn3.cursor()

    ################################################################################
    #Data validation
    petition_info["petition_code"] = petition_info["petition_code"].strip().upper()
    petition_info["DQDP_code"] = petition_info["DQDP_code"].strip().upper()
    petition_info["sdatool"] = petition_info["sdatool"].strip().upper()
    petition_info["feature"] = petition_info["feature"].strip().upper()
    petition_info["UUAA"] = petition_info["UUAA"].strip().upper()
    #petition_info["geography"]
    #petition_info["DDBB"]
    #petition_info["dev_master"]
    petition_info["version"] = petition_info["version"].strip()
    petition_info["petition_arq"] = petition_info["petition_arq"].strip().upper()
    #petition_info["estado"]
    #petition_info["version_date"]
    #petition_info["fecha_in"]
    #petition_info["fecha_out"]
    #petition_info["duration_time"]
    petition_info["description"] = petition_info["description"].strip().capitalize()

    for key, value in petition_info.items():
        if value == "Nan" or value == None or value == "" or value == "None": 
            petition_info[key] = None
    ################################################################################
    try:
        ###########################################################################################################################
        #Insert data into Peticion table
        cursor1.execute("SELECT petition_code FROM Peticion")
        petition_records = cursor1.fetchall()
        if not petition_info['petition_code'] in [record[0] for record in petition_records]:
            cursor1.execute("INSERT INTO Peticion (petition_code, DQDP_code, sdatool, feature, petition_arq, estado, fecha_in, fecha_out, duration_time, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (petition_info['petition_code'], petition_info['DQDP_code'], petition_info['sdatool'], petition_info['feature'], petition_info['petition_arq'], petition_info['estado'], petition_info['fecha_in'], petition_info['fecha_out'], petition_info['duration_time'], petition_info['description'], )) #SQLite3

        #cursor2.execute("SELECT petition_code FROM Peticion")
        #petition_records = cursor1.fetchall()
        #if not petition_info['petition_code'] in [record[0] for record in petition_records]:
        #    cursor2.execute("INSERT INTO Peticion (petition_code, DQDP_code, sdatool, feature, petition_arq, estado, fecha_in, fecha_out, duration_time, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (petition_info['petition_code'], petition_info['DQDP_code'], petition_info['sdatool'], petition_info['feature'], petition_info['petition_arq'], petition_info['estado'], petition_info['fecha_in'], petition_info['fecha_out'], petition_info['duration_time'], petition_info['description'], )) #PostgreSQL localhost

        cursor3.execute("SELECT petition_code FROM Peticion")
        petition_records = cursor3.fetchall()
        if not petition_info['petition_code'] in [record[0] for record in petition_records]:
            cursor3.execute("INSERT INTO Peticion (petition_code, DQDP_code, sdatool, feature, petition_arq, estado, fecha_in, fecha_out, duration_time, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (petition_info['petition_code'], petition_info['DQDP_code'], petition_info['sdatool'], petition_info['feature'], petition_info['petition_arq'], petition_info['estado'], petition_info['fecha_in'], petition_info['fecha_out'], petition_info['duration_time'], petition_info['description'], )) #PostgreSQL Render

        ###########################################################################################################################
        #If UUAA  already exists? Insert data into UUAA table
        cursor1.execute("SELECT UUAA FROM UUAA")
        uuaa_records = cursor1.fetchall()
        if not petition_info['UUAA'] in [record[0] for record in uuaa_records]:
            cursor1.execute("INSERT INTO UUAA (UUAA) VALUES (?)", (petition_info['UUAA'], )) #SQLite3

        #cursor2.execute("SELECT UUAA FROM UUAA")
        #uuaa_records = cursor2.fetchall()
        #if not petition_form['UUAA'] in [record[0] for record in uuaa_records]:
        #    cursor2.execute("INSERT INTO UUAA (UUAA) VALUES (%s)", (petition_info['UUAA'], )) #PostgreSQL localhost

        cursor3.execute("SELECT UUAA FROM UUAA")
        uuaa_records = cursor3.fetchall()
        if not petition_info['UUAA'] in [record[0] for record in uuaa_records]:
            cursor3.execute("INSERT INTO UUAA (UUAA) VALUES (%s)", (petition_info['UUAA'], )) #PostgreSQL Render

        ###########################################################################################################################
        #If geography already exists? Insert data into Geography table
        cursor1.execute("SELECT geography FROM Geography")
        geography_records = cursor1.fetchall()
        if not petition_info['geography'] in [record[0] for record in geography_records]:
            cursor1.execute("INSERT INTO Geography (geography) VALUES (?)", (petition_info['geography'], )) #SQLite3

        #cursor2.execute("SELECT geography FROM Geography")
        #geography_records = cursor2.fetchall()
        #if not petition_form['geography'] in [record[0] for record in geography_records]:
        #    cursor2.execute("INSERT INTO Geography (geography) VALUES (%s)", (petition_info['geography'], )) #PostgreSQL localhost

        cursor3.execute("SELECT geography FROM Geography")
        geography_records = cursor3.fetchall()
        if not petition_info['geography'] in [record[0] for record in geography_records]:
            cursor3.execute("INSERT INTO Geography (geography) VALUES (%s)", (petition_info['geography'], )) #PostgreSQL Render

        ###########################################################################################################################
        #If DDBB already exists? Insert data into DDBB table
        cursor1.execute("SELECT DDBB FROM DDBB")
        ddbb_records = cursor1.fetchall()
        if not petition_info['DDBB'] in [record[0] for record in ddbb_records]:
            cursor1.execute("INSERT INTO DDBB (DDBB) VALUES (?)", (petition_info['DDBB'], )) #SQLite3

        #cursor2.execute("SELECT DDBB FROM DDBB")
        #ddbb_records = cursor2.fetchall()
        #if not petition_form['DDBB'] in [record[0] for record in ddbb_records]:
        #    cursor2.execute("INSERT INTO DDBB (DDBB) VALUES (%s)", (petition_info['DDBB'], )) #PostgreSQL localhost

        cursor3.execute("SELECT DDBB FROM DDBB")
        ddbb_records = cursor3.fetchall()
        if not petition_info['DDBB'] in [record[0] for record in ddbb_records]:
            cursor3.execute("INSERT INTO DDBB (DDBB) VALUES (%s)", (petition_info['DDBB'], )) #PostgreSQL Render

        ###########################################################################################################################      
        #If UUAA, geography_id, dev_master already exists? Insert data into Power_Design table
        cursor1.execute("SELECT UUAA, geography, DDBB, dev_master FROM Power_Design")
        pwd_records = cursor1.fetchall()
        if not [petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master']] in [record[0] for record in pwd_records]:
            cursor1.execute("INSERT INTO Power_Design (UUAA, geography, DDBB, dev_master, version, version_date, description) VALUES (?, ?, ?, ?, ?, ?, ?)", (petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version'], petition_info['version_date'], petition_info['description'], )) #SQLite3

        #cursor2.execute("SELECT UUAA, geography, DDBB, dev_master FROM Power_Design")
        #pwd_records = cursor2.fetchall()
        #if not [petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master']] in [record for record in pwd_records]:
        #    cursor2.execute("INSERT INTO Power_Design (UUAA, geography, DDBB, dev_master, version, version_date, description) VALUES (%s, %s, %s, %s, %s, %s, %s)", (petition_info['UUAA'], petition_info['Geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version'], petition_info['version_date'], petition_info['description'], )) #PostgreSQL localhost

        cursor3.execute("SELECT UUAA, geography, DDBB, dev_master FROM Power_Design")
        pwd_records = cursor3.fetchall()
        if not [petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master']] in [record[0] for record in pwd_records]:
            cursor3.execute("INSERT INTO Power_Design (UUAA, geography, DDBB, dev_master, version, version_date, description) VALUES (%s, %s, %s, %s, %s, %s, %s)", (petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version'], petition_info['version_date'], petition_info['description'], )) #PostgreSQL Render

        ###########################################################################################################################
        #If petition_code, UUAA, geography_id, dev_master already exists? Insert data into Peticion_PWD table
        cursor1.execute("SELECT petition_code, UUAA, geography, DDBB, dev_master FROM Peticion_PWD")
        pwd_records = cursor1.fetchall()
        if not [petition_info['petition_code'], petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version']] in [record[0] for record in pwd_records]:
            cursor1.execute("INSERT INTO Peticion_PWD (petition_code, UUAA, geography, DDBB, dev_master, version, description) VALUES (?, ?, ?, ?, ?, ?, ?)", (petition_info['petition_code'], petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version'], petition_info['description'], )) #SQLite3

        #cursor2.execute("SELECT petition_code, UUAA, geography, DDBB, dev_master FROM Peticion_PWD")
        #pwd_records = cursor2.fetchall()
        #if not [petition_info['petition_code'], petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version']] in [record[0] for record in pwd_records]:
        #    cursor2.execute("INSERT INTO Peticion_PWD (petition_code, UUAA, geography, dev_master, version, description) VALUES (%s, %s, %s, %s, %s, %s, %s)", (petition_info['petition_code'], petition_info['UUAA'], petition_info['Geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version'], petition_info['description'], )) #PostgreSQL localhost

        cursor3.execute("SELECT petition_code, UUAA, geography, DDBB, dev_master FROM Peticion_PWD")
        pwd_records = cursor3.fetchall()
        if not [petition_info['petition_code'], petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version']] in [record[0] for record in pwd_records]:
            cursor3.execute("INSERT INTO Peticion_PWD (petition_code, UUAA, geography, DDBB, dev_master, version, description) VALUES (%s, %s, %s, %s, %s, %s, %s)", (petition_info['petition_code'], petition_info['UUAA'], petition_info['geography'], petition_info['DDBB'], petition_info['dev_master'], petition_info['version'], petition_info['description'], )) #PostgreSQL Render
    
        #Confirm the transaction
        conn1.commit()
        #conn2.commit()
        conn3.commit()

    finally:
        ########################
        if cursor1: 
            cursor1.close()
        if conn1:
            conn1.close()

        ########################
        '''
        if cursor2:
            cursor2.close()
        if conn2:
            conn2.close()
        '''

        ########################
        if cursor3:
            cursor3.close()
        if conn3:
            conn3.close()

        ########################