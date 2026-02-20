import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# 1. Configuración (Siempre al principio)
st.set_page_config(page_title="Ficha-Bot Duque", layout="wide")
st.title("🚀 Ficha-Bot: Gestión de Denuncias Duque")

# 2. DEFINIR LA VARIABLE (Aquí es donde estaba el error)
# Esta línea TIENE que ir antes que cualquier "if" que use ese nombre
archivo_subido = st.file_uploader("Arrastra aquí tu archivo CSV", type=["csv"])

# 3. USAR LA VARIABLE
if archivo_subido is not None:
    try:
        # Usamos el motor de Python que es más robusto para archivos de Excel/Bloc de Notas
        df = pd.read_csv(archivo_subido, sep=None, engine='python', on_bad_lines='skip', encoding='utf-8')
    except Exception:
        archivo_subido.seek(0)
        df = pd.read_csv(archivo_subido, sep=',', on_bad_lines='skip', encoding='latin-1')

    if not df.empty:
        st.success(f"✅ Base de datos cargada: {len(df)} registros.")
        
        # Selector de Código
        opciones = df['Código'].unique()
        codigo_sel = st.selectbox("Busca el Código CONATEL:", opciones)
        
        # ... aquí sigue el resto de tu lógica de generar_ficha_png ...
        # (Asegúrate de que la función generar_ficha_png esté definida arriba)
# Configuración de la página
st.set_page_config(page_title="Ficha-Bot Duque", layout="wide")

def generar_ficha_png(data):
    # Crear un lienzo HD (900x700)
    width, height = 900, 700
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Colores Corporativos
    azul_conatel = (0, 51, 102)
    gris_fondo = (245, 245, 245)
    texto_principal = (30, 30, 30)

    # 1. Encabezado Elegante
    d.rectangle([0, 0, width, 120], fill=azul_conatel)
    # Título del Caso
    d.text((40, 30), f"REPORTE DE INCIDENCIA REGULATORIA", fill=(200, 200, 200))
    d.text((40, 55), f"CÓDIGO: {data['Código']}", fill=(255, 255, 255))
    
    # 2. Cuerpo de la Ficha
    # Fondo para los datos
    d.rectangle([40, 150, 860, 480], outline=(220, 220, 220), width=2)
    
    y = 170
    fields = [
        ("OPERADOR", str(data['OPERADOR'])),
        ("FECHA REGISTRO", str(data['FECHA'])),
        ("DENUNCIANTE", str(data['Denunciante'])),
        ("CÉDULA", str(data['Cédula Denunciante'])),
        ("UBICACIÓN", f"{data['Estado']} / {data['Municipio']} / {data['Parroquia']}"),
        ("ASUNTO", str(data['Asunto'])),
    ]
    
    for label, value in fields:
        d.text((60, y), f"{label}:", fill=azul_conatel)
        d.text((220, y), str(value), fill=texto_principal)
        y += 45

    # 3. Descripción (Ajuste de texto para que no se salga)
    d.text((60, y), "DESCRIPCIÓN DEL CASO:", fill=azul_conatel)
    desc = str(data['Descripción'])
    # Dividir descripción en líneas de 80 caracteres
    lines = [desc[i:i+85] for i in range(0, len(desc), 85)][:4] # Máximo 4 líneas
    y += 30
    for line in lines:
        d.text((60, y), line, fill=(80, 80, 80))
        y += 25
        
    # 4. Pie de página institucional
    d.rectangle([0, 640, width, 700], fill=gris_fondo)
    d.text((40, 660), "SISTEMA DE GESTIÓN REGULATORIA DUQUE - CONSULTORÍA ESTRATÉGICA", fill=(100, 100, 100))

    # Guardar en memoria para Streamlit
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# --- INTERFAZ DE STREAMLIT ---
st.title("🚀 Ficha-Bot: Automatización de Denuncias")
st.markdown("Carga tu Excel/CSV de VenApp para generar fichas de inspección visuales.")

# --- 1. Definimos la variable (El cargador de archivos) ---
archivo_subido = st.file_uploader("Arrastra aquí tu archivo CSV", type=["csv"])

# --- 2. Ahora sí, la usamos ---
if archivo_subido is not None:
    try:
        # Aquí va el código anti-balas que te pasé antes
        df = pd.read_csv(
            archivo_subido, 
            sep=None, 
            engine='python', 
            on_bad_lines='skip', 
            encoding='utf-8'
        )
    except Exception as e:
        archivo_subido.seek(0)
        df = pd.read_csv(archivo_subido, sep=',', on_bad_lines='skip', encoding='latin-1')
    
    # ... resto del código
        
        # Generar y mostrar
        if st.button("Visualizar Ficha Técnica"):
            ficha_png = generar_ficha_png(datos_caso)
            st.image(ficha_png, caption=f"Ficha generada para el caso {codigo_seleccionado}")
            
            # Botón de descarga
            st.download_button(
                label="📥 Descargar Ficha PNG",
                data=ficha_png,
                file_name=f"Ficha_{codigo_seleccionado}.png",
                mime="image/png"
            )
else:
    st.warning("⚠️ Por favor, sube el archivo CSV para activar el sistema.")
