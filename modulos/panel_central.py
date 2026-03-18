# modulos/panel_central.py
import customtkinter as ctk
from PIL import Image
import base64
import io
from .config import *
from .utilidades import create_placeholder_pixel_image

class PanelCentral(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BG_COLOR, border_width=0, **kwargs)
        self.view_state = "image"
        self._construir_ui()

    def _construir_ui(self):
        # Cabecera NOW PLAYING
        title_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        title_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(title_frame, text="NOW PLAYING //", font=(FONT_FAMILY, 22, "bold"), text_color=GREEN_TEXT).pack(side="left")
        ctk.CTkLabel(title_frame, text="  'Team Funk' // Collaborator Groove", font=(FONT_FAMILY, 16), text_color=MAGENTA_TEXT).pack(side="left", padx=5)

        # Área principal (Imagen o Letras)
        self.main_content_frame = ctk.CTkFrame(self, fg_color=BG_COLOR, border_width=0)
        self.main_content_frame.pack(expand=True, fill="both", pady=(0, 20))

        # 1. Vista de Imagen
        self.image_frame = ctk.CTkFrame(self.main_content_frame, fg_color=BG_COLOR)
        self.image_frame.grid(row=0, column=0, sticky="nsew")

        img_data = base64.b64decode(create_placeholder_pixel_image())
        img = Image.open(io.BytesIO(img_data))
        self.pixel_image = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 300))
        
        ctk.CTkLabel(self.image_frame, image=self.pixel_image, text="").pack(pady=20, expand=True)

        # 2. Vista de Letras (Oculta por defecto)
        self.lyrics_frame = ctk.CTkFrame(self.main_content_frame, fg_color=BG_COLOR)
        
        lyrics_text = (
            "lost in the digital static\ncode waves crashing on the screen\n"
            "neon reflections in the matrix\ncan you hear the collaborative beat?\n\n"
            "(chorus)\nteamwork is the groove\nwe are building this, we improve\n"
        )
        self.lyrics_text_box = ctk.CTkTextbox(self.lyrics_frame, width=300, height=300, font=(FONT_FAMILY, 12), text_color=GREEN_TEXT, fg_color=BG_COLOR, border_width=0, wrap="word")
        self.lyrics_text_box.insert("0.0", lyrics_text)
        self.lyrics_text_box.configure(state="disabled")
        self.lyrics_text_box.pack(pady=20, expand=True)
        
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # Controles
        controls_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        controls_frame.pack(fill="x")
        
        player_controls_frame = ctk.CTkFrame(controls_frame, fg_color=BG_COLOR)
        player_controls_frame.pack(pady=5)
        
        # Función rápida para botones de texto monoespaciado
        def btn(text, color):
            return ctk.CTkButton(player_controls_frame, text=f" [{text}] ", font=(FONT_FAMILY, 12), text_color=color, fg_color=BG_COLOR, hover_color=BTN_HOVER_COLOR, border_width=0)
        
        btn("<<", MAGENTA_TEXT).pack(side="left")
        btn("<", MAGENTA_TEXT).pack(side="left")
        btn("||", GREEN_TEXT).pack(side="left")
        btn("play", GREEN_TEXT).pack(side="left")
        btn(">", MAGENTA_TEXT).pack(side="left")
        btn(">>", MAGENTA_TEXT).pack(side="left")
        btn("❤", GREEN_TEXT).pack(side="left")
        
        # Botón Toggle
        self.toggle_btn = ctk.CTkButton(controls_frame, text="[IMAGE / LYRICS]", font=(FONT_FAMILY, 14, "bold"), text_color="#000000", fg_color=GREEN_TEXT, hover_color=MAGENTA_TEXT, corner_radius=0, command=self.toggle_lyrics_image)
        self.toggle_btn.pack(pady=(20, 0))

    def toggle_lyrics_image(self):
        if self.view_state == "image":
            self.image_frame.grid_forget()
            self.lyrics_frame.grid(row=0, column=0, sticky="nsew")
            self.view_state = "lyrics"
        else:
            self.lyrics_frame.grid_forget()
            self.image_frame.grid(row=0, column=0, sticky="nsew")
            self.view_state = "image"
