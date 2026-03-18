# main.py
import customtkinter as ctk
from modulos.config import *
from modulos.panel_izquierdo import PanelIzquierdo
from modulos.panel_central import PanelCentral
from modulos.panel_derecho import PanelDerecho
import os

class CollabMusicStation(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración principal
        self.title("COLABORA MUSIC STATION // v0.1")
        self.geometry("1400x900")
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color=BG_COLOR)
        
        # --- EFECTO TRANSPARENCIA (Gnome) ---
        # Ajustado exactamente al 50% (0.50)
        if os.name != "nt":
             self.attributes("-alpha", 0.50) 

        # Header principal
        header_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        header_frame.pack(side="top", fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(header_frame, text="// MI ESTACIÓN DE COLABORACIÓN MUSICAL", font=(FONT_FAMILY, 24, "bold"), text_color=GREEN_TEXT).pack(anchor="w")
        ctk.CTkLabel(header_frame, text="// powered by Team Colab // v0.1-dev", font=(FONT_FAMILY, 14), text_color=MAGENTA_TEXT).pack(anchor="w")

        # Configurar Grid de 3 columnas
        self.main_container = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=2)
        self.main_container.grid_columnconfigure(2, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Instanciar e insertar módulos
        self.panel_izquierdo = PanelIzquierdo(self.main_container)
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=10)

        self.panel_central = PanelCentral(self.main_container)
        self.panel_central.grid(row=0, column=1, sticky="nsew", padx=10)

        self.panel_derecho = PanelDerecho(self.main_container)
        self.panel_derecho.grid(row=0, column=2, sticky="nsew", padx=10)

if __name__ == "__main__":
    api_key = None
    app = CollabMusicStation()
    app.mainloop()
