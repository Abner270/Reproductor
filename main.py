# main.py
import customtkinter as ctk
from PIL import Image, ImageFilter
import io
import os
import threading
import requests
import base64 # Importación corregida

# Importación de módulos propios
from modulos.config import *
from modulos.panel_izquierdo import PanelIzquierdo
from modulos.panel_central import PanelCentral
from modulos.panel_derecho import PanelDerecho
from modulos.utilidades import create_placeholder_pixel_image
from modulos.gestor_config import cargar_config, guardar_config, verificar_api_key
from modulos.spotify_engine import conectar_spotify

class CollabMusicStation(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. CARGAR CONFIGURACIÓN
        self.config_data = cargar_config()
        
        # 2. CONFIGURACIÓN DE VENTANA
        self.title("COLABORA MUSIC STATION // v0.1")
        try:
            if os.name == "nt":
                self.state("zoomed")
            else:
                self.attributes("-zoomed", True)
        except Exception:
            self.geometry("1280x720")

        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=BG_COLOR)

        # 3. VARIABLES DE ESTADO
        self.bg_mode = self.config_data.get("bg_mode", "Color")
        self.blur_radius = 40
        self.sp = None
        
        # Imagen base inicial (Placeholder corregido)
        placeholder_raw = base64.b64decode(create_placeholder_pixel_image())
        self.base_cover_image = Image.open(io.BytesIO(placeholder_raw))

        # 4. CAPA DE FONDO
        self.bg_label = ctk.CTkLabel(self, text="", image=None)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # 5. CONFIGURACIÓN DE COLUMNAS
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=3) 
        self.grid_columnconfigure(2, weight=2) 
        self.grid_rowconfigure(0, weight=1)

        # 6. INICIALIZAR PANELES
        # Panel Izquierdo
        self.panel_izquierdo = PanelIzquierdo(self, self, self.config_data, width=300)
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Panel Central (Referencia app=self añadida para evitar errores de master)
        self.panel_central = PanelCentral(self, app=self, width=600)
        self.panel_central.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)

        # Panel Derecho
        self.panel_derecho = PanelDerecho(self, width=400)
        self.panel_derecho.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)

        # 7. CONEXIÓN Y BUCLE
        self.config_data = verificar_api_key(self.config_data, self)
        if self.config_data.get("client_id") and self.config_data.get("client_secret"):
            self.sp = conectar_spotify(self.config_data["client_id"], self.config_data["client_secret"])
            if self.sp:
                print("// Conexión con Spotify establecida exitosamente.")
                self.actualizar_loop()

        # Aplicar transparencia y fondo inicial
        self.attributes("-alpha", self.config_data.get("alpha", 0.70))
        self.aplicar_fondo()

    # --- LÓGICA DE ACTUALIZACIÓN ---

    def actualizar_loop(self):
        """Refresco constante cada 4 segundos"""
        threading.Thread(target=self.obtener_datos_spotify, daemon=True).start()
        self.after(4000, self.actualizar_loop)

    def obtener_datos_spotify(self):
        """Hilo secundario para no congelar la app"""
        try:
            if not self.sp: return
            
            track = self.sp.current_user_playing_track()
            queue = self.sp.queue()
            
            if track and track['item']:
                item = track['item']
                nombre = item['name']
                artista = item['artists'][0]['name']
                url_img = item['album']['images'][0]['url']
                ms_actual = track['progress_ms']
                ms_total = item['duration_ms']

                # Descargar imagen
                response = requests.get(url_img, timeout=5)
                img_raw = Image.open(io.BytesIO(response.content))
                
                # Volver al hilo principal para tocar la UI
                self.after(0, lambda: self.refrescar_interfaz(nombre, artista, img_raw, ms_actual, ms_total, queue))
        except Exception as e:
            print(f"// Error en obtención de datos: {e}")

    def refrescar_interfaz(self, nombre, artista, img, ms_actual, ms_total, queue_data):
        """Actualiza todos los elementos visuales"""
        # Actualizar Panel Central
        if hasattr(self.panel_central, 'label_info'):
            self.panel_central.label_info.configure(text=f"  '{nombre}' // {artista}")
        
        if hasattr(self.panel_central, 'label_imagen'):
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 400))
            self.panel_central.label_imagen.configure(image=ctk_img)
            self.panel_central.label_imagen.image = ctk_img

        # Actualizar Progreso
        if hasattr(self.panel_central, 'panel_progreso'):
            self.panel_central.panel_progreso.actualizar_progreso(ms_actual, ms_total)

        # Actualizar Panel Derecho
        if hasattr(self.panel_derecho, 'actualizar_datos'):
            self.panel_derecho.actualizar_datos(queue_data, img)

        # Fondo dinámico
        self.base_cover_image = img
        if self.bg_mode == "Cover":
            self.aplicar_fondo()

    # --- MÉTODOS DE CONTROL ---

    def cambiar_opacidad(self, valor):
        val_float = float(valor)
        self.attributes("-alpha", val_float)
        self.config_data["alpha"] = val_float
        guardar_config(self.config_data)

    def cambiar_modo_fondo(self, modo):
        self.bg_mode = modo
        self.aplicar_fondo()
        self.config_data["bg_mode"] = modo
        guardar_config(self.config_data)

    def aplicar_fondo(self):
        if self.bg_mode == "Color":
            self.bg_label.configure(image=None, fg_color=BG_COLOR)
        else:
            # Procesamiento de desenfoque
            ancho_p = self.winfo_screenwidth()
            alto_p = self.winfo_screenheight()

            img = self.base_cover_image.resize((150, 150)) # Resize pequeño para velocidad
            img = img.filter(ImageFilter.GaussianBlur(self.blur_radius))
            img = img.resize((ancho_p, alto_p))
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(ancho_p, alto_p))
            self.bg_label.configure(image=ctk_img)
            self.bg_label.image = ctk_img

if __name__ == "__main__":
    app = CollabMusicStation()
    app.mainloop()
