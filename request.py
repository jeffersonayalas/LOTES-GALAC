import requests
from bs4 import BeautifulSoup
import re 
from datetime import datetime
from create_database import connection_database

conn = connection_database()
req =open("request.txt", "w")
info = ""

# --- ejecutar diariamente --- #
def get_bcv():
    # Making a GET request
    r = requests.get('https://www.bcv.org.ve/glosario/cambio-oficial', verify=False)
    print(r)
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', id='dolar', class_='col-sm-12')
    content = soup.find_all('strong')
    cadena_limpia = re.sub(r'</?strong>', '', str(content[4]))
    cadena_limpia = re.sub(r'\s+', '', cadena_limpia)  # Eliminar espacios en blanco
    numero_str = cadena_limpia
    numero_float = float(numero_str.replace(",", "."))
    info = ("\n"+ (str(datetime.now().date()) + ";" + str(numero_float)))
    req.write(info)
    print("Tasa del dolar: " + str(numero_float + 1) )

for i in range(10):
    get_bcv()