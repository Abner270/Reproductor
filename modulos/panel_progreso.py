# modulos/panel_progreso.py
import customtkinter as ctk
from .config import *

class PanelProgreso(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._construir_ui()

    def _construir_ui(self):
        # Contenedor de etiquetas de tiempo
        self.time_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.time_frame.pack(fill="x", padx=5)

        self.label_current = ctk.CTkLabel(self.time_frame, text="00:00", font=(FONT_FAMILY, 10), text_color=GREEN_TEXT)
        self.label_current.pack(side="left")

        self.label_total = ctk.CTkLabel(self.time_frame, text="00:00", font=(FONT_FAMILY, 10), text_color=MAGENTA_TEXT)
        self.label_total.pack(side="right")

        # Barra de progreso estilizada
        self.progress_bar = ctk.CTkProgressBar(
            self, 
            orientation="horizontal",
            height=6,
            progress_color=GREEN_TEXT,
            fg_color="#111111",
            border_width=0
        )
        self.progress_bar.set(0) # Inicia en 0
        self.progress_bar.pack(fill="x", padx=5, pady=(2, 10))

    def actualizar_progreso(self, ms_actual, ms_total):
        """Método para actualizar la barra y los textos desde el exterior"""
        progreso = ms_actual / ms_total if ms_total > 0 else 0
        self.progress_bar.set(progreso)

        # Convertir ms a formato MM:SS
        def format_time(ms):
            s = int((ms / 1000) % 60)
            m = int((ms / (1000 * 60)) % 60)
            return f"{m:02d}:{s:02d}"

        self.label_current.configure(text=format_time(ms_actual))
        self.label_total.configure(text=format_time(ms_total))
