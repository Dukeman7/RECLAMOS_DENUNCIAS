import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# Configuración de página - Modo Búnker
st.set_page_config(page_title="Visor de Reclamos THUNDERNET", layout="wide")

# Título con estilo
st.title("🛡️ Visor de Reclamos - Auxilio CONATEL")
st.markdown("---")

# 1. Carga del archivo simplificado (.xlsm con una pestaña)
uploaded_file = st.sidebar.file_uploader("Cargar Plantilla (test)", type=["xlsm", "xlsx"])

if uploaded_file:
    # Leemos la única pestaña disponible
    df = pd.read_excel(uploaded_file) 
    
    # Buscador en la barra lateral
    st.sidebar.header("🔍 Filtro Rápido")
    search_query = st.sidebar.text_input("Buscar por Cédula o Código")
    
    if search_query:
        df_filtered = df[df.astype(str).apply(lambda x: search_query in x.values, axis=1)]
    else:
        df_filtered = df

    # --- NAVEGACIÓN CON MEMORIA DE ESTADO ---
    if not df_filtered.empty:
        total_filas = len(df_filtered)
        
        # Sincronizamos el índice
        if 'idx' not in st.session_state or st.session_state.idx >= total_filas:
            st.session_state.idx = 0

        st.sidebar.markdown(f"### Registro {st.session_state.idx + 1} de {total_filas}")
        
        c1, c2 = st.sidebar.columns(2)
        with c1:
            if st.button("⬅️ Anterior"):
                if st.session_state.idx > 0:
                    st.session_state.idx -= 1
                    st.rerun()
        with c2:
            if st.button("Siguiente ➡️"):
                if st.session_state.idx < total_filas - 1:
                    st.session_state.idx += 1
                    st.rerun()

        # Extraer fila actual
        fila = df_filtered.iloc[st.session_state.idx]
        
        # 3. La Ficha en Pantalla (Campos Imprescindibles)
        col_izq, col_der = st.columns([2, 1])
        
        with col_izq:
            st.subheader(f"📋 Ficha: {fila.get('código', 'N/A')}")
            st.info(f"**Denunciante:** {fila.get('Denunciante', 'N/A')} | **C.I.:** {fila.get('Cédula', 'N/A')}")
            st.warning(f"**Asunto:** {fila.get('Asunto', 'N/A')}")
            st.markdown(f"**Descripción:**\n\n{fila.get('Descripción', 'Sin detalle')}")
        
        with col_der:
            st.error(f"**ESTATUS:** {fila.get('ESTATUS', 'N/A')}")
            st.write(f"📅 **Fecha:** {fila.get('Fecha', 'N/A')}")
            st.write(f"🏷️ **Tipo:** {fila.get('Tipo de reporte', 'N/A')}")
            st.write(f"📍 **Ubicación:** {fila.get('Municipio', 'N/A')}, {fila.get('estado', 'N/A')}")
            st.write(f"📞 **Teléfono:** {fila.get('Teléfono', 'N/A')}")

        # 4. Generador de Imagen PNG
        def crear_png(data):
            # Lienzo blanco
            img = Image.new('RGB', (800, 600), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            # Dibujamos los datos básicos (Simulacro de Ficha)
            d.text((40, 40), f"RECLAMO: {data.get('código', 'N/A')}", fill=(0,0,0))
            d.text((40, 80), f"DENUNCIANTE: {data.get('Denunciante', 'N/A')}", fill=(0,0,0))
            d.text((40, 120), f"CEDULA: {data.get('Cédula', 'N/A')}", fill=(0,0,0))
            d.text((40, 520), f"ESTATUS: {data.get('ESTATUS', 'N/A')}", fill=(200,0,0))
            
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            return buf.getvalue()

        st.download_button(
            label="📥 Descargar Ficha (PNG)",
            data=crear_png(fila),
            file_name=f"Ficha_{fila.get('código', 'export')}.png",
            mime="image/png"
        )
    else:
        st.error("No hay datos que coincidan con la búsqueda.")
else:
    st.info("💡 Por favor, sube el archivo 'plantilla reclamos VENAPP (test).xlsm' para visualizar las fichas.")
