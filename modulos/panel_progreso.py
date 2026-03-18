# modulos/panel_progreso.py
import customtkinter as ctk
from .config import *

class PanelProgreso(ctk.CTkFrame):
    def __init__(self, master, app_master, **kwargs):
        super().__init__(master, fg_color="#080808", height=110, corner_radius=0, **kwargs)
        self.app_master = app_master
        
        # Variables para controlar el flujo de datos
        self.is_dragging = False # Evita saltos mientras arrastras la barra
        self.ms_total = 0
        self.shuffle_state = False
        self.repeat_state = "off"
        
        self._construir_ui()

    def _construir_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        # --- IZQUIERDA: INFO ---
        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.info_frame.grid(row=0, column=0, sticky="nsw", padx=20)
        self.lbl_track = ctk.CTkLabel(self.info_frame, text="---", font=(FONT_FAMILY, 14, "bold"), text_color="white", anchor="w")
        self.lbl_track.pack(pady=(15, 0), anchor="w")
        self.lbl_artist = ctk.CTkLabel(self.info_frame, text="Spotify", font=(FONT_FAMILY, 11), text_color=GREEN_TEXT, anchor="w")
        self.lbl_artist.pack(anchor="w")

        # --- CENTRO: CONTROLES ---
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.grid(row=0, column=1, sticky="nsew")

        # Botones de Control
        self.btns_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.btns_frame.pack(pady=(5, 0))

        self.btn_shuffle = ctk.CTkButton(self.btns_frame, text="🔀", width=30, fg_color="transparent", text_color="gray", command=self._toggle_shuffle)
        self.btn_shuffle.pack(side="left", padx=10)

        ctk.CTkButton(self.btns_frame, text="⏮", width=35, fg_color="transparent", command=self.app_master.panel_central.prev_track).pack(side="left", padx=5)
        
        self.btn_play = ctk.CTkButton(self.btns_frame, text="▶", width=42, height=42, corner_radius=21, fg_color="white", text_color="black", command=self._toggle_play_pause)
        self.btn_play.pack(side="left", padx=10)

        ctk.CTkButton(self.btns_frame, text="⏭", width=35, fg_color="transparent", command=self.app_master.panel_central.next_track).pack(side="left", padx=5)
        
        self.btn_repeat = ctk.CTkButton(self.btns_frame, text="🔁", width=30, fg_color="transparent", text_color="gray", command=self._toggle_repeat)
        self.btn_repeat.pack(side="left", padx=10)

        # BARRA DE PROGRESO INTERACTIVA (SLIDER)
        self.slider_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.slider_frame.pack(fill="x", padx=40, pady=5)

        self.lbl_current = ctk.CTkLabel(self.slider_frame, text="0:00", font=(FONT_FAMILY, 10), text_color="gray")
        self.lbl_current.pack(side="left", padx=5)

        self.progress_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=100, progress_color=GREEN_TEXT, 
                                            button_color="white", height=14, command=self._on_slider_drag)
        self.progress_slider.set(0)
        self.progress_slider.pack(side="left", expand=True, fill="x")
        
        # Enlazar eventos de mouse
        self.progress_slider.bind("<Button-1>", self._on_slider_press)
        self.progress_slider.bind("<ButtonRelease-1>", self._on_slider_release)

        self.lbl_total = ctk.CTkLabel(self.slider_frame, text="0:00", font=(FONT_FAMILY, 10), text_color="gray")
        self.lbl_total.pack(side="left", padx=5)

        # --- DERECHA: EXTRAS Y VOLUMEN ---
        self.extra_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.extra_frame.grid(row=0, column=2, sticky="nse", padx=20)

        # Botones adicionales
        ctk.CTkButton(self.extra_frame, text="🎙", width=30, fg_color="transparent", command=self.app_master.panel_central.toggle_lyrics_image).pack(side="left")
        ctk.CTkButton(self.extra_frame, text="☰", width=30, fg_color="transparent", command=lambda: print("Fila")).pack(side="left")
        
        ctk.CTkLabel(self.extra_frame, text="🔊", font=(FONT_FAMILY, 12)).pack(side="left", padx=(5, 0))
        self.vol_slider = ctk.CTkSlider(self.extra_frame, width=100, from_=0, to=100, progress_color=GREEN_TEXT, command=self._set_volume)
        self.vol_slider.pack(side="left", padx=5)
        
        ctk.CTkButton(self.extra_frame, text="⛶", width=30, fg_color="transparent", command=self._toggle_fullscreen).pack(side="left")

    # --- LÓGICA DE INTERACCIÓN ---
    
    def _on_slider_press(self, event):
        self.is_dragging = True

    def _on_slider_release(self, event):
        """Al soltar el mouse, salta al punto de la canción en Spotify"""
        if self.app_master.sp and self.ms_total > 0:
            nuevo_ms = int((self.progress_slider.get() / 100) * self.ms_total)
            try:
                self.app_master.sp.seek_track(nuevo_ms)
            except: pass
        self.is_dragging = False

    def _on_slider_drag(self, value):
        if self.ms_total > 0:
            ms_actual = int((value / 100) * self.ms_total)
            self.lbl_current.configure(text=self._format_ms(ms_actual))

    def _set_volume(self, value):
        """Silencia el error 403 si el dispositivo no permite control de volumen"""
        if self.app_master.sp:
            try:
                self.app_master.sp.volume(int(value))
            except Exception:
                pass # Ignoramos el error 403 para no ensuciar la consola

    def actualizar_datos(self, titulo, artista, ms_actual, ms_total):
        self.lbl_track.configure(text=titulo)
        self.lbl_artist.configure(text=artista)
        self.ms_total = ms_total
        if not self.is_dragging:
            ratio = (ms_actual / ms_total) * 100 if ms_total > 0 else 0
            self.progress_slider.set(ratio)
            self.lbl_current.configure(text=self._format_ms(ms_actual))
            self.lbl_total.configure(text=self._format_ms(ms_total))

    def _format_ms(self, ms):
        segundos = int((ms / 1000) % 60)
        minutos = int((ms / (1000 * 60)) % 60)
        return f"{minutos}:{segundos:02d}"

    def _toggle_play_pause(self):
        # Lógica de cambio visual y comando
        if self.btn_play.cget("text") == "▶":
            self.btn_play.configure(text="⏸")
            self.app_master.panel_central.play_music()
        else:
            self.btn_play.configure(text="▶")
            self.app_master.panel_central.pause_music()

    def _toggle_shuffle(self):
        if self.app_master.sp:
            self.shuffle_state = not self.shuffle_state
            try:
                self.app_master.sp.shuffle(self.shuffle_state)
                self.btn_shuffle.configure(text_color=GREEN_TEXT if self.shuffle_state else "gray")
            except: pass

    def _toggle_repeat(self):
        if self.app_master.sp:
            modes = ["off", "context", "track"]
            idx = (modes.index(self.repeat_state) + 1) % 3
            self.repeat_state = modes[idx]
            try:
                self.app_master.sp.repeat(self.repeat_state)
                color = GREEN_TEXT if self.repeat_state != "off" else "gray"
                self.btn_repeat.configure(text_color=color, text="🔂" if self.repeat_state == "track" else "🔁")
            except: pass

    def _toggle_fullscreen(self):
        is_fs = self.app_master.attributes("-fullscreen")
        self.app_master.attributes("-fullscreen", not is_fs)
