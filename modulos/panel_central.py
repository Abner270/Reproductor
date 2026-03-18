# modulos/panel_central.py
import customtkinter as ctk
from PIL import Image
import base64
import io
from .config import *
from .utilidades import create_placeholder_pixel_image
from .panel_progreso import PanelProgreso 

class PanelCentral(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, fg_color="transparent", border_width=0, **kwargs)
        self.app = app # Recibimos la referencia directa de la app principal
        self.view_state = "image"
        
        # Cargar imagen por defecto (pixel art)
        img_data = base64.b64decode(create_placeholder_pixel_image())
        img_raw = Image.open(io.BytesIO(img_data))
        self.pixel_image = ctk.CTkImage(light_image=img_raw, dark_image=img_raw, size=(400, 400))
        
        self._construir_ui()

    def _construir_ui(self):
        # 1. CABECERA (Info de la canción)
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(title_frame, text="NOW PLAYING //", font=(FONT_FAMILY, 22, "bold"), text_color=GREEN_TEXT).pack(side="left")
        
        # IMPORTANTE: self.label_info debe existir para main.py
        self.label_info = ctk.CTkLabel(title_frame, text="  Esperando reproducción...", font=(FONT_FAMILY, 16), text_color=MAGENTA_TEXT)
        self.label_info.pack(side="left", padx=5)

        # 2. ÁREA CENTRAL (Contenedor de Imagen o Letras)
        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content_frame.pack(expand=True, fill="both")
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(0, weight=1)

        # Frame de Imagen
        self.image_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.image_frame.grid(row=0, column=0, sticky="nsew")

        # IMPORTANTE: self.label_imagen es lo que busca el error del Traceback
        self.label_imagen = ctk.CTkLabel(self.image_frame, text="", image=self.pixel_image)
        self.label_imagen.pack(expand=True)

        # Frame de Letras (Oculto al inicio)
        self.lyrics_frame = ctk.CTkFrame(self.main_content_frame, fg_color="#080808", corner_radius=10)
        self.lyrics_label = ctk.CTkLabel(self.lyrics_frame, text="[ Letras no disponibles ]", font=(FONT_FAMILY, 14), text_color="white")
        self.lyrics_label.pack(expand=True, pady=20)

        # 3. CONTROLES Y PROGRESO
        bottom_controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_controls_frame.pack(fill="x", pady=(10, 0))

        # BARRA DE PROGRESO (Instancia del módulo separado)
        self.panel_progreso = PanelProgreso(bottom_controls_frame)
        self.panel_progreso.pack(fill="x", pady=5)

        # BOTONES DE CONTROL
        btns_frame = ctk.CTkFrame(bottom_controls_frame, fg_color="transparent")
        btns_frame.pack(pady=5)

        ctk.CTkButton(btns_frame, text="PREV", width=80, fg_color=BTN_COLOR, hover_color=BTN_HOVER_COLOR, command=self.prev_track).pack(side="left", padx=5)
        ctk.CTkButton(btns_frame, text="PAUSE", width=80, fg_color=BTN_COLOR, hover_color=BTN_HOVER_COLOR, command=self.pause_music).pack(side="left", padx=5)
        ctk.CTkButton(btns_frame, text="PLAY", width=80, fg_color=MAGENTA_TEXT, hover_color=BTN_HOVER_COLOR, command=self.play_music).pack(side="left", padx=5)
        ctk.CTkButton(btns_frame, text="NEXT", width=80, fg_color=BTN_COLOR, hover_color=BTN_HOVER_COLOR, command=self.next_track).pack(side="left", padx=5)

        # BOTÓN SWITCH LYRICS
        self.toggle_btn = ctk.CTkButton(bottom_controls_frame, text="[ SWITCH TO LYRICS ]", 
                                        font=(FONT_FAMILY, 11, "bold"), text_color="#000000", 
                                        fg_color=GREEN_TEXT, hover_color=MAGENTA_TEXT, 
                                        corner_radius=2, height=20, command=self.toggle_lyrics_image)
        self.toggle_btn.pack(pady=(5, 0))

    # --- MÉTODOS DE CONTROL ---
    def play_music(self):
        if self.app.sp:
            try: self.app.sp.start_playback()
            except Exception as e: print(f"// Error: {e}")

    def pause_music(self):
        if self.app.sp:
            try: self.app.sp.pause_playback()
            except Exception as e: print(f"// Error: {e}")

    def next_track(self):
        if self.app.sp:
            try: self.app.sp.next_track()
            except Exception as e: print(f"// Error: {e}")

    def prev_track(self):
        if self.app.sp:
            try: self.app.sp.previous_track()
            except Exception as e: print(f"// Error: {e}")

    def toggle_lyrics_image(self):
        if self.view_state == "image":
            self.image_frame.grid_forget()
            self.lyrics_frame.grid(row=0, column=0, sticky="nsew")
            self.view_state = "lyrics"
            self.toggle_btn.configure(text="[ SWITCH TO COVER ]")
        else:
            self.lyrics_frame.grid_forget()
            self.image_frame.grid(row=0, column=0, sticky="nsew")
            self.view_state = "image"
            self.toggle_btn.configure(text="[ SWITCH TO LYRICS ]")
