#!/usr/bin/env python
# coding: utf-8

# In[5]:


#%load_ext autoreload
get_ipython().run_line_magic('autoreload', '2')

import sqlite3
import psycopg2
import pandas as pd
import numpy as np
import math
import io
import json
from DataBase_functions import *

#Google sheed API
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


# <p style="font-size: 50px; text-align: center; color: #20a7e5;">Creating definitive data-frame</p>

# <p style="font-size: 25px; color: #208ee5">Registro actividad todos</p>

# In[ ]:


# Email service account that need to share the google sheet: matiasblaquier@theta-voyager-406314.iam.gserviceaccount.com
service_account_email = "matiasblaquier@theta-voyager-406314.iam.gserviceaccount.com" 

#Permisos que solicitará a la cuenta de google
scope = [
    'https://spreadsheets.google.com/feeds',        #Scope antiguo de Sheet API (v3)
    'https://www.googleapis.com/auth/spreadsheets', #Scope moderno de Sheet API (v4)
    'https://www.googleapis.com/auth/drive'         #Permisos para Google Drive
    ]

credentials = "credentials.json" #Credenciales del proyecto de Google Cloud

headers_definitive = ["Fecha de alta", "Fecha incurrida", "Fecha de fin", "UUAA", "Código", "SDATOOL", "Feature", "Petición", "Geografía", "Gestor BBDD", "Ámbito", "Responsable", "Validada", "Horas", "Comentarios", "version_date", "version", "petition_arq", "dev_master"]
try: 
    #Cargar credenciales
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)

    #Autorizar gspread con las credenciales
    client = gspread.authorize(creds)

    # ID de la hoja de cálculo 
    spreadsheet_id = ["1X6Mto2NH8iqmhV0LBkQJvBAZUG_Uvcj6PkCFN1s_xa0", "1mUJAhezlVOj2TVWBs3loo8C91aDWzqaYjboDysidpO0"] #[2025, 2024]  

    #Dataframe con los datos de todos los meses
    headers = ["Fecha de alta", "Fecha incurrida", "Fecha de fin", "UUAA", "Código", "SDATOOL", "Feature", "Petición", "Geografía", "Gestor BBDD", "Ámbito", "Responsable", "Validada", "Horas", "Comentarios"]
    df_rat = pd.DataFrame(columns=headers)
    for i in spreadsheet_id: 
        # Open the Google Sheet file by ID
        spreadsheet = client.open_by_key(i)

        # List all sheets file
        sheets = spreadsheet.worksheets()
        print(f"Available sheeds: {[sheet.title for sheet in sheets]}")
 
        meses = ["2025", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre", "Enero_25", "Febrero_25", "Marzo_25"]
        for sheet in sheets:
            sheet_name = sheet.title
            print(sheet_name) 
            sheet.update(values=[headers], range_name='A1')
            if sheet_name in meses:
                df_aux = pd.DataFrame(sheet.get_all_records(expected_headers=headers))
                df_rat = pd.concat([df_rat, df_aux], ignore_index=True)
            else: 
                print(sheet_name, "is not a month")
                pass
    #df = df.drop_duplicates(subset='Código', keep='first')
    df_rat = df_rat[headers] #Únicamente me quedo con las columnas que me interesa
    print(df_rat.shape, "\n", df_rat.columns)

    #Dataframe validation
    df_rat.rename(columns={"Validada": "validada", "Responsable": "responsable", "Gestor DDBB": "DDBB", "Geografía": "geography", "Petición": "petition_code", "Feature": "feature", "SDATOOL": "sdatool", "Código": "DQDP_code", "Gestor BBDD": "DDBB", "Horas": "duration_time", "Comentarios": "description", "Fecha de alta": "fecha_in", "Fecha de fin": "fecha_out"}, inplace=True)

    df_rat["fecha_in"] = df_rat["fecha_in"].astype(str)
    df_rat["Fecha incurrida"] = df_rat["Fecha incurrida"].astype(str)
    df_rat["fecha_out"] = df_rat["fecha_out"].astype(str)
    df_rat["UUAA"] = df_rat["UUAA"].astype(str)
    df_rat["DQDP_code"] = df_rat["DQDP_code"].astype(str)
    df_rat["sdatool"] = df_rat["sdatool"].astype(str)
    df_rat["feature"] = df_rat["feature"].astype(str)
    df_rat["geography"] = df_rat["geography"].astype(str)
    df_rat["DDBB"] = df_rat["DDBB"].astype(str)
    df_rat["Ámbito"] = df_rat["Ámbito"].astype(str)
    df_rat["responsable"] = df_rat["responsable"].astype(str)
    df_rat["validada"] = df_rat["validada"].astype(str)
    df_rat["duration_time"] = pd.to_numeric(df_rat["duration_time"], errors="coerce")
    df_rat["description"] = df_rat["description"].astype(str)
    df_rat["petition_code"] = df_rat["petition_code"].astype(str)

    df_rat["version_date"] = "Nan"
    df_rat["version"] = "Nan"
    df_rat["petition_arq"] = "Nan"
    df_rat["dev_master"] = "Nan"

except gspread.exceptions.APIError as e:
    print(f"APIError: {e}")

except Exception as e:
    print(f"Error: {e}")

print(df_rat, "\n", df_rat.columns)


# <p style="font-size: 35px; color: #208ee5;">Peticiones globales Oracle, Elastic Search y Mongo DB</p>

# <p style="font-size: 25px; color: #208cc5;;">Oracle Physics, Elastic Search, Mongo DB</p>

# In[ ]:


# Email service account that need to share the google sheet
service_account_email = "matiasblaquier@theta-voyager-406314.iam.gserviceaccount.com"
#email that need to share the google sheet = matiasblaquier@theta-voyager-406314.iam.gserviceaccount.com

scope = [
    'https://spreadsheets.google.com/feeds', 
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]

credentials = "credentials.json"

try: 
    #Cargar credenciales
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)

    #Autorizar gspread con las credenciales
    client = gspread.authorize(creds)

    # ID de la hoja de cálculo. #Oracle Physics, Elastic Search, Mongo DB v1, Mongo DB v2 
    spreadsheet_id = [
        "1cjUK1zR2pFzN7ev81AYrX9-Mc7x6haKEhfCQooeXAvM", # Oracle Physics
        "1Ax-27CgcSSjFdwy2JYZDn2DDksRb9VdJ2V5bzmIICt0", # Elastic Search
        "1xA2c48-yER2ltpg_6_aIG3pkrM389nFTgrpiCRCeQYI", # Mongo DB v1
        "18JsNWwD4HC9LBi7cga9uC1IleJG1ElgLIC1eK-NBHbk"  # Mongo DB v2
    ] 

    #DataFrame con los datos del excel
    headers = ["UUAA", "Petición Jira", "Versión Repo", "Petición ARQ", "Fecha cierre", "Path", "Comentarios"]
    df_globales = pd.DataFrame(columns=headers)
    for i in spreadsheet_id: 
        # Open the Google Sheet file by ID
        spreadsheet = client.open_by_key(i)

        # List all sheets file
        sheets = spreadsheet.worksheets()
        print(f"Available sheeds: {[sheet.title for sheet in sheets]}")

        for sheet in sheets: 
            try: 
                print(sheet.title)
                sheet.update(values=[headers], range_name='A1') #Nombrando las columnas

                df_aux = pd.DataFrame(sheet.get_all_records(expected_headers=headers))
                df_globales = pd.concat([df_globales, df_aux], ignore_index=True)
                print(df_globales.columns)
                #Poniendo el DDBB correspondiente
                if i == spreadsheet_id[0]: 
                    df_globales["DDBB"] = "Oracle Physics"
                elif i == spreadsheet_id[1]: 
                    df_globales.loc[df_globales["DDBB"] != "Oracle Physics", "DDBB"] = "Elastic Search"
                elif i == spreadsheet_id[2] or i == spreadsheet_id[3]: 
                    df_globales.loc[(df_globales["DDBB"] != "Oracle Physics") & (df_globales["DDBB"] != "Elastic Search"), "DDBB"] = "Mongo DB"
                else: 
                    print("Fuera de rango spreadsheet_id")

            except gspread.exceptions.APIError as e:
                if e.response.status_code == 429: 
                    wait_time = 6
                    print(f"Quota exceeded. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else: 
                    pass
            
    #Creating DDBB and geography column
    df_globales["geography"] = "Global"

    print(df_globales.shape)

    df_globales["UUAA"] = df_globales["UUAA"].astype(str)
    df_globales["Petición Jira"] = df_globales["Petición Jira"].astype(str)
    df_globales["Versión Repo"] = df_globales["Versión Repo"].astype(str)
    df_globales["Petición ARQ"] = df_globales["Petición ARQ"].astype(str)
    df_globales["Fecha cierre"] = df_globales["Fecha cierre"].astype(str)
    df_globales["Comentarios"] = df_globales["Comentarios"].astype(str)
    df_globales["Path"] = df_globales["Path"].astype(str)
    df_globales["DDBB"] = df_globales["DDBB"].astype(str)
    df_globales["geography"] = df_globales["geography"].astype(str)

    df_globales.rename(columns={"Path": "path", "Petición Jira": "petition_code", "Versión Repo": "version", "Petición ARQ": "petition_arq", "Fecha cierre": "fecha_out", "Comentarios": "description"}, inplace=True)
    df_globales = df_globales[["petition_code", "version", "petition_arq", "fecha_out", "description", "path", "UUAA", "DDBB", "geography"]]
except gspread.exceptions.APIError as e:
    print(f"APIError: {e}")

except Exception as e:
    print(f"Error: {e}")

print(df_globales.columns, df_globales.shape)


# <p style="font-size: 35px; color: #208ee5;">dqdp_portal CSV</p>

# In[8]:


# Email service account that need to share the google sheet
service_account_email = "matiasblaquier@theta-voyager-406314.iam.gserviceaccount.com"
#email that need to share the google sheet = matiasblaquier@theta-voyager-406314.iam.gserviceaccount.com

scope = [
    'https://spreadsheets.google.com/feeds', 
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]

credentials = "credentials.json"

creds = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)

service = build('drive', 'v3', credentials=creds)

#Drive, folder id
folder_id = '1w2V9GaUCXD4vdjolQjIAEMujMOiqYwEP'

#list of archives
results = service.files().list(
    q = f"'{folder_id}' in parents", 
    pageSize=120, 
    fields = "nextPageToken, files(id, name)"
).execute()
files = results.get('files', [])

#List that can take all dataframe from csv files
dfs = []

# Itera sobre los archivos y lee los CSV
for file in files:
    if file['name'].endswith('.csv'): # Solo procesa archivos CSV
        file_id = file['id']
        print(file['name'])
        # Descarga el archivo CSV a un archivo temporal
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO() # Usamos un archivo en memoria para no guardar el archivo
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        fh.seek(0) # Reiniciar el puntero al inicio del archivo
        try:
            df_aux = pd.read_csv(fh) # Lee el CSV con Pandas
            dfs.append(df_aux)
        except Exception as e:
            print(f"Error al leer el archivo {file['name']}: {e}")

# Combina todos los DataFrames en uno solo
df_csv_combined = pd.concat(dfs, ignore_index=True)


# In[9]:


print(df_csv_combined.columns)
df_csv_combined.rename(columns={'Código': 'DQDP_code', 'Responsable': 'responsable', 'Fecha de alta': 'fecha_in', 'Petición': 'petition_code', 'Geografía': 'geography', 'Horas esfuerzo': 'duration_time', 'Gestor': 'DDBB', 'Fecha fin': 'fecha_out'}, inplace=True)
df_csv_combined['description'] = df_csv_combined['Descripción corta'] + '\n' + df_csv_combined['Descripción']
df_csv_combined = df_csv_combined[['DQDP_code', 'UUAA', 'responsable', 'fecha_in', 'petition_code', 'geography', 'duration_time', 'DDBB', 'description']]

df_csv_combined.columns


# <p style="font-size: 35px; color: #20cff5; text-align: center;">All in one Data Frame</p>

# In[10]:


print("Data-frame from CSV files: ", df_csv_combined.columns, "\n", "Data-frame from Registro Actividad Todos: ", df_rat.columns, "\n", "Data-frame from Globales: ", df_globales.columns)
print(set(df_csv_combined.columns) & set(df_rat.columns) & set(df_globales.columns))


# In[11]:


#Creating global data-frame
df_combined = pd.DataFrame(columns=list(df_rat.columns))
df_combined = pd.concat([df_combined, df_rat, df_globales, df_csv_combined], ignore_index=True)
print(df_combined.columns)

columns_to_use = ["fecha_in", "fecha_out", "UUAA","sdatool", "feature",  "DQDP_code", "geography", "DDBB", "Ámbito", "responsable", "validada", "description", "version_date", "version", "petition_arq", "petition_code", "duration_time", "dev_master"]
df_combined = df_combined[columns_to_use]

for column in columns_to_use: 
    df_combined[column] = df_combined[column].astype(str)

df_combined["duration_time"] = pd.to_numeric(df_combined["duration_time"], errors="coerce")
df_combined["dev_master"] = "None"

#Poniendo "None" o np.nan donde corresponde


for row in df_combined.iterrows(): 
    for key, value in dict(row[1]).items():
        if value == "Nan" or value == None or value == "" or value == "nan" or value == "None" or value == "none" or value == "NONE" or value == np.nan: 
            if key == "duration_time": #Numeric columns
                df_combined.at[row[0], key] = np.nan
            else:
                df_combined.at[row[0], key] = "None"



df_combined = df_combined[df_combined["petition_code"] != "None"]

agg_dict = {
    col: 'first' for col in df_combined.columns if col not in ["description", "duration_time"]
}
agg_dict['description'] = lambda x: "\n".join(x.astype(str))
agg_dict["duration_time"] = 'sum'

#Data frame final a partir del campo 'poetition_code'
#df_g.drop_duplicates(subset=["petition_code"], keep="first", inplace=True) #Método 1
final_df = df_combined.groupby("petition_code", as_index=False).agg(agg_dict) #Método 2


# <p>Nan counting</p>

# In[12]:


petitions = set(final_df["petition_code"])
print(len(petitions), final_df.columns)

#Poniendo "None" o None donde corresponda
for petition in petitions: 
    dic_aux = {i: [] for i in columns_to_use}

    for column in columns_to_use: 
        df_filtered = final_df[final_df["petition_code"] == petition]
        
        if not df_filtered.empty: 
            df_value = df_filtered[column].values[0]
        else: 
            df_value = "None" if column != "duration_time" else None
        
        if df_value != "None" and df_value is not None: 
            dic_aux[column].append(df_value)
        else:
            dic_aux[column].append(df_value) #None o "None"

    df_aux = pd.DataFrame(dic_aux)
    final_df = pd.concat([final_df, df_aux], ignore_index=True)

agg_dict = {
col: 'first' for col in final_df.columns if col not in ["description", "duration_time"]
}
agg_dict['description'] = lambda x: "\n".join(x.astype(str))
agg_dict["duration_time"] = 'sum'
final_df = final_df.groupby("petition_code", as_index=False).agg(agg_dict)

#Contar los valores "None" o None
df_none_count = {i: 0 for i in list(final_df.columns)}
for row in final_df.iterrows(): 
    for key, value in dict(row[1]).items():
        if value == "None" or value == None or (isinstance(value, float) and np.isnan(value)):
            df_none_count[key] += 1
        else: 
            pass
print(final_df.shape, final_df.shape, final_df.shape)
df_none_count


# ---
# ---

# <p style="font-size: 45px; text-align: center; color: green;">Cleaning definitive dataframe</p>

# In[13]:


print(final_df["geography"].unique())
print(final_df["DDBB"].unique())
#final_df.drop(columns=['', 'path'], inplace=True)
print(final_df.columns)


# In[14]:


final_df["DDBB"] = final_df["DDBB"].replace(["DB2 HOST"], "DB2 Host")
final_df["DDBB"] = final_df["DDBB"].replace(["ORACLE Physics"], "Oracle Physics")
final_df["DDBB"] = final_df["DDBB"].replace(["ELASTICSEARCH", "ElasTICSEARCH", "ElaSTICSEARCH"], "Elastic Search")
final_df["DDBB"] = final_df["DDBB"].replace(["ORACLE R2", "oracle r2"], "Oracle R2")
final_df["DDBB"] = final_df["DDBB"].replace(["teradata", "TERADATA"], "Teradata")
final_df["DDBB"] = final_df["DDBB"].replace(["MongoDB", "MONGO DB", "MongoDB", "MONGODB", "Mongo\t", "Mongo"], "Mongo DB")
final_df["DDBB"] = final_df["DDBB"].replace(["POSTGRESS R2", "POSTGRESS Physics", "PosgreSQL"], "PostgreSQL")
final_df["DDBB"] = final_df["DDBB"].replace(["NETEZZA"], "Netezza")

final_df["geography"] = final_df["geography"].replace(["España/CIB", "España-CIB"], "CIB")
final_df["geography"] = final_df["geography"].replace(["España "], "España")


# In[15]:


final_df["fecha_in"] = final_df["fecha_in"].astype(str)
#final_df["Fecha incurrida"] = final_df["Fecha incurrida"].astype(str)
final_df["fecha_out"] = final_df["fecha_out"].astype(str)
final_df["UUAA"] = final_df["UUAA"].astype(str)
final_df["DQDP_code"] = final_df["DQDP_code"].astype(str)
final_df["sdatool"] = final_df["sdatool"].astype(str)
final_df["feature"] = final_df["feature"].astype(str)
final_df["petition_code"] = final_df["petition_code"].astype(str)
final_df["geography"] = final_df["geography"].astype(str)
final_df["DDBB"] = final_df["DDBB"].astype(str)
final_df["responsable"] = final_df["responsable"].astype(str)
final_df["version"] = final_df["version"].astype(str)
final_df["petition_arq"] = final_df["petition_arq"].astype(str)
final_df["dev_master"] = final_df["dev_master"].astype(str)
final_df["path"] = final_df["dev_master"].astype(str)
final_df["description"] = final_df["description"].astype(str)
final_df["duration_time"] = pd.to_numeric(final_df["duration_time"], errors="coerce")


# ---

# <p style="font-size: 25px; color: #00d17f;">Actualizar y guardar</p>

# In[16]:


#Actualizar y guardar

# Email service account that need to share the google sheet
service_account_email = "matiasblaquier@theta-voyager-406314.iam.gserviceaccount.com"
#email that need to share the google sheet = matiasblaquier@theta-voyager-406314.iam.gserviceaccount.com

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

set_with_dataframe(worksheet, final_df, include_index=False, include_column_header=True, resize=True)

###############################################################################################################
#Guardo el df en un excel en la carpeta actual
final_df.to_excel("petitions.xlsx", index=False, sheet_name="All petitions")


# In[17]:


final_df.columns


# ---
# ---

# In[18]:


for row in final_df.iterrows():
    try: 
        insert_data(dict(row[1]))
    except gspread.exceptions.APIError as e:
        if e.response.status_code == 429: 
            wait_time = 6
            print(f"Quota exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else: 
            pass


# <p style="font-size: 40px; color: grey;">Testing</p>

# In[19]:


conn1 = sqlite3.connect("BBVA.db")
cursor1 = conn1.cursor()
cursor1.execute("PRAGMA foreign_keys = ON") #In sqlite3 foreign keys are disabled by default

#######
cursor1.execute("SELECT UUAA FROM UUAA")
all_uuaa = [x[0] for x in cursor1.fetchall()]

#######
conn1.commit()
cursor1.close()
conn1.close()


# In[20]:


'''
conn3 =  psycopg2.connect(
        dbname = "pwd_control_plnk", 
        user = "matublaq",
        password = "SF19KOpSPMl8Ru51ONQ33AHOf0RuZnne", 
        host = "dpg-ctevf3t6l47c73b4jadg-a.oregon-postgres.render.com",
        port = "5432"
)   
cursor3 = conn3.cursor()

##########


##########
conn3.commit()
cursor3.close()
conn3.close()
'''


# In[21]:


print(len(all_uuaa))
all_uuaa


# In[ ]:




