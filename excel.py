import csv
from openpyxl import Workbook

def txt_a_excel_csv(ruta_txt, ruta_excel):
    """Convierte un archivo TXT (CSV) a un archivo Excel."""
    try:
        workbook = Workbook()
        sheet = workbook.active

        with open(ruta_txt, 'r', encoding='utf-8') as archivo_txt:
            lector_csv = csv.reader(archivo_txt)
            for fila in lector_csv:
                sheet.append(fila)

        workbook.save(ruta_excel)
        print(f"Archivo TXT '{ruta_txt}' convertido a Excel '{ruta_excel}' exitosamente.")

    except FileNotFoundError:
        print(f"Error: Archivo '{ruta_txt}' no encontrado.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


ruta_txt = "mi_archivo.txt"  # Reemplaza con la ruta de tu archivo TXT
ruta_excel = "mi_archivo.xlsx"  # Reemplaza con la ruta y nombre del archivo Excel de salida

txt_a_excel_csv(ruta_txt, ruta_excel)