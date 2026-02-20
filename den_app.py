import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Ficha-Bot Duque", layout="wide")

# 2. FUNCIÓN DE DISEÑO (El motor gráfico)
def generar_ficha_png(data):
    # Lienzo HD
    width, height = 450, 750
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    azul_conatel = (0, 51, 102)
    gris_fondo = (245, 245, 245)
    
    # Encabezado
    d.rectangle([0, 0, width, 120], fill=azul_conatel)
    # Usamos draw.text sin fuentes externas para evitar errores de archivo en el servidor
    d.text((40, 30), "REPORTE DE INCIDENCIA REGULATORIA", fill=(200, 200, 200))
    d.text((40, 55), f"CODIGO: {data.get('Código', 'N/A')}", fill=(255, 255, 255))
    
    # Cuerpo de datos
    d.rectangle([40, 150, 860, 550], outline=(220, 220, 220), width=2)
    y = 170
    
    # Mapeo de campos
    fields = [
        ("OPERADOR", str(data.get('OPERADOR', 'THUNDERNET'))),
        ("FECHA", str(data.get('FECHA', 'S/D'))),
        ("DENUNCIANTE", str(data.get('Denunciante', 'S/D'))),
        ("CEDULA", str(data.get('Cédula Denunciante', 'S/D'))),
        ("TELEFONO", str(data.get('Teléfono Denunciante', 'S/D'))),
        ("UBICACION", f"{data.get('Estado', '')} / {data.get('Municipio', '')}"),
        ("ASUNTO", str(data.get('Asunto', 'S/D'))),
    ]
    
    for label, value in fields:
        d.text((60, y), f"{label}:", fill=azul_conatel)
        d.text((220, y), str(value), fill=(30, 30, 30))
        y += 45

    # Descripción
    d.text((60, y), "DESCRIPCION:", fill=azul_conatel)
    desc = str(data.get('Descripción', 'Sin descripción'))
    # Ajuste de texto simple para que no se desborde
    lines = [desc[i:i+80] for i in range(0, len(desc), 80)][:6]
    y += 30
    for line in lines:
        d.text((60, y), line, fill=(80, 80, 80))
        y += 25
        
    # Pie de página
    d.rectangle([0, 680, width, 750], fill=gris_fondo)
    d.text((40, 705), "SISTEMA DE GESTION REGULATORIA DUQUE - MODO AUTOMATION", fill=(100, 100, 100))

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# 3. INTERFAZ DE USUARIO
st.title("🚀 Ficha-Bot: Inteligencia de Denuncias")
st.markdown("Generación de fichas técnicas para casos CONATEL / VenApp.")

# Cargador
archivo_subido = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo_subido is not None:
    try:
        # Intento con motor flexible
        df = pd.read_csv(archivo_subido, sep=None, engine='python', on_bad_lines='skip', encoding='utf-8')
    except Exception:
        archivo_subido.seek(0)
        df = pd.read_csv(archivo_subido, sep=',', on_bad_lines='skip', encoding='latin-1')

    if not df.empty:
        st.success(f"✅ Se cargaron {len(df)} registros correctamente.")
        
        # Verificamos que exista la columna crítica
        if 'Código' in df.columns:
            codigo_sel = st.selectbox("Selecciona el Código a procesar:", df['Código'].unique())
            
            if codigo_sel:
                # Filtrar el caso seleccionado
                datos_caso = df[df['Código'] == codigo_sel].iloc[0]
                
                # Botón para disparar la generación
                if st.button("Generar Ficha Visual"):
                    with st.spinner('Dibujando ficha...'):
                        ficha_png = generar_ficha_png(datos_caso)
                        st.image(ficha_png, caption=f"Ficha generada para el caso {codigo_sel}")
                        
                        st.download_button(
                            label="📥 Descargar Ficha PNG",
                            data=ficha_png,
                            file_name=f"Ficha_{codigo_sel}.png",
                            mime="image/png"
                        )
        else:
            st.error("Error: La columna 'Código' no fue detectada. Verifica el encabezado de tu CSV.")
    else:
        st.warning("El archivo parece estar vacío.")
