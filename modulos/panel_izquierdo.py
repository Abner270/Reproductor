# modulos/panel_izquierdo.py
import customtkinter as ctk
from .config import *

class PanelIzquierdo(ctk.CTkFrame):
    def __init__(self, master, app_master, **kwargs):
        super().__init__(master, fg_color="transparent", border_width=0, **kwargs)
        self.app_master = app_master
        self._construir_ui()

    def _construir_ui(self):
        # --- SECCIÓN: MIS PLAYLISTS ---
        label = ctk.CTkLabel(self, text="// MIS PLAYLISTS", font=(FONT_FAMILY, 18, "bold"), text_color=MAGENTA_TEXT)
        label.pack(anchor="w", pady=(0, 10))

        playlists = ["  [chill-colab]", "  [code-and-debug]", "  [teammate-lo-fi]", "  [funk-for-bugs]", "  [synthwave-neon-night]"]
        playlists_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", width=280, height=120)
        playlists_frame.pack(anchor="w", pady=(0, 20), fill="x")
        
        for p in playlists:
            ctk.CTkLabel(playlists_frame, text=p, font=(FONT_FAMILY, 12), text_color=GREEN_TEXT).pack(anchor="w", pady=1)

        # --- SECCIÓN: AJUSTES VISUALES EN TIEMPO REAL ---
        ajustes_frame = ctk.CTkFrame(self, fg_color="#111111", corner_radius=8)
        ajustes_frame.pack(anchor="w", pady=(0, 20), fill="x", ipadx=10, ipady=10)
        
        ctk.CTkLabel(ajustes_frame, text="// UI SETTINGS", font=(FONT_FAMILY, 14, "bold"), text_color=MAGENTA_TEXT).pack(anchor="w", pady=(0,10))

        # 1. Slider Transparencia (Mínimo 65%, Máximo 100%)
        ctk.CTkLabel(ajustes_frame, text="Transparencia", font=(FONT_FAMILY, 11), text_color="white").pack(anchor="w")
        self.slider_alpha = ctk.CTkSlider(ajustes_frame, from_=0.65, to=1.0, command=self.app_master.cambiar_opacidad, button_color=GREEN_TEXT)
        self.slider_alpha.set(0.70) # Valor inicial al 70%
        self.slider_alpha.pack(fill="x", pady=(0, 10))

        # 2. Toggle Fondo (Color vs Imagen)
        ctk.CTkLabel(ajustes_frame, text="Fondo App", font=(FONT_FAMILY, 11), text_color="white").pack(anchor="w")
        self.btn_bg = ctk.CTkSegmentedButton(ajustes_frame, values=["Color", "Cover"], command=self.app_master.cambiar_modo_fondo, selected_color=MAGENTA_TEXT)
        self.btn_bg.set("Color")
        self.btn_bg.pack(fill="x", pady=(0, 10))

        # --- SECCIÓN: INFO ---
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(anchor="w", pady=(0, 20))
        ctk.CTkLabel(stats_frame, text="// SYSTEM INFO", font=(FONT_FAMILY, 14, "bold"), text_color=MAGENTA_TEXT).pack(anchor="w")
        for item in ["// 14 playlists", "// 650 tracks"]:
            ctk.CTkLabel(stats_frame, text="  "+item, font=(FONT_FAMILY, 12), text_color=GREEN_TEXT).pack(anchor="w", pady=1)
