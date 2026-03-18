# modulos/utilidades.py
from PIL import Image, ImageDraw
import base64
import io

def create_placeholder_pixel_image():
    """Crea un pixel art simple (base64) para usar como placeholder del cover de la canción."""
    size = (64, 64)
    img = Image.new("RGBA", size, color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    
    neon_color = (0, 255, 127) # Verde primavera
    magenta_color = (255, 0, 255) # Magenta
    
    # Diseño de ciudad pixelada simplificada
    draw.rectangle([5, 40, 10, 64], fill=neon_color)
    draw.rectangle([12, 30, 20, 64], fill=neon_color)
    draw.rectangle([22, 20, 28, 64], fill=neon_color)
    draw.rectangle([30, 35, 38, 64], fill=neon_color)
    draw.rectangle([40, 25, 48, 64], fill=neon_color)
    draw.rectangle([50, 45, 58, 64], fill=neon_color)
    
    # Unos pocos puntos magenta aleatorios como luces
    draw.point((15, 35), fill=magenta_color)
    draw.point((25, 25), fill=magenta_color)
    draw.point((35, 40), fill=magenta_color)
    draw.point((45, 30), fill=magenta_color)
    draw.point((55, 50), fill=magenta_color)
    draw.point((15, 55), fill=magenta_color)
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# --- NUEVA FUNCIÓN PARA EL GATITO MICRO ---
def create_micro_sleeping_cat_image():
    """Crea un pixel art de un gatito micro-pequeño y durmiendo (base64)."""
    # Usamos un tamaño base pequeño para el diseño
    size = (32, 16) 
    img = Image.new("RGBA", size, color=(0, 0, 0, 0)) # Fondo transparente
    draw = ImageDraw.Draw(img)
    
    # Colores
    cat_color = (170, 220, 230) # Cian pastel/grisáceo como el anterior
    
    # Diseño Micro:
    # Cuerpo (forma de L muy pequeña)
    draw.rectangle([10, 8, 20, 12], fill=cat_color) # Parte horizontal
    draw.rectangle([18, 5, 20, 8], fill=cat_color)  # Parte vertical (cabeza/orejas)

    # Orejas (dos píxeles individuales sobre la cabeza)
    draw.point((18, 4), fill=cat_color)
    draw.point((20, 4), fill=cat_color)

    # Ojo cerrado (un solo píxel negro en la "cabeza")
    draw.point((19, 6), fill=(0, 0, 0))

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
