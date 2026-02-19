import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
import io

# Configuración de página
st.set_page_config(page_title="Visor de Reclamos THUNDERNET", layout="wide")

st.title("🛡️ Visor de Reclamos - Auxilio CONATEL")
st.markdown("---")

uploaded_file = st.sidebar.file_uploader("Cargar Plantilla (test)", type=["xlsm", "xlsx"])

if uploaded_file:
    # Leemos el Excel y limpiamos los nombres de las columnas (quitamos espacios y pasamos a minúsculas para comparar)
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip() # Limpia espacios invisibles
    
    # Buscador
    st.sidebar.header("🔍 Filtro Rápido")
    search_query = st.sidebar.text_input("Buscar por Cédula o Código")
    
    if search_query:
        df_filtered = df[df.astype(str).apply(lambda x: search_query.lower() in x.values.astype(str).lower(), axis=1)]
    else:
        df_filtered = df

    if not df_filtered.empty:
        total_filas = len(df_filtered)
        
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

        fila = df_filtered.iloc[st.session_state.idx]
        
        # --- MAPEO DINÁMICO DE COLUMNAS (Ajustado a tu archivo) ---
        # Usamos .get() con el nombre exacto que aparece en tu archivo test
        codigo = fila.get('código') or fila.get('Código') or "N/A"
        denunciante = fila.get('Denunciante') or "N/A"
        cedula = fila.get('Cédula') or "N/A"
        asunto = fila.get('Asunto') or "N/A"
        descripcion = fila.get('Descripción') or "Sin detalle"
        estatus = fila.get('ESTATUS') or "N/A"
        fecha = fila.get('Fecha') or "N/A"
        tipo = fila.get('Tipo de reporte') or "N/A"
        municipio = fila.get('Municipio') or ""
        estado_local = fila.get('estado') or fila.get('Estado') or ""
        telefono = fila.get('Teléfono') or "N/A"

        # 3. Diseño de la Ficha
        col_izq, col_der = st.columns([2, 1])
        
        with col_izq:
            st.subheader(f"📋 Ficha: {codigo}")
            st.info(f"**Denunciante:** {denunciante} | **C.I.:** {cedula}")
            st.warning(f"**Asunto:** {asunto}")
            st.markdown(f"**Descripción:**\n\n{descripcion}")
        
        with col_der:
            st.error(f"**ESTATUS:** {estatus}")
            st.write(f"📅 **Fecha:** {fecha}")
            st.write(f"🏷️ **Tipo:** {tipo}")
            st.write(f"📍 **Ubicación:** {municipio}, {estado_local}")
            st.write(f"📞 **Teléfono:** {telefono}")

        # 4. Generador de Imagen PNG
        def crear_png():
            img = Image.new('RGB', (800, 600), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            d.text((40, 40), f"RECLAMO: {codigo}", fill=(0,0,0))
            d.text((40, 80), f"DENUNCIANTE: {denunciante}", fill=(0,0,0))
            d.text((40, 120), f"CEDULA: {cedula}", fill=(0,0,0))
            d.text((40, 520), f"ESTATUS: {estatus}", fill=(200,0,0))
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            return buf.getvalue()

        st.download_button(
            label="📥 Descargar Ficha (PNG)",
            data=crear_png(),
            file_name=f"Ficha_{codigo}.png",
            mime="image/png"
        )
    else:
        st.error("No hay datos que coincidan.")
else:
    st.info("💡 Sube el archivo para activar el búnker de reclamos.")
