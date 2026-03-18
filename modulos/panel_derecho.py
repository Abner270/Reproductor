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
        
        # Variable de memoria para evitar que la lista parpadee al refrescar
        self.ultima_cola_id = "" 
        
        self._construir_ui()

    def _construir_ui(self):
        # --- 1. IMAGEN DE LA CANCIÓN (LADO DERECHO) ---
        self.img_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.img_frame.pack(fill="x", pady=(0, 10)) 
        
        # Cargamos el placeholder inicial (Pixel Art)
        img_data = base64.b64decode(create_placeholder_pixel_image())
        img_raw = Image.open(io.BytesIO(img_data))
        self.placeholder_img = ctk.CTkImage(light_image=img_raw, dark_image=img_raw, size=(350, 350))
        
        self.label_jam_img = ctk.CTkLabel(self.img_frame, image=self.placeholder_img, text="")
        self.label_jam_img.pack(pady=10)

        # --- 2. ESTADO DE LA SESIÓN (JAM / SOLO) ---
        self.header_jam = ctk.CTkLabel(self, text="ESTADO DE SESIÓN //", font=(FONT_FAMILY, 16, "bold"), text_color=MAGENTA_TEXT)
        self.header_jam.pack(anchor="w", pady=0)
        
        self.jam_status_label = ctk.CTkLabel(self, text="// Checking status...", font=(FONT_FAMILY, 12, "bold"), text_color=GREEN_TEXT)
        self.jam_status_label.pack(anchor="w", pady=(0, 5))
                
        # --- 3. FILA DE REPRODUCCIÓN (QUEUE) ---
        ctk.CTkLabel(self, text="SIGUIENTES EN LA COLA //", font=(FONT_FAMILY, 14, "bold"), text_color=GREEN_TEXT).pack(anchor="w", pady=(10, 5))
        
        # Usamos un ScrollableFrame para que si la cola es larga no se rompa el diseño
        self.queue_container = ctk.CTkScrollableFrame(self, fg_color="#080808", corner_radius=8, height=300)
        self.queue_container.pack(anchor="w", pady=(0, 15), fill="x", ipadx=5, ipady=5) 

    def actualizar_datos(self, queue_data, current_img):
        """
        Este método es llamado por main.py cada 4-5 segundos.
        """
        try:
            # 1. ACTUALIZAR LA IMAGEN (Siempre se actualiza si cambia de track)
            ctk_img = ctk.CTkImage(light_image=current_img, dark_image=current_img, size=(350, 350))
            self.label_jam_img.configure(image=ctk_img)
            self.label_jam_img.image = ctk_img

            # 2. PROCESAR LA COLA
            proximas_canciones = queue_data.get('queue', [])[:10] # Tomamos las siguientes 10
            
            # Creamos un identificador único sumando los nombres de las canciones
            # Si el orden o las canciones cambian, el ID cambiará.
            cola_id_actual = "-".join([t.get('name', '') for t in proximas_canciones])

            # --- TRUCO ANTI-PARPADEO ---
            # Si la lista de canciones es exactamente la misma que la vez anterior,
            # salimos de la función sin borrar ni redibujar nada.
            if cola_id_actual == self.ultima_cola_id:
                return 
            
            # Si llegamos aquí, es porque la cola cambió de verdad. Guardamos el nuevo ID.
            self.ultima_cola_id = cola_id_actual

            # 3. REDIBUJAR LA LISTA
            # Limpiamos el contenedor
            for widget in self.queue_container.winfo_children():
                widget.destroy()

            if not proximas_canciones:
                ctk.CTkLabel(self.queue_container, text="No hay más canciones", 
                             font=(FONT_FAMILY, 11), text_color="#555555").pack(pady=10)
            else:
                for i, track in enumerate(proximas_canciones):
                    nombre = track.get('name', 'Unknown')
                    artista = track['artists'][0]['name'] if track.get('artists') else 'Unknown'
                    
                    # Frame por cada fila de la cola
                    track_item = ctk.CTkFrame(self.queue_container, fg_color="transparent")
                    track_item.pack(fill="x", pady=3)
                    
                    # Número de posición
                    ctk.CTkLabel(track_item, text=f"{i+1} ", font=(FONT_FAMILY, 10, "bold"), 
                                 text_color=GREEN_TEXT, width=20).pack(side="left")
                    
                    # Texto de la canción (truncado si es muy largo)
                    txt_full = f"{nombre} - {artista}"
                    if len(txt_full) > 35:
                        txt_full = txt_full[:32] + "..."
                        
                    info_lbl = ctk.CTkLabel(track_item, text=txt_full, 
                                            font=(FONT_FAMILY, 11), text_color="white", anchor="w")
                    info_lbl.pack(side="left", fill="x")

            # 4. ACTUALIZAR ESTADO DE JAM
            # Spotify API indica si es una sesión compartida (Jam)
            es_jam = queue_data.get('is_shared_session', False)
            if es_jam:
                self.jam_status_label.configure(text="// JAM SESSION ACTIVE", text_color=GREEN_TEXT)
            else:
                self.jam_status_label.configure(text="// SOLO SESSION", text_color=MAGENTA_TEXT)

        except Exception as e:
            print(f"// Error en Panel Derecho: {e}")
