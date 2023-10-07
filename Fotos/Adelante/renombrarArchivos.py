import os

# Directorio donde se encuentran los archivos que deseas renombrar
directorio = "p"
i=0
# Obtener una lista de los archivos en el directorio
archivos = os.listdir(directorio)

# Iterar a través de los archivos y renombrarlos
for archivo in archivos:
    # Verificar si el archivo cumple con ciertos criterios antes de renombrarlo
    if archivo.endswith(".jpg"):
        # Construir el nuevo nombre de archivo
        nuevo_nombre = "objeto_" + str(i)+".jpg"
        i+=1
        
        # Crear la ruta completa para el archivo antiguo y el nuevo nombre
        ruta_antigua = os.path.join(directorio, archivo)
        ruta_nueva = os.path.join(directorio, nuevo_nombre)
        
        # Renombrar el archivo
        os.rename(ruta_antigua, ruta_nueva)
        print(f"Renombrado: {ruta_antigua} -> {ruta_nueva}")