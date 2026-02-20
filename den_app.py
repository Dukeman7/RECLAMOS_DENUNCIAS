import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# 1. Cargar la data
df = pd.read_csv('Casos Abiertos THUNDERNET NOV-DIC-ENE-FEB.xlsx - Hoja1.csv')

def crear_ficha_png(codigo_caso):
    # Filtrar el caso
    caso = df[df['Código'] == codigo_caso].iloc[0]
    
    # Crear lienzo (HD)
    img = Image.new('RGB', (800, 600), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Colores y Estilos
    header_color = (0, 51, 102) # Azul Marino
    text_color = (30, 30, 30)
    
    # Dibujar Encabezado
    d.rectangle([0, 0, 800, 80], fill=header_color)
    d.text((20, 20), f"FICHA DE DENUNCIA: {caso['Código']}", fill=(255,255,255))
    d.text((20, 45), f"OPERADOR: {caso['OPERADOR']}", fill=(255,255,255))

    # Cuerpo de la Ficha
    y = 100
    fields = [
        ("DENUNCIANTE", caso['Denunciante']),
        ("CÉDULA", caso['Cédula Denunciante']),
        ("ESTADO/MUN.", f"{caso['Estado']} / {caso['Municipio']}"),
        ("ASUNTO", caso['Asunto']),
        ("DESCRIPCIÓN", caso['Descripción'][:300] + "...") # Limitado para la ficha
    ]
    
    for label, value in fields:
        d.text((20, y), f"{label}:", fill=header_color)
        d.text((150, y), str(value), fill=text_color)
        y += 40
        
    # Pie de Ficha
    d.rectangle([0, 550, 800, 600], fill=(240, 240, 240))
    d.text((20, 565), f"ESTATUS: {caso['ESTATUS']} | FECHA REGISTRO: {caso['FECHA']}", fill=(100, 100, 100))

    img.save(f"Ficha_{codigo_caso}.png")
