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

    # Crear la tabla Power_Design
    query = '''
        CREATE TABLE IF NOT EXISTS Power_Design (
            UUAA VARCHAR(4) NOT NULL,
            geography VARCHAR(32) NOT NULL,
            dev_master VARCHAR(10) NOT NULL CHECK (dev_master IN ('Dev', 'Master', 'None')),
            version INTEGER NOT NULL,
            date DATE NOT NULL,
            description VARCHAR(255),
            PRIMARY KEY (UUAA, geography, dev_master),
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA),
            FOREIGN KEY (geography) REFERENCES Geography(geography)
        );
    '''
    cursor1.execute(query)
    #cursor2.execute(query)
    cursor3.execute(query)

    # Crear la tabla Peticion
    query = '''
        CREATE TABLE IF NOT EXISTS Peticion (
            petition_code VARCHAR(64) PRIMARY KEY,
            DQDP_code VARCHAR(64) NOT NULL,
            sdatool VARCHAR(64) NOT NULL,
            feature VARCHAR(64) NOT NULL,
            UUAA VARCHAR(4) NOT NULL,
            geography VARCHAR(32) NOT NULL,
            petition_arq VARCHAR(64) NOT NULL,
            estado VARCHAR(20) NOT NULL CHECK (estado IN ('Pendiente', 'En Proceso', 'Finalizado')),
            fecha_in DATE NOT NULL,
            fecha_out DATE,
            time_duration TIME NOT NULL, 
            descripcion VARCHAR(255) NOT NULL,
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA), 
            FOREIGN KEY (geography) REFERENCES Geography(geography)
        );
    '''
    cursor1.execute(query)
    #cursor2.execute(query)
    cursor3.execute(query)

    # Crear la tabla Peticion_PWD con una clave primaria compuesta
    query = '''
        CREATE TABLE IF NOT EXISTS Peticion_PWD (
            petition_code VARCHAR(64) NOT NULL,
            UUAA VARCHAR(4) NOT NULL,
            geography VARCHAR(32) NOT NULL,
            dev_master VARCHAR(10) NOT NULL CHECK (dev_master IN ('Dev', 'Master', 'None')),
            version INTEGER NOT NULL,
            PRIMARY KEY (petition_code, UUAA, geography, dev_master),
            FOREIGN KEY (petition_code) REFERENCES Peticion(petition_code),
            FOREIGN KEY (UUAA, geography, dev_master) REFERENCES Power_Design(UUAA, geography, dev_master)
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
########################

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

    tables = ["UUAA", "Geography", "Power_Design", "Peticion", "Peticion_PWD", "Versions"]
    for table in tables:
        cursor1.execute(f"DROP TABLE IF EXISTS {table}")
    query = '''
        DROP TABLE IF EXISTS UUAA CASCADE;
        DROP TABLE IF EXISTS Geography CASCADE;
        DROP TABLE IF EXISTS Power_Design CASCADE;
        DROP TABLE IF EXISTS Peticion CASCADE;
        DROP TABLE IF EXISTS Peticion_PWD CASCADE;
        DROP TABLE IF EXISTS Versions CASCADE;
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
    ########################

def insert_data(petition_form): 
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
    try: 
        #Insert data into Peticion table
        query = "INSERT INTO Peticion (petition_code, DQDP_code, sdatool, feature, UUAA, geography, petition_arq, estado, fecha_in, fecha_out, time_duration, descripcion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        params = (petition_form['petition_code'], petition_form['DQDP_code'], petition_form['sdatool'], petition_form['feature'], petition_form['UUAA'], petition_form['geography'], petition_form['petition_arq'], petition_form['estado'], petition_form['fecha_in'], petition_form['fecha_out'], petition_form['time_duration'], petition_form['descripcion'])
        cursor1.execute(query, params)
        #cursor2.execute(query)
        cursor3.execute(query, params)

        #If UUAA  already exists? Insert data into UUAA table
        if not petition_form['UUAA'] in cursor1.execute("SELECT UUAA FROM UUAA").fetchall():
            cursor1.execute("INSERT INTO UUAA (UUAA) VALUES (?)", (petition_form['UUAA'])) #SQLite3
        #if not petition_form['UUAA'] in cursor2.execute("SELECT UUAA FROM UUAA").fetchall():
        #    cursor2.execute("INSERT INTO UUAA (UUAA) VALUES (?)", (petition_form['UUAA'])) #PostgreSQL localhost
        if not petition_form['UUAA'] in cursor3.execute("SELECT UUAA FROM UUAA").fetchall():
            cursor3.execute("INSERT INTO UUAA (UUAA) VALUES (?)", (petition_form['UUAA'])) #PostgreSQL Render

        #If geography already exists? Insert data into Geography table
        if not petition_form['geography'] in cursor1.execute("SELECT geography FROM Geography").fetchall():
            cursor1.execute("INSERT INTO Geography (geography) VALUES (?)", (petition_form['geography'])) #SQLite3
        #if not petition_form['Geography'] in cursor2.execute("SELECT geography FROM Geography").fetchall():
        #    cursor2.execute("INSERT INTO Geography (geography) VALUES (?)", (petition_form['Geography'])) #PostgreSQL localhost
        if not petition_form['geography'] in cursor3.execute("SELECT geography FROM Geography").fetchall():
            cursor3.execute("INSERT INTO Geography (geography) VALUES (?)", (petition_form['geography'])) #PostgreSQL Render

        #If petition_code, UUAA, geography_id, dev_master already exists? Insert data into Peticion_PWD table
        if not [petition_form['petition_code'], petition_form['UUAA'], petition_form['geography'], petition_form['dev_master']] in cursor1.execute("SELECT petition_code, UUAA, geography, dev_master FROM Peticion_PWD").fetchall():
            cursor1.execute("INSERT INTO Peticion_PWD (petition_code, UUAA, geography, dev_master, version) VALUES (?, ?, ?, ?, ?)", (petition_form['petition_code'], petition_form['UUAA'], petition_form['Geography'], petition_form['dev_master'], petition_form['version'])) #SQLite3
        #if not [petition_form['petition_code'], petition_form['UUAA'], petition_form['Geography'], petition_form['dev_master']] in cursor2.execute("SELECT petition_code, UUAA, geography, dev_master FROM Peticion_PWD").fetchall():
        #    cursor2.execute("INSERT INTO Peticion_PWD (petition_code, UUAA, geography, dev_master, version) VALUES (?, ?, ?, ?, ?)", (petition_form['petition_code'], petition_form['UUAA'], petition_form['Geography'], petition_form['dev_master'], petition_form['version'])) #PostgreSQL localhost
        if not [petition_form['petition_code'], petition_form['UUAA'], petition_form['geography'], petition_form['dev_master']] in cursor3.execute("SELECT petition_code, UUAA, geography, dev_master FROM Peticion_PWD").fetchall():
            cursor3.execute("INSERT INTO Peticion_PWD (petition_code, UUAA, geography, dev_master, version) VALUES (?, ?, ?, ?, ?)", (petition_form['petition_code'], petition_form['UUAA'], petition_form['Geography'], petition_form['dev_master'], petition_form['version'])) #PostgreSQL Render
        
        #If UUAA, geography_id, dev_master already exists? Insert data into Power_Design table
        if not [petition_form['UUAA'], petition_form['geography'], petition_form['dev_master']] in cursor1.execute("SELECT UUAA, geography, dev_master FROM Power_Design").fetchall():
            cursor1.execute("INSERT INTO Power_Design (UUAA, geography, dev_master, version, date, description) VALUES (?, ?, ?, ?, ?, ?)", (petition_form['UUAA'], petition_form['Geography'], petition_form['dev_master'], petition_form['version'], petition_form['date'], petition_form['description']))
        #if not [petition_form['UUAA'], petition_form['Geography'], petition_form['dev_master']] in cursor2.execute("SELECT UUAA, geography, dev_master FROM Power_Design").fetchall():
        #    cursor2.execute("INSERT INTO Power_Design (UUAA, geography, dev_master, version, date, description) VALUES (?, ?, ?, ?, ?, ?)", (petition_form['UUAA'], petition_form['Geography'], petition_form['dev_master'], petition_form['version'], petition_form['date'], petition_form['description']))
        if not [petition_form['UUAA'], petition_form['geography'], petition_form['dev_master']] in cursor3.execute("SELECT UUAA, geography, dev_master FROM Power_Design").fetchall():
            cursor3.execute("INSERT INTO Power_Design (UUAA, geography, dev_master, version, date, description) VALUES (?, ?, ?, ?, ?, ?)", (petition_form['UUAA'], petition_form['Geography'], petition_form['dev_master'], petition_form['version'], petition_form['date'], petition_form['description']))
    
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