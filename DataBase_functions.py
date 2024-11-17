import sqlite3
import nbformat

import numpy as np
import pandas as pd 
import time

#Execute shell commands
import subprocess


def create_database():
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

    #Create a Geofraphy table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Geography (
            geography VARCHAR(50) PRIMARY KEY,
            DESCRIPTION VARCHAR(255)
        )
    ''')


    #Create a Versions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Versions (
            UUAA VARCHAR(4) NOT NULL,
            Geography_id INTEGER NOT NULL,
            version_id INTEGER NOT NULL,
            version integer NOT NULL,
            date date NOT NULL,
            description varchar(50) NOT NULL,
            PRIMARY KEY (version_id),
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA),
            FOREIGN KEY (geography) REFERENCES geography(geography), 
            INDEX (UUAA, geography)
        )
    ''')

    # Create a petición table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Peticion (
            petition_code VARCHAR(12) PRIMARY KEY,
            DQDP_code VARCHAR(12) NOT NULL,
            sdatool VARCHAR(12) NOT NULL,
            feature VARCHAR(12) NOT NULL,
            UUAA VARCHAR(4) NOT NULL,
            geography VARCHAR(50) NOT NULL,
            estado CHECK(estado IN ('Pendiente', 'En Proceso', 'Finalizado')) NOT NULL,
            fecha date NOT NULL,
            descripcion varchar(50) NOT NULL,
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA), 
            FOREIGN KEY (geography) REFERENCES geography(geography)
        )
    ''')

    # Create a Peticion_version table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Peticion_version (
            petition_code VARCHAR(12) NOT NULL,
            version_id INTEGER NOT NULL,
            PRIMARY KEY (petition_code, version_id),
            FOREIGN KEY (petition_code) REFERENCES Peticion(petition_code),
            FOREIGN KEY (version_id) REFERENCES Versions(version_id), 
        )
    ''')

    conn.commit()
    conn.close()

    def insert_data(petition_form)
        conn = sqlite3.connect("BBVA.db")
        cursor = conn.cursor()

        #if UUAA and geography already exists? 
        if not petition_from['UUAA'] in cursor.execute("SELECT UUAA FROM UUAA").fetchall():
            cursor.execute("INSERT INTO UUAA (UUAA, description) VALUES (?, ?)", (petition_form['UUAA']))
        if not petition_form['Geography'] in cursor.execute("SELECT geography FROM Geography").fetchall():
            cursor.execute("INSERT INTO Geography (geography) VALUES (?)", (petition_form['Geography']))



        conn.commit()
        conn.close()