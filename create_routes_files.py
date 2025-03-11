import os

def list_directory_structure(startpath, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(startpath):
            # Ignorar las carpetas 'venv' y '.git'
            if 'venv' in dirs:
                dirs.remove('venv')  # Esto evita que se recorra la carpeta 'venv'
            if '.git' in dirs:
                dirs.remove('.git')  # Esto evita que se recorra la carpeta '.git'
            if 'trash' in dirs:
                dirs.remove('trash') 

            # Calculamos la profundidad del directorio actual
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)  # Indentación para el nivel
            f.write(f"{indent}{os.path.basename(root)}/\n")  # Carpeta
            for file in files:
                f.write(f"{indent}    {file}\n")  # Archivos

# Ruta donde se encuentra tu proyecto
project_path = '/home/desarrollo/Escritorio/pruebas/GALAC'  # Cambia esto a la ruta de tu proyecto
output_txt_file = 'estructura_proyecto.txt'

list_directory_structure(project_path, output_txt_file)

print(f"Estructura de directorios guardada en '{output_txt_file}'.")



