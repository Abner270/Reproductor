# modulos/utilidades.py
from PIL import Image, ImageDraw
import base64
import io

def create_placeholder_pixel_image():
    """Crea un pixel art simple (base64) para usar como placeholder del cover de la canción."""
    size = (64, 64)
    img = Image.new("RGBA", size, color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    
    neon_color = (0, 255, 127)
    magenta_color = (255, 0, 255)
    
    draw.rectangle([5, 40, 10, 64], fill=neon_color)
    draw.rectangle([12, 30, 20, 64], fill=neon_color)
    draw.rectangle([22, 20, 28, 64], fill=neon_color)
    draw.rectangle([30, 35, 38, 64], fill=neon_color)
    draw.rectangle([40, 25, 48, 64], fill=neon_color)
    draw.rectangle([50, 45, 58, 64], fill=neon_color)
    
    puntos = [(15, 35), (25, 25), (35, 40), (45, 30), (55, 50), (15, 55)]
    for p in puntos:
        draw.point(p, fill=magenta_color)
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
