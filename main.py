# main.py
import customtkinter as ctk
from PIL import Image, ImageFilter
import io
import base64
import os

from modulos.config import *
from modulos.panel_izquierdo import PanelIzquierdo
from modulos.panel_central import PanelCentral
from modulos.panel_derecho import PanelDerecho
from modulos.utilidades import create_placeholder_pixel_image

class CollabMusicStation(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw() # Ocultar mientras carga

        self.title("COLABORA MUSIC STATION // v0.1")
        self.geometry("1400x900")
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=BG_COLOR)

        # Variables de estado del fondo
        self.bg_mode = "Color"
        self.blur_radius = 5
        
        # Cargar la imagen del "Cover" (usamos el pixel art como ejemplo)
        img_data = base64.b64decode(create_placeholder_pixel_image())
        self.base_cover_image = Image.open(io.BytesIO(img_data)).convert("RGBA")

        # --- CAPA 0: EL FONDO MAESTRO ---
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # --- CAPA 1: EL CONTENEDOR PRINCIPAL (Transparente) ---
        # Hacemos el contenedor transparente para que se vea el fondo
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Header principal
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(side="top", fill="x", padx=20, pady=10)
        ctk.CTkLabel(header_frame, text="// MI ESTACIÓN DE COLABORACIÓN MUSICAL", font=(FONT_FAMILY, 24, "bold"), text_color=GREEN_TEXT).pack(anchor="w")

        # Grid de 3 columnas
        self.content_grid = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_grid.pack(expand=True, fill="both")
        self.content_grid.grid_columnconfigure(0, weight=1)
        self.content_grid.grid_columnconfigure(1, weight=2)
        self.content_grid.grid_columnconfigure(2, weight=1)
        self.content_grid.grid_rowconfigure(0, weight=1)

        # Instanciar módulos (Fíjate que le pasamos 'self' al panel izquierdo)
        self.panel_izquierdo = PanelIzquierdo(self.content_grid, app_master=self)
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=10)

        self.panel_central = PanelCentral(self.content_grid)
        self.panel_central.grid(row=0, column=1, sticky="nsew", padx=10)

        self.panel_derecho = PanelDerecho(self.content_grid)
        self.panel_derecho.grid(row=0, column=2, sticky="nsew", padx=10)

        # Aplicar valores iniciales
        self.aplicar_fondo()
        if os.name != "nt":
            self.attributes("-alpha", 0.70)
            
        self.deiconify() # Mostrar ventana

    # --- FUNCIONES EN TIEMPO REAL ---
    def cambiar_opacidad(self, valor):
        """Ajusta la transparencia de la ventana en GNOME"""
        if os.name != "nt":
            self.attributes("-alpha", float(valor))

    def cambiar_modo_fondo(self, modo):
        """Cambia entre color solido y la imagen de la canción"""
        self.bg_mode = modo
        self.aplicar_fondo()

    def cambiar_blur(self, valor):
        """Ajusta el nivel de desenfoque (solo visible en modo Cover)"""
        self.blur_radius = float(valor)
        if self.bg_mode == "Cover":
            self.aplicar_fondo()

    def aplicar_fondo(self):
        """Renderiza el fondo según la configuración actual"""
        if self.bg_mode == "Color":
            self.bg_label.configure(image="", fg_color=BG_COLOR)
        else:
            # Truco de rendimiento: Reducimos la imagen drásticamente, la desenfocamos y la ampliamos.
            # Esto hace que el blur se aplique a 60 FPS sin trabar la interfaz.
            img = self.base_cover_image.resize((100, 100))
            if self.blur_radius > 0:
                img = img.filter(ImageFilter.GaussianBlur(self.blur_radius))
            
            # Ampliamos al tamaño de la ventana
            img = img.resize((1400, 900))
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(1400, 900))
            self.bg_label.configure(image=ctk_img, fg_color="transparent")

if __name__ == "__main__":
    app = CollabMusicStation()
    app.mainloop()
