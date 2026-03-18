# modulos/gestor_api.py
import json
import os
import customtkinter as ctk

ARCHIVO_CREDENCIALES = ".credenciales.json"

def cargar_api_key():
    """Busca si la API Key ya está guardada en el sistema."""
    if os.path.exists(ARCHIVO_CREDENCIALES):
        with open(ARCHIVO_CREDENCIALES, "r") as f:
            datos = json.load(f)
            return datos.get("spotify_api_key")
    return None

def guardar_api_key(key):
    """Guarda la API Key permanentemente en un archivo JSON."""
    with open(ARCHIVO_CREDENCIALES, "w") as f:
        json.dump({"spotify_api_key": key}, f)

def verificar_y_pedir_api():
    """Verifica la API. Si no existe, lanza un popup para pedirla."""
    key = cargar_api_key()
    
    if not key:
        # Crea un cuadro de diálogo nativo de CustomTkinter
        dialog = ctk.CTkInputDialog(
            text="Bienvenido.\nPor favor, ingresa tu API Key de Spotify para continuar:", 
            title="Configuración Inicial API"
        )
        key_ingresada = dialog.get_input()
        
        if key_ingresada:
            guardar_api_key(key_ingresada)
            print("// API Key guardada exitosamente.")
            return key_ingresada
        else:
            print("// ADVERTENCIA: No se ingresó API Key. Modo local activado.")
            return None
            
    return key
