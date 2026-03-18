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
        # --- 1. IMAGEN DEL TRACK ACTUAL (VISTA DERECHA) ---
        self.img_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.img_frame.pack(fill="x", pady=(0, 10)) 
        
        # Placeholder inicial
        img_data = base64.b64decode(create_placeholder_pixel_image())
        img = Image.open(io.BytesIO(img_data))
        self.placeholder_img = ctk.CTkImage(light_image=img, dark_image=img, size=(350, 350))
        
        self.label_jam_img = ctk.CTkLabel(self.img_frame, image=self.placeholder_img, text="")
        self.label_jam_img.pack(pady=10)

        # --- 2. SECCIÓN DE ESTADO (JAM / SOLO) ---
        self.header_jam = ctk.CTkLabel(self, text="ESTADO DE SESIÓN //", font=(FONT_FAMILY, 16, "bold"), text_color=MAGENTA_TEXT)
        self.header_jam.pack(anchor="w", pady=0)
        
        self.jam_status_label = ctk.CTkLabel(self, text="// Checking status...", font=(FONT_FAMILY, 12, "bold"), text_color=GREEN_TEXT)
        self.jam_status_label.pack(anchor="w", pady=(0, 5))
        
        # Contenedor para miembros (si es un Jam)
        self.members_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.members_frame.pack(anchor="w", fill="x", pady=(0, 10))
                
        # --- 3. FILA DE REPRODUCCIÓN (QUEUE) ---
        ctk.CTkLabel(self, text="SIGUIENTES EN LA COLA //", font=(FONT_FAMILY, 14, "bold"), text_color=GREEN_TEXT).pack(anchor="w", pady=(10, 5))
        
        # Este frame es el que limpiaremos y llenaremos dinámicamente
        self.queue_container = ctk.CTkScrollableFrame(self, fg_color="#080808", corner_radius=5, height=250)
        self.queue_container.pack(anchor="w", pady=(0, 15), fill="x", ipadx=5, ipady=5) 

    def actualizar_datos(self, queue_data, current_img):
        """
        Método llamado desde main.py para refrescar la información.
        """
        try:
            # 1. Actualizar la imagen derecha (350x350)
            ctk_img = ctk.CTkImage(light_image=current_img, dark_image=current_img, size=(350, 350))
            self.label_jam_img.configure(image=ctk_img)
            self.label_jam_img.image = ctk_img

            # 2. Detectar si es un Jam
            # Spotify API: is_shared_session indica si es un Jam/Group Session
            es_jam = queue_data.get('is_shared_session', False)
            
            if es_jam:
                self.jam_status_label.configure(text="// JAM SESSION ACTIVE", text_color=GREEN_TEXT)
                # Nota: La API de Spotify no da los nombres de los miembros por privacidad fácilmente.
                # Podrías mostrar un mensaje genérico o "Listening with friends"
            else:
                self.jam_status_label.configure(text="// SOLO SESSION", text_color=MAGENTA_TEXT)

            # 3. Actualizar la lista de la Cola (Queue)
            # Limpiar widgets anteriores
            for widget in self.queue_container.winfo_children():
                widget.destroy()

            proximas_canciones = queue_data.get('queue', [])[:8] # Mostramos las próximas 8

            if not proximas_canciones:
                lbl = ctk.CTkLabel(self.queue_container, text="No hay más canciones en la cola", 
                                   font=(FONT_FAMILY, 11), text_color="#555555")
                lbl.pack(pady=10)
            else:
                for i, track in enumerate(proximas_canciones):
                    nombre = track.get('name', 'Unknown')
                    artista = track['artists'][0]['name'] if track.get('artists') else 'Unknown'
                    
                    # Contenedor por cada track para mejor estilo
                    track_item = ctk.CTkFrame(self.queue_container, fg_color="transparent")
                    track_item.pack(fill="x", pady=2)
                    
                    num_lbl = ctk.CTkLabel(track_item, text=f"{i+1} ", font=(FONT_FAMILY, 10, "bold"), text_color=GREEN_TEXT)
                    num_lbl.pack(side="left")
                    
                    info_lbl = ctk.CTkLabel(track_item, text=f"{nombre[:25]}.. - {artista}", 
                                            font=(FONT_FAMILY, 11), text_color="white", anchor="w")
                    info_lbl.pack(side="left", fill="x")

        except Exception as e:
            print(f"// Error actualizando Panel Derecho: {e}")
