# main.py
import customtkinter as ctk
from PIL import Image, ImageFilter
import io
import base64
import os

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
        
        # 1. CARGAR CONFIGURACIÓN (MEMORIA)
        self.config_data = cargar_config()
        
        # 2. CONFIGURACIÓN DE VENTANA (MAXIMIZADA)
        self.title("COLABORA MUSIC STATION // v0.1")
        self.resizable(True, True)
        try:
            if os.name == "nt":
                self.state("zoomed")
            else:
                self.attributes("-zoomed", True)
        except Exception:
            ancho = self.winfo_screenwidth()
            alto = self.winfo_screenheight()
            self.geometry(f"{ancho}x{alto}+0+0")

        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=BG_COLOR)

        # 3. VARIABLES DE ESTADO (Desde la memoria)
        self.bg_mode = self.config_data.get("bg_mode", "Color")
        self.alpha_actual = self.config_data.get("alpha", 0.70)
        self.blur_radius = 15 # Valor estético fijo
        
        # Spotify Engine (Se inicializa como None)
        self.sp = None
        
        # Cargar imagen base (Placeholder)
        img_data = base64.b64decode(create_placeholder_pixel_image())
        self.base_cover_image = Image.open(io.BytesIO(img_data)).convert("RGBA")

        # --- CAPA 0: EL FONDO MAESTRO ---
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # --- CAPA 1: EL CONTENEDOR PRINCIPAL ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(side="top", fill="x", padx=20, pady=10)
        ctk.CTkLabel(header_frame, text="// MI ESTACIÓN DE COLABORACIÓN MUSICAL", 
                     font=(FONT_FAMILY, 24, "bold"), text_color=GREEN_TEXT).pack(anchor="w")

        # Grid de Contenido
        self.content_grid = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_grid.pack(expand=True, fill="both")
        self.content_grid.grid_columnconfigure(0, weight=1)
        self.content_grid.grid_columnconfigure(1, weight=2)
        self.content_grid.grid_columnconfigure(2, weight=1)
        self.content_grid.grid_rowconfigure(0, weight=1)

        # Instanciar Paneles
        self.panel_izquierdo = PanelIzquierdo(self.content_grid, app_master=self, config_inicial=self.config_data)
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=10)

        self.panel_central = PanelCentral(self.content_grid)
        self.panel_central.grid(row=0, column=1, sticky="nsew", padx=10)

        self.panel_derecho = PanelDerecho(self.content_grid)
        self.panel_derecho.grid(row=0, column=2, sticky="nsew", padx=10)

        # 4. APLICAR TRANSPARENCIA INICIAL
        if os.name != "nt":
            self.attributes("-alpha", self.alpha_actual)

        # 5. ARRANQUE OPTIMIZADO (Lazy Loading)
        self.after(100, self.aplicar_fondo)
        
        # 6. VERIFICAR CREDENCIALES SPOTIFY
        # Lanzamos el popup después de que la interfaz sea visible
        self.after(1000, self.inicializar_spotify)

    def inicializar_spotify(self):
        """Pide las llaves si no existen e intenta conectar"""
        self.config_data = verificar_api_key(self.config_data, self)
        
        if self.config_data.get("client_id") and self.config_data.get("client_secret"):
            self.sp = conectar_spotify(
                self.config_data["client_id"],
                self.config_data["client_secret"]
            )
            if self.sp:
                print("// Conexión con Spotify establecida exitosamente.")

    # --- FUNCIONES DE CONTROL EN TIEMPO REAL ---
    def cambiar_opacidad(self, valor):
        """Ajusta transparencia y guarda en memoria"""
        val_float = float(valor)
        if os.name != "nt":
            self.attributes("-alpha", val_float)
        
        self.config_data["alpha"] = val_float
        guardar_config(self.config_data)

    def cambiar_modo_fondo(self, modo):
        """Cambia modo de fondo y guarda en memoria"""
        self.bg_mode = modo
        self.aplicar_fondo()
        
        self.config_data["bg_mode"] = modo
        guardar_config(self.config_data)

    def aplicar_fondo(self):
        """Renderiza el fondo según el modo activo"""
        if self.bg_mode == "Color":
            self.bg_label.configure(image=None, fg_color=BG_COLOR)
        else:
            ancho_p = self.winfo_screenwidth()
            alto_p = self.winfo_screenheight()

            # Procesamiento rápido: imagen pequeña -> blur -> redimensionar
            img = self.base_cover_image.resize((100, 100))
            img = img.filter(ImageFilter.GaussianBlur(self.blur_radius))
            img = img.resize((ancho_p, alto_p))
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(ancho_p, alto_p))
            self.bg_label.configure(image=ctk_img, fg_color="transparent")

if __name__ == "__main__":
    app = CollabMusicStation()
    app.mainloop()
