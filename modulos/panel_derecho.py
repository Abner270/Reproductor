# modulos/panel_derecho.py
import customtkinter as ctk
from PIL import Image
import base64
import io
from .config import *
from .utilidades import create_placeholder_pixel_image

class PanelDerecho(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", border_width=0, **kwargs)
        self._construir_ui()

    def _construir_ui(self):
        # --- 1. IMAGEN DEL JAM (NUEVO TAMAÑO GIGANTE) ---
        img_frame = ctk.CTkFrame(self, fg_color="transparent")
        img_frame.pack(fill="x", pady=(0, 10)) 
        
        img_data = base64.b64decode(create_placeholder_pixel_image())
        img = Image.open(io.BytesIO(img_data))
        
        # --- TAMAÑO MAXIMIZADO PARA PANTALLA COMPLETA: 350x350 ---
        self.jam_image = ctk.CTkImage(light_image=img, dark_image=img, size=(350, 350)) 
        
        ctk.CTkLabel(img_frame, image=self.jam_image, text="").pack(pady=10)

        # --- 2. EL JAM ---
        ctk.CTkLabel(self, text="EL JAM CURATED QUEUE", font=(FONT_FAMILY, 16, "bold"), text_color=MAGENTA_TEXT).pack(anchor="w", pady=0)
        ctk.CTkLabel(self, text="// Tracks for Colab Funk", font=(FONT_FAMILY, 12, "bold"), text_color=GREEN_TEXT).pack(anchor="w", pady=(0, 5))
        
        jam_tracks = [
            "1: SynthRider - Orbital Vector", 
            "2: CyberFunk - Circuit Breaker",
            "3: NeonGhost - Pulse Code"
        ]
        
        jam_list_frame = ctk.CTkFrame(self, fg_color="#111111", corner_radius=5)
        jam_list_frame.pack(anchor="w", pady=(0, 15), fill="x", ipadx=5, ipady=5) 
        
        for track in jam_tracks:
            ctk.CTkLabel(jam_list_frame, text=track, font=(FONT_FAMILY, 11), text_color=MAGENTA_TEXT).pack(anchor="w", pady=1)
                
        # --- 3. SIGUIENTES REPRODUCCIONES ---
        ctk.CTkLabel(self, text="SIGUIENTES REPRODUCCIONES //", font=(FONT_FAMILY, 14, "bold"), text_color=GREEN_TEXT).pack(anchor="w", pady=(0, 5))
        
        upcoming_tracks = [f"{i}: CyberPunk - Track {i}" for i in range(4, 25)]
        
        upcoming_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", width=280)
        upcoming_frame.pack(anchor="w", fill="both", expand=True)
        
        for track in upcoming_tracks:
            ctk.CTkLabel(upcoming_frame, text=track, font=(FONT_FAMILY, 11), text_color=GREEN_TEXT).pack(anchor="w", pady=1)
