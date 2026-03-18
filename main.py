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
        
        self.title("COLABORA MUSIC STATION // v0.1")
        
        # Ventana maximizada, pero con botones de control
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

        # Variables de estado
        self.bg_mode = "Color" 
        self.blur_radius = 15 # Valor fijo estético para el fondo
        
        # Cargar imagen base
        img_data = base64.b64decode(create_placeholder_pixel_image())
        self.base_cover_image = Image.open(io.BytesIO(img_data)).convert("RGBA")

        # --- CAPA 0: EL FONDO MAESTRO ---
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # --- CAPA 1: EL CONTENEDOR PRINCIPAL ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(side="top", fill="x", padx=20, pady=10)
        ctk.CTkLabel(header_frame, text="// MI ESTACIÓN DE COLABORACIÓN MUSICAL", font=(FONT_FAMILY, 24, "bold"), text_color=GREEN_TEXT).pack(anchor="w")

        # Grid
        self.content_grid = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_grid.pack(expand=True, fill="both")
        self.content_grid.grid_columnconfigure(0, weight=1)
        self.content_grid.grid_columnconfigure(1, weight=2)
        self.content_grid.grid_columnconfigure(2, weight=1)
        self.content_grid.grid_rowconfigure(0, weight=1)

        # Instanciar módulos
        self.panel_izquierdo = PanelIzquierdo(self.content_grid, app_master=self)
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=10)

        self.panel_central = PanelCentral(self.content_grid)
        self.panel_central.grid(row=0, column=1, sticky="nsew", padx=10)

        self.panel_derecho = PanelDerecho(self.content_grid)
        self.panel_derecho.grid(row=0, column=2, sticky="nsew", padx=10)

        # Transparencia general
        if os.name != "nt":
            self.attributes("-alpha", 0.70)

        # Optimizacion de arranque
        self.after(50, self.aplicar_fondo)

    # --- FUNCIONES EN TIEMPO REAL ---
    def cambiar_opacidad(self, valor):
        if os.name != "nt":
            self.attributes("-alpha", float(valor))

    def cambiar_modo_fondo(self, modo):
        self.bg_mode = modo
        self.aplicar_fondo()

    def aplicar_fondo(self):
        """Renderiza el fondo optimizando la resolución a la pantalla actual"""
        if self.bg_mode == "Color":
            self.bg_label.configure(image=None, fg_color=BG_COLOR)
        else:
            ancho_pantalla = self.winfo_screenwidth()
            alto_pantalla = self.winfo_screenheight()

            img = self.base_cover_image.resize((100, 100))
            if self.blur_radius > 0:
                img = img.filter(ImageFilter.GaussianBlur(self.blur_radius))
            
            img = img.resize((ancho_pantalla, alto_pantalla))
            
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(ancho_pantalla, alto_pantalla))
            self.bg_label.configure(image=ctk_img, fg_color="transparent")

if __name__ == "__main__":
    app = CollabMusicStation()
    app.mainloop()
