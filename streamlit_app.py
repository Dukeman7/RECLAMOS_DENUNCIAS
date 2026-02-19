import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# Configuración de página
st.set_page_config(page_title="Visor de Reclamos THUNDERNET", layout="wide")

# Título y Estética Búnker
st.title("🛡️ Visor de Reclamos - Auxilio CONATEL")
st.markdown("---")

# 1. Carga de datos
uploaded_file = st.sidebar.file_uploader("Cargar Excel (.xlsm)", type=["xlsm", "xlsx"])

if uploaded_file:
    # Leemos la base de datos (ajusta el nombre de la hoja si es necesario)
    df = pd.read_excel(uploaded_file, sheet_name=0) # Asumiendo que la data está en la primera hoja
    
    # Limpieza básica de columnas para que coincidan con tus requisitos
    # (Aquí podrías mapear los nombres reales de tu Excel a estos estándar)
    
    # --- LÓGICA DE NAVEGACIÓN CON MEMORIA ---

if not df_filtered.empty:
    total_filas = len(df_filtered)
    
    # Inicializamos el índice en la memoria si no existe
if 'indice_reclamo' not in st.session_state:
    st.session_state.indice_reclamo = 0

    # Controles de navegación en la barra lateral
    st.sidebar.markdown(f"### Registro {st.session_state.indice_reclamo + 1} de {total_filas}")
    
    col_nav1, col_nav2 = st.sidebar.columns(2)
    
    with col_nav1:
        if st.button("⬅️ Anterior"):
            if st.session_state.indice_reclamo > 0:
                st.session_state.indice_reclamo -= 1
                st.rerun() # Fuerza la recarga con el nuevo dato

    with col_nav2:
        if st.button("Siguiente ➡️"):
            if st.session_state.indice_reclamo < total_filas - 1:
                st.session_state.indice_reclamo += 1
                st.rerun() # Fuerza la recarga con el nuevo dato

    # Extraer datos de la fila según la memoria
    fila = df_filtered.iloc[st.session_state.indice_reclamo]
    
    # ... (aquí sigue el resto de tu código para mostrar la ficha)
        
        # 3. Diseño de la Ficha en Pantalla (Simulando "VUELTA A CONATEL")
    col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"📋 Ficha de Reclamo: {fila.get('código', 'N/A')}")
            
            with st.container():
                st.info(f"**Denunciante:** {fila.get('Denunciante', 'N/A')} | **Cédula:** {fila.get('Cédula', 'N/A')}")
                st.warning(f"**Asunto:** {fila.get('Asunto', 'N/A')}")
                st.write(f"**Descripción:** {fila.get('Descripción', 'No hay descripción')}")
        
        with col2:
            st.error(f"**ESTATUS:** {fila.get('ESTATUS', 'N/A')}")
            st.write(f"**Fecha:** {fila.get('Fecha', 'N/A')}")
            st.write(f"**Tipo:** {fila.get('Tipo de reporte', 'N/A')}")
            st.write(f"**Ubicación:** {fila.get('Municipio', 'N/A')}, {fila.get('estado', 'N/A')}")
            st.write(f"**Teléfono:** {fila.get('Teléfono', 'N/A')}")

        # 4. Función para generar la IMAGEN (PNG)
        def generar_imagen(data):
            img = Image.new('RGB', (800, 600), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            # Nota: Para fuentes específicas, necesitarías el archivo .ttf, 
            # aquí usamos la por defecto para que no de error
            d.text((50, 50), f"RECLAMO CONATEL: {data.get('código', 'N/A')}", fill=(0, 0, 0))
            d.text((50, 100), f"Denunciante: {data.get('Denunciante', 'N/A')}", fill=(0, 0, 0))
            d.text((50, 150), f"Cédula: {data.get('Cédula', 'N/A')}", fill=(0, 0, 0))
            d.text((50, 200), f"Descripción: {str(data.get('Descripción', ''))[:100]}...", fill=(0, 0, 0))
            d.text((50, 500), f"Estatus: {data.get('ESTATUS', 'N/A')}", fill=(255, 0, 0))
            
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()

        # Botón de descarga
        btn_png = generar_imagen(fila)
        st.download_button(
            label="🖼️ Descargar Ficha como PNG",
            data=btn_png,
            file_name=f"Ficha_{fila.get('código', 'reclamo')}.png",
            mime="image/png"
        )
    else:
        st.error("No se encontraron registros.")
else:
    st.info("👋 Sube el archivo Excel de THUNDERNET para empezar a revisar.")
