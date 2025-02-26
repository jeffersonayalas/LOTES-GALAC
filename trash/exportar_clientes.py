
import csv

def txt_to_csv(txt_filepath, csv_filepath, delimiter="\t"):
    """Exporta un archivo TXT a CSV.

    Args:
        txt_filepath: Ruta al archivo TXT.
        csv_filepath: Ruta al archivo CSV de salida.
        delimiter: Delimitador usado en el archivo TXT (coma por defecto).

    """

    try:
        with open(txt_filepath, 'r', encoding='latin-1') as txtfile, \
                open(csv_filepath, 'w', newline='', encoding='latin-1') as csvfile:
            reader = csv.reader(txtfile, delimiter=delimiter)
            writer = csv.writer(csvfile)
            for row in reader:
                writer.writerow(row)
    except FileNotFoundError:
        print(f"Error: El archivo TXT '{txt_filepath}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


txt_to_csv('clientes_facturas.txt', 'clientes_empresas.csv')


