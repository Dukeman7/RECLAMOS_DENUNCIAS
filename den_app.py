import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ficha-Bot Duque", layout="wide")

# 2. FUNCIÓN DE DISEÑO (El motor gráfico)
def generar_ficha_png(data):
    # Lienzo HD
    width, height = 900, 750
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    azul_conatel = (0, 51, 102)
    gris_fondo = (245, 245, 245)
    
    # Encabezado
    d.rectangle([0, 0, width, 120], fill=azul_conatel)
    d.text((40, 30), "REPORTE DE INCIDENCIA REGULATORIA", fill=(200, 200, 200))
    d.text((40, 55), f"CÓDIGO: {data.get('Código', 'N/A')}", fill=(255, 255, 255))
    
    # Cuerpo de datos
    d.rectangle([40, 150, 860, 520], outline=(220, 220, 220), width=2)
    y = 170
    fields = [
        ("OPERADOR", str(data.get('OPERADOR', 'THUNDERNET'))),
        ("FECHA REGISTRO", str(data.get('FECHA', 'S/D'))),
        ("DENUNCIANTE", str(data.get('Denunciante', 'S/D'))),
        ("CÉDULA", str(data.get('Cédula Denunciante', 'S/D'))),
        ("UBICACIÓN", f"{data.get('Estado', '')} / {data.get('Municipio', '')}"),
        ("ASUNTO", str(data.get('Asunto', 'S/D'))),
    ]
    
    for label, value in fields:
        d.text((60, y), f"{label}:", fill=azul_conatel)
        d.text((220, y), str(value), fill=(30, 30, 30))
        y += 45

    # Descripción
    d.text((60, y), "DESCRIPCIÓN:", fill=azul_conatel)
    desc = str(data.get('Descripción', 'Sin descripción'))
    lines = [desc[i:i+80] for i in range(0, len(desc), 80)][:5]
    y += 30
    for line in lines:
        d.text((60, y), line, fill=(80, 80, 80))
        y += 25
        
    # Pie de página
    d.rectangle([0, 680, width, 750], fill=gris_fondo)
    d.text((40, 700), "SISTEMA DE GESTIÓN REGULATORIA DUQUE - MODO AUTOMATION", fill=(100, 100, 100))

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# 3. INTERFAZ DE USUARIO (Orden Crítico)
st.title("🚀 Ficha-Bot: Inteligencia de Denuncias")
st.markdown("Convierte sábanas de Excel en fichas de acción rápida.")

# A. Definimos el cargador PRIMERO
archivo_subido = st.file_uploader("Sube tu archivo CSV (UTF-8)", type=["csv"])

# B. Lógica de procesamiento DESPUÉS
if archivo_subido is not None:
    try:
        # Intento robusto de lectura
        df = pd.read_csv(archivo_subido, sep=None, engine='python', on_bad_lines='skip', encoding='utf-8')
    except Exception:
        archivo_subido.seek(0)
        df = pd.read_csv(archivo_subido, sep=',', on_bad_lines='skip', encoding='latin-1')

    if not df.empty:
        st.success(f"✅ Se cargaron {len(df)} registros correctamente.")
        
        # Selector de Código
        if 'Código' in df.columns:
            codigo_sel = st.selectbox("Busca el Código a reportar:", df['Código'].unique())
            
            if codigo_sel:
                datos_caso = df[df['
