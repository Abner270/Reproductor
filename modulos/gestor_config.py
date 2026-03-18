# modulos/gestor_config.py
import json
import os
import customtkinter as ctk

ARCHIVO_CONFIG = ".config_estacion.json"

def cargar_config():
    if os.path.exists(ARCHIVO_CONFIG):
        try:
            with open(ARCHIVO_CONFIG, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "client_id": None, 
        "client_secret": None,
        "alpha": 0.70, 
        "bg_mode": "Color"
    }

def guardar_config(datos):
    with open(ARCHIVO_CONFIG, "w") as f:
        json.dump(datos, f)

def verificar_api_key(datos, app_master):
    # Si falta alguna de las dos llaves, lanzamos los popups
    if not datos.get("client_id") or not datos.get("client_secret"):
        id_dialog = ctk.CTkInputDialog(text="Pega tu Client ID de Spotify:", title="Configuración Spotify")
        client_id = id_dialog.get_input()
        
        secret_dialog = ctk.CTkInputDialog(text="Pega tu Client Secret de Spotify:", title="Configuración Spotify")
        client_secret = secret_dialog.get_input()
        
        if client_id and client_secret:
            datos["client_id"] = client_id
            datos["client_secret"] = client_secret
            guardar_config(datos)
            print("// Credenciales de Spotify vinculadas.")
            
    return datos
