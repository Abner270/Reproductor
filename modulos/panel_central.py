# modulos/panel_central.py
import customtkinter as ctk
from PIL import Image
from .config import *

class PanelCentral(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, fg_color="transparent", border_width=0, **kwargs)
        self.app = app 
        self.view_state = "image" # Estado inicial: viendo la portada
        self._construir_ui()

    def _construir_ui(self):
        # 1. Cabecera de información
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        self.label_info = ctk.CTkLabel(title_frame, text="Cargando Spotify...", font=(FONT_FAMILY, 16), text_color=MAGENTA_TEXT)
        self.label_info.pack(side="left")

        # 2. Contenedor principal para contenido intercambiable
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", pady=20)

        # Vista de Imagen (Portada)
        self.label_imagen = ctk.CTkLabel(self.container, text="", fg_color="transparent")
        self.label_imagen.pack(expand=True, fill="both")

        # Vista de Letras (Oculta por defecto)
        self.lyrics_frame = ctk.CTkScrollableFrame(self.container, fg_color="#0a0a0a", corner_radius=10)
        self.lbl_lyrics = ctk.CTkLabel(self.lyrics_frame, text="Letras no disponibles aún...", 
                                      font=(FONT_FAMILY, 18), text_color="white", justify="left")
        self.lbl_lyrics.pack(pady=20, padx=20)

    def toggle_lyrics_image(self):
        """Función que faltaba y causaba el error"""
        if self.view_state == "image":
            # Cambiar a Letras
            self.label_imagen.pack_forget()
            self.lyrics_frame.pack(expand=True, fill="both")
            self.view_state = "lyrics"
            print("// Vista: Letras")
        else:
            # Cambiar a Imagen
            self.lyrics_frame.pack_forget()
            self.label_imagen.pack(expand=True, fill="both")
            self.view_state = "image"
            print("// Vista: Portada")

    # --- Métodos de control de Spotify ---
    def play_music(self):
        if self.app.sp:
            try: self.app.sp.start_playback()
            except: print("// Error en Play")

    def pause_music(self):
        if self.app.sp:
            try: self.app.sp.pause_playback()
            except: print("// Error en Pause")

    def next_track(self):
        if self.app.sp:
            try: self.app.sp.next_track()
            except: print("// Error en Next")

    def prev_track(self):
        if self.app.sp:
            try: self.app.sp.previous_track()
            except: print("// Error en Prev")
