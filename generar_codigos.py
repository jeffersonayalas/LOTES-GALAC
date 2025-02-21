import random
import string

generados = set()

def generar_codigo_cliente():
    while True:
        # Generar un nuevo código
        primera_letra = random.choice(string.ascii_uppercase)
        dos_digitos = f"{random.randint(0, 99):02d}"
        tres_letras_1 = ''.join(random.choices(string.ascii_uppercase, k=3))
        un_digito = str(random.randint(0, 9))
        tres_letras_2 = ''.join(random.choices(string.ascii_uppercase, k=3))
        
        codigo_cliente = f"{primera_letra}{dos_digitos}{tres_letras_1}{un_digito}{tres_letras_2}"

        # Verificar si el código ya ha sido generado
        #Aca se realiza consulta a la base de datos 
        if codigo_cliente not in generados:
            generados.add(codigo_cliente)  # Agregar el código al conjunto
            return codigo_cliente  # Retornar el nuevo código
        else:
            generar_codigo_cliente()
            return codigo_cliente

# Generar un código de ejemplo
codigo = generar_codigo_cliente()
print("Código de cliente generado:", codigo)


# Ejemplo de uso
for i in range(100):
    codigo = generar_codigo_cliente()
    print("Código de cliente generado:", codigo)