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

    #Create a Geography table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Geography (
            geography_id INTEGER PRIMARY KEY,
            geography VARCHAR(64), 
            description VARCHAR(255)
        )
    ''')


    #Create a Power_Design table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Power_Design (
            combined_uuaa_geo_dema varchar(255) PRIMARY KEY,
            UUAA VARCHAR(4) NOT NULL,
            Geography_id INTEGER NOT NULL,
            dev_master CHECK(dev_master IN ('Dev', 'Master')) NOT NULL,
            version INTEGER NOT NULL,
            date DATE NOT NULL,
            description VARCHAR(255) NOT NULL,
            FOREIGN KEY (UUAA) REFERENCES UUAA(UUAA),
            FOREIGN KEY (geography_id) REFERENCES Geography(geography_id), 
            INDEX (UUAA, Geography_id, dev_master)
        )
    ''')
    # Create a trigger to update combined_uuaa_geo_dema
    CREATE TRIGGER IF NOT EXISTS update_combined_uuaa_geo_dema 
    AFTER INSERT ON Power_Design 
    FOR each ROW 
    BEGIN
        SET combined_uuaa_geo_dema = NEW.UUAA || '-' || NEW.Geography_id || '-' || NEW.dev_master 
        WHERE UUAA = NEW.UUAA AND Geography_id = NEW.Geography_id AND dev_master = NEW.dev_master; 
    END;
    
    CREATE TRIGGER IF NOT EXISTS update_combined_uuaa_geo_dema_on_update
    AFTER UPDATE OF UUAA, geography_id, dev_master ON Power_Design
    FOR EACH ROW
    BEGIN
        UPDATE Power_Design
        SET combined_uuaa_geo_dema = NEW.UUAA || '-' || NEW.geography_id || '-' || NEW.dev_master
        WHERE UUAA = NEW.UUAA AND geography_id = NEW.geography_id AND dev_master = NEW.dev_master;
    END;

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
            fecha_out DATE NOT NULL,
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
            combined_uuaa_geo_dema VARCHAR(255) NOT NULL,
            PRIMARY KEY (petition_code, combined_uuaa_geo_dema),
            FOREIGN KEY (combined_uuaa_geo_dema) REFERENCES Power_Design(combined_uuaa_geo_dema)
        )
    ''')

    conn.commit()
    conn.close()

    def insert_data(petition_form):
        conn = sqlite3.connect("BBVA.db")
        cursor = conn.cursor()

        #if UUAA and geography already exists? 
        if not petition_from['UUAA'] in cursor.execute("SELECT UUAA FROM UUAA").fetchall():
            cursor.execute("INSERT INTO UUAA (UUAA, description) VALUES (?, ?)", (petition_form['UUAA']))
        if not petition_form['Geography'] in cursor.execute("SELECT geography FROM Geography").fetchall():
            cursor.execute("INSERT INTO Geography (geography) VALUES (?)", (petition_form['Geography']))



        conn.commit()
        conn.close()