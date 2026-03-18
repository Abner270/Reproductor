# main.py
import customtkinter as ctk
from PIL import Image, ImageFilter
import io
import os
import threading
import requests
import base64

# Importación de módulos propios
from modulos.config import *
from modulos.panel_izquierdo import PanelIzquierdo
from modulos.panel_central import PanelCentral
from modulos.panel_derecho import PanelDerecho
from modulos.panel_progreso import PanelProgreso
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
            if os.name == "nt": self.state("zoomed")
            else: self.attributes("-zoomed", True)
        except Exception: self.geometry("1280x720")

        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=BG_COLOR)

        # 3. VARIABLES DE ESTADO
        self.bg_mode = self.config_data.get("bg_mode", "Color")
        self.blur_radius = 40
        self.sp = None
        
        placeholder_raw = base64.b64decode(create_placeholder_pixel_image())
        self.base_cover_image = Image.open(io.BytesIO(placeholder_raw))

        # 4. CAPA DE FONDO
        self.bg_label = ctk.CTkLabel(self, text="", image=None)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # 5. CONTENEDOR DE PANELES (Superior)
        self.content_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.content_grid.pack(expand=True, fill="both") 
        
        self.content_grid.grid_columnconfigure(0, weight=1) 
        self.content_grid.grid_columnconfigure(1, weight=3) 
        self.content_grid.grid_columnconfigure(2, weight=2) 
        self.content_grid.grid_rowconfigure(0, weight=1)

        # 6. INICIALIZAR PANELES
        self.panel_izquierdo = PanelIzquierdo(self.content_grid, self, self.config_data)
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.panel_central = PanelCentral(self.content_grid, app=self)
        self.panel_central.grid(row=0, column=1, sticky="nsew", padx=10, pady=20)

        self.panel_derecho = PanelDerecho(self.content_grid)
        self.panel_derecho.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)

        # --- LA BARRA INFERIOR GLOBAL ---
        self.player_bar = PanelProgreso(self, app_master=self)
        self.player_bar.pack(side="bottom", fill="x")

        # 7. CONEXIÓN Y ARRANQUE
        self.config_data = verificar_api_key(self.config_data, self)
        if self.config_data.get("client_id") and self.config_data.get("client_secret"):
            self.sp = conectar_spotify(self.config_data["client_id"], self.config_data["client_secret"])
            if self.sp:
                print("// Spotify conectado.")
                self.actualizar_loop_imagenes()   # Bucle lento (imágenes)
                self.actualizar_estado_reproduccion() # Tu bucle rápido (tiempo)

        self.attributes("-alpha", self.config_data.get("alpha", 0.70))
        self.aplicar_fondo()

    # --- BUCLE DE IMÁGENES (Cada 4 segundos) ---
    def actualizar_loop_imagenes(self):
        threading.Thread(target=self._hilo_imagenes, daemon=True).start()
        self.after(4000, self.actualizar_loop_imagenes)

    def _hilo_imagenes(self):
        try:
            if not self.sp: return
            track = self.sp.current_user_playing_track()
            if track and track['item']:
                url_img = track['item']['album']['images'][0]['url']
                response = requests.get(url_img, timeout=5)
                img_raw = Image.open(io.BytesIO(response.content))
                queue = self.sp.queue()
                
                self.after(0, lambda: self._refrescar_visuales(img_raw, queue))
        except: pass

    def _refrescar_visuales(self, img, queue_data):
        # Actualiza portada central
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 400))
        self.panel_central.label_imagen.configure(image=ctk_img)
        
        # Actualiza cola derecha
        self.panel_derecho.actualizar_datos(queue_data, img)
        
        # Actualiza fondo
        self.base_cover_image = img
        if self.bg_mode == "Cover": self.aplicar_fondo()

    # --- TU FUNCIÓN DE ESTADO (Cada 1 segundo) ---
    def actualizar_estado_reproduccion(self):
        if self.sp:
            try:
                track = self.sp.current_user_playing_track()
                if track:
                    nombre = track['item']['name']
                    artista = track['item']['artists'][0]['name']
                    ms_total = track['item']['duration_ms']
                    ms_actual = track['progress_ms']
                    
                    # Actualizamos la barra inferior
                    self.player_bar.actualizar_datos(nombre, artista, ms_actual, ms_total)
                    
                    # Sincronizamos el texto del panel central
                    self.panel_central.label_info.configure(text=f"  '{nombre}' // {artista}")
            except:
                pass
        
        # Se repite cada segundo
        self.after(1000, self.actualizar_estado_reproduccion)

    # --- MÉTODOS DE CONFIGURACIÓN ---
    def cambiar_opacidad(self, valor):
        self.attributes("-alpha", float(valor))
        self.config_data["alpha"] = float(valor)
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
            ancho_p = self.winfo_screenwidth()
            alto_p = self.winfo_screenheight()
            img = self.base_cover_image.resize((100, 100))
            img = img.filter(ImageFilter.GaussianBlur(self.blur_radius))
            img = img.resize((ancho_p, alto_p))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(ancho_p, alto_p))
            self.bg_label.configure(image=ctk_img)

if __name__ == "__main__":
    app = CollabMusicStation()
    app.mainloop()
