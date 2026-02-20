import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
import io

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ficha-Bot Duque 2.0", layout="wide")

# 2. FUNCIÓN DE DISEÑO PRO (Corregida y completa)
def generar_ficha_pro(data):
    # Lienzo tipo A4 vertical (800x1000) ahora 450x700 LD
    width, height = 450, 700
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Paleta de Colores
    azul_fuerte = (27, 79, 114)
    gris_borde = (200, 200, 200)
    gris_fondo = (245, 248, 250)
    rojo_status = (200, 0, 0)
    texto_negro = (30, 30, 30)

    # A. Encabezado
    d.rectangle([0, 0, width, 80], fill=azul_fuerte)
    d.text((width//2 - 140, 35), "FICHA DE RECLAMO - GESTION DUQUE", fill=(255, 255, 255))

    # B. Código y Estatus
    d.text((40, 110), f"CODIGO: {data.get('Código', 'S/D')}", fill=texto_negro)
    d.text((width - 280, 110), f"ESTATUS: {data.get('ESTATUS', 'ABIERTO')}", fill=rojo_status)
          # cambié 220 por 280
    # C. Bloque: DATOS DEL CLIENTE
    d.rectangle([40, 150, width-40, 260], outline=gris_borde, width=2)
    d.text((50, 155), "DATOS DEL CLIENTE", fill=azul_fuerte)
    d.text((60, 185), f"Nombre: {data.get('Denunciante', 'S/D')}", fill=texto_negro)
    d.text((60, 215), f"Cedula: {data.get('Cédula Denunciante', 'S/D')}", fill=texto_negro)
    # Contacto en una línea
    contacto = f"Telf: {data.get('Teléfono Denunciante', 'S/D')}   |   Email: {data.get('Correo Denunciante', 'S/D')}"
    d.text((60, 235), contacto, fill=texto_negro)

    # D. Bloque: UBICACIÓN          cambie aqui 380 por 300
    d.rectangle([40, 280, width-40, 300], outline=gris_borde, width=2)
    d.text((50, 285), "UBICACION DEL INCIDENTE", fill=azul_fuerte)
    ubicacion = f"Estado: {data.get('Estado', 'S/D')} | Municipio: {data.get('Municipio', 'S/D')}"
    d.text((60, 315), ubicacion, fill=texto_negro)
    d.text((60, 345), f"Parroquia: {data.get('Parroquia', 'S/D')}", fill=texto_negro)

    # E. Bloque: DETALLE DEL RECLAMO   660 por 600
    d.rectangle([40, 400, width-40, 600], outline=gris_borde, width=2)
    d.text((50, 305), "DETALLE DEL RECLAMO", fill=azul_fuerte)  #405 x 305
    d.text((60, 335), f"Asunto: {data.get('Asunto', 'S/D')}", fill=texto_negro) #435x335
    
    desc_cuerpo = str(data.get('Descripción', 'Sin descripción adicional'))
    lines = [desc_cuerpo[i:i+85] for i in range(0, len(desc_cuerpo), 85)][:7]
    y_desc = 370  # cambie de 470 a 370
    d.text((60, 370), "Descripcion del Ciudadano:", fill=(100, 100, 100))
    for line in lines:
        y_desc += 22
        d.text((60, y_desc), line, fill=(60, 60, 60))

    # F. Bloque: GESTIÓN INTERNA (El área blanca de Daniel)
    d.rectangle([40, 480, width-40, 750], fill=gris_fondo, outline=gris_borde)  # cambio 680 x480 y 950x750
    d.text((50, 485), "PARA USO INTERNO / RESPUESTA TECNICA", fill=azul_fuerte)
    # Cuadro para escribir
    d.rectangle([60, 520, width-60, 680], fill=(255, 255, 255), outline=gris_borde)
    d.text((70, 530), "Observaciones del Tecnico:", fill=(200, 200, 200))
    
    d.text((60, 710), "Firma Responsable: ____________________", fill=texto_negro)
    d.text((width-260, 710), "Fecha Cierre: __/__/2026", fill=texto_negro)

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
