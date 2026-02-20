def generar_ficha_pro(data):
    width, height = 800, 1000  # Más vertical para incluir el área de firma
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    azul_venapp = (27, 79, 114)
    gris_borde = (200, 200, 200)
    rojo_status = (255, 0, 0)

    # 1. Encabezado Principal
    d.rectangle([0, 0, width, 80], fill=azul_venapp)
    d.text((width//2 - 150, 30), "FICHA DE RECLAMO - MODO AUTOMATION", fill=(255, 255, 255))

    # 2. Código y Estatus
    d.text((40, 110), f"CÓDIGO: {data.get('Código', 'S/D')}", fill=(30, 30, 30))
    d.text((width - 200, 110), f"ESTATUS: {data.get('ESTATUS', 'ABIERTO')}", fill=rojo_status)

    # 3. Bloque: DATOS DEL CLIENTE
    d.rectangle([40, 150, width-40, 250], outline=gris_borde, width=2)
    d.text((50, 155), "DATOS DEL CLIENTE", fill=azul_venapp)
    d.text((60, 185), f"Nombre: {data.get('Denunciante', 'S/D')}", fill=(0, 0, 0))
    # Línea compartida: Cédula | Telf | Email
    info_contacto = f"Cédula: {data.get('Cédula Denunciante', 'S/D')}  |  Telf: {data.get('Teléfono Denunciante', 'S/D')}  |  Email: {data.get('Correo', 'S/D')}"
    d.text((60, 215), info_contacto, fill=(0, 0, 0))

    # 4. Bloque: UBICACIÓN
    d.rectangle([40, 270, width-40, 370], outline=gris_borde, width=2)
    d.text((50, 275), "UBICACIÓN DEL INCIDENTE", fill=azul_venapp)
    ubicacion = f"Estado: {data.get('Estado', 'S/D')} | Municipio: {data.get('Municipio', 'S/D')} | Parroquia: {data.get('Parroquia', 'S/D')}"
    d.text((60, 305), ubicacion, fill=(0, 0, 0))
    d.text((60, 335), f"Dirección: {data.get('Dirección', 'Ver detalle en descripción')}", fill=(0, 0, 0))

    # 5. Bloque: DETALLE DEL RECLAMO
    d.rectangle([40, 390, width-40, 650], outline=gris_borde, width=2)
    d.text((50, 395), "DETALLE DEL RECLAMO", fill=azul_duque)
    d.text((60, 425), f"Categoría: {data.get('Asunto', 'S/D')}", fill=(0, 0, 0))
    
    desc_cuerpo = str(data.get('Descripción', 'S/D'))
    lines = [desc_cuerpo[i:i+85] for i in range(0, len(desc_cuerpo), 85)][:6]
    y_desc = 460
    d.text((60, 460), "Descripción del Ciudadano:", fill=(30, 30, 30))
    for line in lines:
        y_desc += 25
        d.text((60, y_desc), line, fill=(60, 60, 60))

    # 6. Bloque: GESTIÓN INTERNA (Para Daniel)
    d.rectangle([40, 670, width-40, 950], fill=(245, 248, 250), outline=gris_borde)
    d.text((50, 675), "PARA USO INTERNO / GESTIÓN DE RESPUESTA", fill=azul_venapp)
    d.text((60, 710), "Respuesta Técnica / Acción Tomada:", fill=(100, 100, 100))
    # Recuadro blanco para escribir
    d.rectangle([60, 740, width-60, 880], fill=(255, 255, 255), outline=gris_borde)
    
    d.text((60, 910), "Firma / Responsable: __________________________", fill=(30, 30, 30))
    d.text((width-250, 910), "Fecha de Cierre: __ / __ / __", fill=(30, 30, 30))

    # Guardar
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
