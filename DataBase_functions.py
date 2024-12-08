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

#############################################################################################################################
############################################### SQLITE3 #####################################################################
def create_databas_sqlite3():
    # Connect/Create a database
    conn = sqlite3.connect("BBVA.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")


    #Create a UUAA table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UUAA (
            UUAA VARCHAR(4) PRIMARY KEY,
            description VARCHAR(255)
        )
    ''')

    #Create a Geography table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Geography (
            geography_id INTEGER PRIMARY KEY,
            geography VARCHAR(64) NOT NULL, 
            description VARCHAR(255)
        )
    ''')


    #Create a Power_Design table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Power_Design (
            UUAA VARCHAR(4) NOT NULL,
            Geography_id INTEGER NOT NULL,
            dev_master CHECK(dev_master IN ('Dev', 'Master', 'None')) NOT NULL,
            version INTEGER NOT NULL,
            date DATE NOT NULL,
            description VARCHAR(255),
            PRIMARY KEY (UUAA, Geography_id, dev_master),
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA),
            FOREIGN KEY (geography_id) REFERENCES Geography(geography_id)
        )
    ''')

    # Create a petición table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Peticion (
            petition_code VARCHAR(64) PRIMARY KEY,
            DQDP_code VARCHAR(64) NOT NULL,
            sdatool VARCHAR(64) NOT NULL,
            feature VARCHAR(64) NOT NULL,
            UUAA VARCHAR(4) NOT NULL,
            geography_id INTEGER NOT NULL,
            petition_arq VARCHAR(64) NOT NULL,
            estado CHECK(estado IN ('Pendiente', 'En Proceso', 'Finalizado')) NOT NULL,
            fecha_in DATE NOT NULL,
            fecha_out DATE,
            time_duration TIME NOT NULL, 
            descripcion varchar(255) NOT NULL,
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA), 
            FOREIGN KEY (geography_id) REFERENCES Geography(geography_id)
        )
    ''')

    # Create a Peticion_PowerDesign table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Peticion_PWD (
            petition_code VARCHAR(64) NOT NULL,
            UUAA VARCHAR(4) NOT NULL,
            Geography_id INTEGER NOT NULL,
            dev_master CHECK(dev_master IN ('Dev', 'Master', 'None')) NOT NULL,
            version INTEGER NOT NULL,
            PRIMARY KEY (petition_code, UUAA, Geography_id, dev_master),
            FOREIGN KEY (petition_code) REFERENCES Peticion(petition_code),
            FOREIGN KEY (UUAA, Geography_id, dev_master) REFERENCES Power_Design(UUAA, Geography_id, dev_master), 
            FOREIGN KEY (version_id) REFERENCES Versions(version_id)
        )
    ''')

    conn.commit()
    conn.close()

def delete_database_tables_sqlite3():
    conn = sqlite3.connect("BBVA.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS UUAA")
    cursor.execute("DROP TABLE IF EXISTS Geography")
    cursor.execute("DROP TABLE IF EXISTS Power_Design")
    cursor.execute("DROP TABLE IF EXISTS Peticion")
    cursor.execute("DROP TABLE IF EXISTS Peticion_PWD")
    cursor.execute("DROP TABLE IF EXISTS Versions")

    conn.commit()
    conn.close()


# Petition form: [petition_code, DQDP_code, sdatool, feature, UUAA, geography, petition_arq, estado, fecha_in, fecha_out, time_duration, descripcion]
def insert_data_sqlite3(petition_form):
    conn = sqlite3.connect("BBVA.db")
    cursor = conn.cursor()

    #Insert data into Peticion table
    cursor.execute("INSERT INTO Peticion (petition_code, DQDP_code, sdatool, feature, UUAA, geography_id, petition_arq, estado, fecha_in, fecha_out, time_duration, descripcion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (petition_form['petition_code'], petition_form['DQDP_code'], petition_form['sdatool'], petition_form['feature'], petition_form['UUAA'], petition_form['Geography'], petition_form['petition_arq'], petition_form['estado'], petition_form['fecha_in'], petition_form['fecha_out'], petition_form['time_duration'], petition_form['descripcion']))
    
    #if UUAA and geography already exists? 
    # Insert data into UUAA and Geography tables
    if not petition_from['UUAA'] in cursor.execute("SELECT UUAA FROM UUAA").fetchall():
        cursor.execute("INSERT INTO UUAA (UUAA, description) VALUES (?, ?)", (petition_form['UUAA']))
    if not petition_form['Geography'] in cursor.execute("SELECT geography FROM Geography").fetchall():
        cursor.execute("INSERT INTO Geography (geography, description) VALUES (?, ?)", (petition_form['Geography']))


    conn.commit()
    conn.close()


#############################################################################################################################
############################################### POSTGRESQL ##################################################################

def create_database_postgresql():
    # Connect/Create a database
    conn = psycopg2.connect(
        dbname = "pwd_control", 
        user = "postgres", 
        password = "Matias123!", 
        host = "localhost",
        port = "5432"
    )
    
    cursor = conn.cursor()

    # Crear la tabla UUAA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UUAA (
            UUAA VARCHAR(4) PRIMARY KEY,
            description VARCHAR(255)
        )
    ''')

    # Crear la tabla Geography
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Geography (
            geography_id SERIAL PRIMARY KEY,
            geography VARCHAR(64) NOT NULL, 
            description VARCHAR(255)
        )
    ''')

    # Crear la tabla Power_Design
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Power_Design (
            UUAA VARCHAR(4) NOT NULL,
            geography_id INTEGER NOT NULL,
            dev_master VARCHAR(10) NOT NULL CHECK (dev_master IN ('Dev', 'Master', 'None')),
            version INTEGER NOT NULL,
            date DATE NOT NULL,
            description VARCHAR(255),
            PRIMARY KEY (UUAA, geography_id, dev_master),
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA),
            FOREIGN KEY (geography_id) REFERENCES Geography(geography_id)
        )
    ''')

    # Crear la tabla Peticion
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Peticion (
            petition_code VARCHAR(64) PRIMARY KEY,
            DQDP_code VARCHAR(64) NOT NULL,
            sdatool VARCHAR(64) NOT NULL,
            feature VARCHAR(64) NOT NULL,
            UUAA VARCHAR(4) NOT NULL,
            geography_id INTEGER NOT NULL,
            petition_arq VARCHAR(64) NOT NULL,
            estado VARCHAR(20) NOT NULL CHECK (estado IN ('Pendiente', 'En Proceso', 'Finalizado')),
            fecha_in DATE NOT NULL,
            fecha_out DATE,
            time_duration TIME NOT NULL, 
            descripcion VARCHAR(255) NOT NULL,
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA), 
            FOREIGN KEY (geography_id) REFERENCES Geography(geography_id)
        )
    ''')

    # Crear la tabla Peticion_PWD con una clave primaria compuesta
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Peticion_PWD (
            petition_code VARCHAR(64) NOT NULL,
            UUAA VARCHAR(4) NOT NULL,
            geography_id INTEGER NOT NULL,
            dev_master VARCHAR(10) NOT NULL CHECK (dev_master IN ('Dev', 'Master', 'None')),
            version INTEGER NOT NULL,
            PRIMARY KEY (petition_code, UUAA, geography_id, dev_master),
            FOREIGN KEY (petition_code) REFERENCES Peticion(petition_code),
            FOREIGN KEY (UUAA, geography_id, dev_master) REFERENCES Power_Design(UUAA, geography_id, dev_master)
        )
    ''')

    conn.commit()
    conn.close()

def delete_database_tables_postgresql():
    conn = psycopg2.connect(
        dbname = "pwd_control", 
        user = "postgres",
        password = "Matias123!",
        host = "localhost",
        port = "5432"
    )

    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS UUAA")
    cursor.execute("DROP TABLE IF EXISTS Geography")
    cursor.execute("DROP TABLE IF EXISTS Power_Design")
    cursor.execute("DROP TABLE IF EXISTS Peticion")
    cursor.execute("DROP TABLE IF EXISTS Peticion_PWD")
    cursor.execute("DROP TABLE IF EXISTS Versions")

    conn.commit()
    conn.close()