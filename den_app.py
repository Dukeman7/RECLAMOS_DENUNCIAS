import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
import io

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ficha-Bot Duque 2.0", layout="wide")

# 2. FUNCIÓN DE DISEÑO PRO (Corregida y completa)
def generar_ficha_pro(data):
    # 1. Ajuste de Lienzo: 550 ancho (mejor para lectura) x 750 alto (compacto pero todo cabe)
    width, height = 550, 750
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    azul_fuerte = (27, 79, 114)
    gris_borde = (200, 200, 200)
    gris_fondo = (245, 248, 250)
    rojo_status = (200, 0, 0)
    texto_negro = (30, 30, 30)

    # A. Encabezado
    d.rectangle([0, 0, width, 70], fill=azul_fuerte)
    d.text((width//2 - 140, 25), "FICHA DE RECLAMO - GESTION DUQUE", fill=(255, 255, 255))

    # B. Código y Estatus (y=90)
    d.text((40, 85), f"CODIGO: {data.get('Código', 'S/D')}", fill=texto_negro)
    d.text((width - 180, 85), f"ESTATUS: {data.get('ESTATUS', 'ABIERTO')}", fill=rojo_status)

    # C. Bloque: DATOS DEL CLIENTE (y=120 a 210)
    d.rectangle([40, 115, width-40, 210], outline=gris_borde, width=2)
    d.text((50, 120), "DATOS DEL CLIENTE", fill=azul_fuerte)
    d.text((60, 145), f"Nombre: {data.get('Denunciante', 'S/D')}", fill=texto_negro)
    contacto = f"C.I: {data.get('Cédula Denunciante', 'S/D')}  |  Telf: {data.get('Teléfono Denunciante', 'S/D')}"
    d.text((60, 175), contacto, fill=texto_negro)

    # D. Bloque: UBICACIÓN (y=220 a 290) - Reducido el espacio
    d.rectangle([40, 220, width-40, 290], outline=gris_borde, width=2)
    d.text((50, 225), "UBICACION", fill=azul_fuerte)
    ubicacion = f"{data.get('Estado', 'S/D')} | {data.get('Municipio', 'S/D')} | {data.get('Parroquia', 'S/D')}"
    d.text((60, 255), ubicacion, fill=texto_negro)

    # E. Bloque: DETALLE DEL RECLAMO (y=300 a 480)
    d.rectangle([40, 300, width-40, 480], outline=gris_borde, width=2)
    d.text((50, 305), "DETALLE DEL RECLAMO", fill=azul_fuerte)
    d.text((60, 330), f"Asunto: {data.get('Asunto', 'S/D')[:50]}", fill=texto_negro) # Limitado asunto
    
    desc_cuerpo = str(data.get('Descripción', 'Sin descripción'))
    # Limitamos a 5 líneas y recortamos caracteres para que no se salga del ancho
    lines = [desc_cuerpo[i:i+60] for i in range(0, len(desc_cuerpo), 60)][:5]
    y_desc = 355
    d.text((60, 355), "Descripción:", fill=(100, 100, 100))
    for line in lines:
        y_desc += 20
        d.text((60, y_desc), line, fill=(60, 60, 60))

    # F. Bloque: GESTIÓN INTERNA (Daniel) (y=490 a 700)
    d.rectangle([40, 495, width-40, 680], fill=gris_fondo, outline=gris_borde)
    d.text((50, 500), "PARA USO INTERNO / RESPUESTA TECNICA", fill=azul_fuerte)
    # Cuadro blanco para escribir
    d.rectangle([60, 530, width-60, 620], fill=(255, 255, 255), outline=gris_borde)
    d.text((70, 540), "Observaciones del Técnico:", fill=(200, 200, 200))
    
    # G. Firma y Fecha (Relocalizados al fondo de la nueva altura)
    d.text((60, 645), "Firma Responsable: ____________________", fill=texto_negro)
    d.text((width-220, 645), "Fecha: __/__/2026", fill=texto_negro)

    # Retorno de imagen
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
    
# 3. INTERFAZ STREAMLIT
st.title("🚀 Ficha-Bot Duque Professional")
st.markdown("Generación de expedientes técnicos con formato de auditoría.")

archivo_subido = st.file_uploader("Carga tu CSV de denuncias", type=["csv"])

if archivo_subido:
    try:
        df = pd.read_csv(archivo_subido, sep=None, engine='python', on_bad_lines='skip', encoding='utf-8')
    except:
        archivo_subido.seek(0)
        df = pd.read_csv(archivo_subido, sep=',', on_bad_lines='skip', encoding='latin-1')

    if not df.empty and 'Código' in df.columns:
        codigo_sel = st.selectbox("Selecciona Código a Procesar:", df['Código'].unique())
        
        if st.button("Generar Ficha Pro"):
            datos = df[df['Código'] == codigo_sel].iloc[0]
            ficha = generar_ficha_pro(datos)
            st.image(ficha)
            st.download_button("📥 Descargar Expediente PNG", data=ficha, file_name=f"Expediente_{codigo_sel}.png")
    else:
        st.error("Archivo cargado, pero no se encontró la columna 'Código'.")
