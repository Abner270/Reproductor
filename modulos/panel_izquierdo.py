# modulos/panel_izquierdo.py
import customtkinter as ctk
from .config import *

class PanelIzquierdo(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=BG_COLOR, border_width=0, **kwargs)
        self._construir_ui()

    def _construir_ui(self):
        # Título Playlists
        label = ctk.CTkLabel(self, text="// MIS PLAYLISTS", font=(FONT_FAMILY, 18, "bold"), text_color=MAGENTA_TEXT)
        label.pack(anchor="w", pady=(0, 10))

        playlists = [
            "  [chill-colab]", "  [code-and-debug]", "  [teammate-lo-fi]",
            "  [funk-for-bugs]", "  [synthwave-neon-night]", "  [ambient-void-focus]",
            "  [reggae-dub-break]", "  [psytrance-flow-state]", "  [classical-concerto]",
            "  [minimal-loops-station]", "  [8bit-beats-retro]", "  [future-pop-rhythm]",
            "  [heavy-metal-crush]", "  [data-stream-flow]"
        ]
        
        # Lista scrollable de playlists
        playlists_frame = ctk.CTkScrollableFrame(self, fg_color=BG_COLOR, width=280, height=200)
        playlists_frame.pack(anchor="w", pady=(0, 20), fill="x")
        
        for playlist_name in playlists:
            p_label = ctk.CTkLabel(playlists_frame, text=playlist_name, font=(FONT_FAMILY, 12), text_color=GREEN_TEXT)
            p_label.pack(anchor="w", pady=1)

        # Links (reproduciendo la imagen original)
        links_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        links_frame.pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(links_frame, text="  [about]  [credits]  [rss.xml]", font=(FONT_FAMILY, 12), text_color=MAGENTA_TEXT).pack(anchor="w")
        ctk.CTkLabel(links_frame, text="  [patreon]  [podcasts.apple]", font=(FONT_FAMILY, 12), text_color=GREEN_TEXT).pack(anchor="w")
        ctk.CTkLabel(links_frame, text="  [folder.jpg]  [enterprise mode]", font=(FONT_FAMILY, 12), text_color=MAGENTA_TEXT).pack(anchor="w")
        ctk.CTkLabel(links_frame, text="  [invert]  [fullscreen]", font=(FONT_FAMILY, 12), text_color=GREEN_TEXT).pack(anchor="w")

        # Stats del sistema
        stats_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        stats_frame.pack(anchor="w", pady=(0, 20))
        ctk.CTkLabel(stats_frame, text="// SYSTEM INFO", font=(FONT_FAMILY, 14, "bold"), text_color=MAGENTA_TEXT).pack(anchor="w")
        stats_data = ["// 14 playlists", "// 650 tracks", "// 32 hours", "// 45 minutes", "// 22 seconds"]
        for item in stats_data:
            ctk.CTkLabel(stats_frame, text="  "+item, font=(FONT_FAMILY, 12), text_color=GREEN_TEXT).pack(anchor="w", pady=1)

        # Snippet de código Collab
        code_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        code_frame.pack(anchor="w", pady=(0, 20))
        ctk.CTkLabel(code_frame, text="// TEAM COLLAB CODE SNIPPET", font=(FONT_FAMILY, 14, "bold"), text_color=MAGENTA_TEXT).pack(anchor="w")
        code_text = "def find_collaborator(task='UI'):\n\treturn '// ' + task + ' teammate...';"
        ctk.CTkLabel(code_frame, text=code_text, font=(FONT_FAMILY, 12), text_color=GREEN_TEXT, justify="left").pack(anchor="w", pady=2)
