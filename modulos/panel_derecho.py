# modulos/panel_derecho.py
import customtkinter as ctk
from .config import *

class PanelDerecho(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BG_COLOR, border_width=0, **kwargs)
        self._construir_ui()

    def _construir_ui(self):
        ctk.CTkLabel(self, text="EL JAM CURATED QUEUE", font=(FONT_FAMILY, 18, "bold"), text_color=MAGENTA_TEXT).pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(self, text="// Tracks for Colab Funk", font=(FONT_FAMILY, 14, "bold"), text_color=GREEN_TEXT).pack(anchor="w", pady=(0, 5))
        
        # Jam Tracks
        jam_tracks = [
            "1: SynthRider - Orbital Vector", "2: CyberFunk - Circuit Breaker",
            "3: NeonGhost - Pulse Code", "4: FutureWave - Binary Sea"
        ]
        
        jam_list_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        jam_list_frame.pack(anchor="w", pady=(0, 20), fill="x")
        
        for track in jam_tracks:
            ctk.CTkLabel(jam_list_frame, text=track, font=(FONT_FAMILY, 12), text_color=MAGENTA_TEXT).pack(anchor="w", pady=1)
                
        # Siguientes Reproducciones
        ctk.CTkLabel(self, text="SIGUIENTES REPRODUCCIONES //", font=(FONT_FAMILY, 16, "bold"), text_color=GREEN_TEXT).pack(anchor="w", pady=(0, 10))
        
        upcoming_tracks = [
            f"{i}: CyberPunk - Track {i}" for i in range(5, 25) # Genera 20 tracks dummy
        ]
        
        upcoming_frame = ctk.CTkScrollableFrame(self, fg_color=BG_COLOR, width=280, height=250)
        upcoming_frame.pack(anchor="w", pady=(0, 20), fill="x")
        
        for track in upcoming_tracks:
            ctk.CTkLabel(upcoming_frame, text=track, font=(FONT_FAMILY, 12), text_color=GREEN_TEXT).pack(anchor="w", pady=1)
