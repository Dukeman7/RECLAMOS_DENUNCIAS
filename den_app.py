if archivo_subido:
    try:
        # Intentamos con separador por defecto (coma) pero ignorando errores de filas
        df = pd.read_csv(
            archivo_subido, 
            sep=None,             # Detecta automáticamente si es coma o punto y coma
            engine='python',      # El motor Python es más lento pero más robusto
            on_bad_lines='skip',  # Si una fila tiene errores, se la salta y no mata la App
            encoding='utf-8'      # Ya que pasamos por el Bloc de Notas
        )
    except Exception as e:
        # Segundo intento por si el primero falla catastróficamente
        archivo_subido.seek(0)
        df = pd.read_csv(archivo_subido, sep=',', on_bad_lines='skip', encoding='latin-1')
    
    if not df.empty:
        st.success(f"🚀 Base de datos cargada: {len(df)} registros procesados.")
    else:
        st.error("El archivo parece estar vacío o no se pudo procesar.")
