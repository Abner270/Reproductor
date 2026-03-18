# modulos/spotify_engine.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def conectar_spotify(client_id, client_secret):
    """Crea la conexión real con tu cuenta"""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="user-read-currently-playing user-modify-playback-state user-read-playback-state"
        ))
        return sp
    except Exception as e:
        return None
