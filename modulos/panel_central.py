# modulos/panel_central.py
import customtkinter as ctk
from PIL import Image
import base64
import io
from .config import *
from .utilidades import create_placeholder_pixel_image
from .panel_progreso import PanelProgreso # Importamos el nuevo módulo

class PanelCentral(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", border_width=0, **kwargs)
        self.app = self.master.master.master 
        self.view_state = "image"
        self._construir_ui()

    def _construir_ui(self):
        # 1. CABECERA (Se mantiene minimalista arriba)
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(title_frame, text="NOW PLAYING //", font=(FONT_FAMILY, 22, "bold"), text_color=GREEN_TEXT).pack(side="left")
        self.label_info = ctk.CTkLabel(title_frame, text="  'Team Funk' // Collaborator Groove", font=(FONT_FAMILY, 16), text_color=MAGENTA_TEXT)
        self.label_info.pack(side="left", padx=5)

        # 2. ÁREA CENTRAL ENFOCADA (Ocupa todo el espacio disponible)
        self.main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        # Usamos expand=True para que tome el centro de la pantalla
        self.main_content_frame.pack(expand=True, fill="both")

        # Vista de Imagen
        self.image_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.image_frame.grid(row=0, column=0, sticky="nsew")

        img_data = base64.b64decode(create_placeholder_pixel_image())
        img = Image.open(io.BytesIO(img_data))
        # Aumentamos un poco el tamaño para que sea el protagonista (ej. 400x400)
        self.pixel_image = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 400))
        
        self.image_label = ctk.CTkLabel(self.image_frame, image=self.pixel_image, text="")
        self.image_label.pack(pady=10, expand=True)

        # Vista de Letras
        self.lyrics_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.lyrics_frame.grid_forget()

        self.lyrics_text_box = ctk.CTkTextbox(self.lyrics_frame, width=500, height=450, font=(FONT_FAMILY, 16), text_color=GREEN_TEXT, fg_color="#050505", border_width=1, border_color="#111111", wrap="word")
        self.lyrics_text_box.insert("0.0", "esperando señal de spotify...")
        self.lyrics_text_box.configure(state="disabled")
        self.lyrics_text_box.pack(pady=10, expand=True)
        
        self.main_content_frame.grid_rowconfigure(0, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)

        # 3. SECCIÓN INFERIOR: PROGRESO Y CONTROLES (Agrupados abajo)
        bottom_controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_controls_frame.pack(fill="x", pady=(10, 0))

        # Barra de progreso integrada desde el nuevo archivo
        self.progreso = PanelProgreso(bottom_controls_frame)
        self.progreso.pack(fill="x")

        player_controls_frame = ctk.CTkFrame(bottom_controls_frame, fg_color="transparent")
        player_controls_frame.pack(pady=5)
        
        # Botones de control
        ctk.CTkButton(player_controls_frame, text=" [<<] ", width=40, font=(FONT_FAMILY, 12), text_color=MAGENTA_TEXT, fg_color="transparent", hover_color=BTN_HOVER_COLOR, command=self.prev_track).pack(side="left")
        ctk.CTkButton(player_controls_frame, text=" [||] ", width=40, font=(FONT_FAMILY, 12), text_color=GREEN_TEXT, fg_color="transparent", hover_color=BTN_HOVER_COLOR, command=self.pause_music).pack(side="left")
        ctk.CTkButton(player_controls_frame, text=" [PLAY] ", width=60, font=(FONT_FAMILY, 12, "bold"), text_color=GREEN_TEXT, fg_color="transparent", hover_color=BTN_HOVER_COLOR, command=self.play_music).pack(side="left")
        ctk.CTkButton(player_controls_frame, text=" [>>] ", width=40, font=(FONT_FAMILY, 12), text_color=MAGENTA_TEXT, fg_color="transparent", hover_color=BTN_HOVER_COLOR, command=self.next_track).pack(side="left")
        
        # Botón de Toggle (Switch) al final
        self.toggle_btn = ctk.CTkButton(bottom_controls_frame, text="[SWITCH TO LYRICS]", font=(FONT_FAMILY, 11, "bold"), text_color="#000000", fg_color=GREEN_TEXT, hover_color=MAGENTA_TEXT, corner_radius=2, height=20, command=self.toggle_lyrics_image)
        self.toggle_btn.pack(pady=(5, 0))

    # --- Los métodos de control (play, pause, next, prev, toggle) se mantienen igual ---
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
            self.toggle_btn.configure(text="[SWITCH TO IMAGE]")
        else:
            self.lyrics_frame.grid_forget()
            self.image_frame.grid(row=0, column=0, sticky="nsew")
            self.view_state = "image"
            self.toggle_btn.configure(text="[SWITCH TO LYRICS]")
