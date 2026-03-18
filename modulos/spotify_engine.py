# modulos/spotify_engine.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def conectar_spotify(client_id, client_secret):
    try:
        # Añadimos 'user-read-playback-state' para la cola de reproducción
        scope = "user-read-currently-playing user-modify-playback-state user-read-playback-state"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://127.0.0.1:8888/callback",
            scope=scope,
            open_browser=True
        ))
        return sp
    except Exception as e:
        print(f"// Error de conexión: {e}")
        return None
