import sys
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QPushButton, QVBoxLayout, QHBoxLayout, 
                             QFileDialog, QLineEdit, QMainWindow, QTextEdit, 
                             QTabWidget, QSplitter, QGridLayout, QDateEdit, 
                             QListWidget, QListWidgetItem)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from operate_database import main_database, update_database, connection_database
from main import execute_data
from api_odoo_prueba import api_data

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FACTURACION POR LOTES - ODOO/GALAC")

        # Crear el campo de fecha
        self.fecha = QLabel("Seleccione una fecha:")
        self.date_edit = QDateEdit(self)
        self.date_edit.setDate(QDate.currentDate())  # Establecer la fecha actual como valor por defecto
        self.date_edit.setDisplayFormat("yyyy-MM-dd")  # Formato de visualización

        fecha = self.date_edit.date()

        # Crear un layout horizontal para la fecha
        layout_fecha = QHBoxLayout()
        layout_fecha.addWidget(self.fecha)
        layout_fecha.addWidget(self.date_edit)

        # Layout de grilla principal
        layoutPrincipal = QGridLayout()
        
        # Añadir el layout de fecha en la parte superior
        layoutPrincipal.addLayout(layout_fecha, 0, 0, 1, 2)  # Fila 0, columna 0, ocupa 1 fila y 2 columnas

        ventana1 = VentanaPrincipal(fecha)
        ventana1.setGeometry(800, 500, 800, 500)
        layoutPrincipal.addWidget(ventana1, 1, 1)  # Fila 1, Columna 1

        ventana2 = VentanaArchivo(fecha)
        ventana2.setGeometry(500, 500, 500, 500)
        layoutPrincipal.addWidget(ventana2, 1, 0)  # Fila 1, Columna 0

        layoutPrincipal.setRowStretch(1, 1)  # Asegura que la fila con las ventanas sea flexible
        layoutPrincipal.setColumnStretch(1, 1)  # Asegura que la columna con las ventanas sea flexible

        widgetCentral = QWidget()
        widgetCentral.setLayout(layoutPrincipal)

        widgetCentral.setStyleSheet("border: 0.5px solid rgb(0, 165, 248); padding: 10px; border-radius: 5px")

        # Establecer el widget central en la ventana principal
        self.setCentralWidget(widgetCentral)


    def center(self):
        # Obtener el tamaño de la ventana
        tamanio_ventana = self.frameGeometry()
        # Obtener la resolución de la pantalla
        pantalla = QApplication.primaryScreen().availableGeometry()
        
        # Calcular la posición centrada
        x = (pantalla.width() - tamanio_ventana.width()) // 2
        y = (pantalla.height() - tamanio_ventana.height()) // 2

        # Mover la ventana a la posición calculada
        self.move(x, y)

    #Funcion obtiene la ventana a la cual va a aplicar los cambios 
    def cargar_contenido_archivo(self, ruta_archivo, ventana):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()  # Leer todo el archivo
                self.texto.setPlainText(contenido)  # Establecer el contenido en el QTextEdit
        except Exception as e:
            self.etiqueta.setText(f"Error al cargar el archivo: {str(e)}")  # Manejo de errores

    def process(ventana):
        # Llama a api_data y emite el resultado
        resultado = api_data(1, ventana.fecha_data)  # Llama a la función
        return resultado
        self.resultado_obtenido.emit(resultado)  # Emitir el resultado a través de la señal

class VentanaPrincipal(QWidget):
    # Definir la señal que enviará el resultado
    contenido_archivo_obtenido = pyqtSignal(str)

    def __init__(self, fecha):
        super().__init__()

        self.estado_resultado = False
        self.ruta_excel = None
        self.setWindowTitle("FACTURACION POR LOTES - GALAC/ODOO")
        self.fecha_data = fecha

        self.etiqueta_resultado = QLabel("")
        self.etiqueta_resultado.setObjectName("etiqueta_resultado")  # Asigna el ID para el QLabel resultado
        self.button = QPushButton("FUSIONAR", self)
        self.etiqueta_tipo = QLabel("Clientes a facturar: ")

        # Crear el QListWidget para el checklist
        self.checklist = QListWidget()
        items = ['Clientes en Bolivares', 'Clientes en Divisas']
        self.checklist.setFixedSize(QSize(250, 70))

        # Añadir elementos al checklist
        for item in items:
            list_item = QListWidgetItem(item)
            list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)  # Hacer el elemento chequeable
            list_item.setCheckState(Qt.Unchecked)  # Estado inicial: desmarcado
            self.checklist.addItem(list_item)

        self.texto_edit = QTextEdit(self)
        self.texto_edit.setReadOnly(True)  # Para evitar modificaciones
        self.texto_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        disenio_horizontal_monto = QHBoxLayout()
        disenio_horizontal_monto.addWidget(self.etiqueta_tipo)
        disenio_horizontal_monto.addWidget(self.checklist)

        disenio_vertical = QVBoxLayout()
        disenio_vertical.addLayout(disenio_horizontal_monto)
        disenio_vertical.addWidget(self.texto_edit)
        disenio_vertical.addWidget(self.etiqueta_resultado)
        disenio_vertical.addWidget(self.button)
        self.setLayout(disenio_vertical)

        # Conectar señal y slot para mostrar el contenido
        self.contenido_archivo_obtenido.connect(self.mostrar_contenido_archivo)

        self.button.clicked.connect(self.enviar_datos)

    def obtener_tipos_clientes(self):
        """Verifica los tipos de clientes seleccionados en el checklist."""
        tipos_clientes = []
        for index in range(self.checklist.count()):
            item = self.checklist.item(index)
            if item.checkState() == Qt.Checked:
                tipos_clientes.append(item.text())
        return tipos_clientes

    def enviar_datos(self):
        try:
            # Muestra el mensaje de espera
            self.etiqueta_resultado.setText("Espere unos segundos...")

            # Obtener los tipos de clientes seleccionados
            tipos_clientes = self.obtener_tipos_clientes()
            if not tipos_clientes:
                self.etiqueta_resultado.setText("Selecciona al menos un tipo de cliente.")
                return

            # Crea un hilo para la operación de fusión
            hilo_fusion = threading.Thread(target=self.ejecutar_api_data, args=(tipos_clientes,))
            hilo_fusion.start()

        except ValueError:
            self.etiqueta_resultado.setText("Error: Ingresa un monto válido.")
        except FileNotFoundError:
            self.etiqueta_resultado.setText("Error: Archivo no encontrado.")

    def ejecutar_api_data(self, tipos_clientes):
        # Aquí puedes usar tipos_clientes para procesar la lógica necesaria
        # Por ejemplo, puedes pasarlos a la función api_data
        archivo_resultado = api_data(1, self.fecha_data, tipos_clientes)  # Asegúrate de que tu función api_data esté ajustada para recibir esto
        self.leer_contenido_archivo(archivo_resultado)  # Leer el contenido del archivo

    def leer_contenido_archivo(self, archivo):
        try:
            contenido = archivo.read()  # Leer todo el contenido del archivo
            self.contenido_archivo_obtenido.emit(contenido)  # Emitir el contenido leído
            archivo.close()  # Cerrar el archivo después de leer
        except Exception as e:
            self.etiqueta_resultado.setText(f"Error al leer el archivo: {str(e)}")  # Manejo de errores

    @pyqtSlot(str)
    def mostrar_contenido_archivo(self, contenido):
        self.texto_edit.setPlainText(contenido)  # Mostrar el contenido en QTextEdit
        self.etiqueta_resultado.setText("Contenido cargado correctamente.")  # Mensaje de éxito

class VentanaArchivo(QWidget):
    # Señal para comunicar la actualización completada
    actualizarFinished = pyqtSignal(tuple)

    def __init__(self, fecha, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Archivo TXT")
        self.fecha_data = fecha
        self.ruta_txt = None
        self.initUI()

    def initUI(self):
        self.boton_archivo = QPushButton("Verificación de Clientes", self)
        self.boton_archivo.clicked.connect(self.enviar_datos)
        self.etiqueta = QLabel("")
        self.etiqueta.setObjectName("etiqueta_resultado")
        self.texto = QTextEdit(self)
        self.texto.setReadOnly(True)  # Para evitar modificaciones

        layout = QVBoxLayout()
        layout.addWidget(self.texto)
        layout.addWidget(self.etiqueta)
        layout.addWidget(self.boton_archivo)
        self.setLayout(layout)  # Uso de setLayout en lugar de setCentralWidget

        # Conectar señal a la función para actualizar GUI
        self.actualizarFinished.connect(self.mostrar_resultado_actualizacion)

    def enviar_datos(self):
        try:
            # Muestra el mensaje de espera
            self.etiqueta.setText("Espere unos segundos...")
            # Crea un hilo para la operación
            hilo_actualizacion = threading.Thread(target=self.ejecutar_api_data)
            hilo_actualizacion.start()
        except ValueError:
            self.etiqueta.setText("Error: Ingresa un monto válido.")
        except FileNotFoundError:
            self.etiqueta.setText("Error: Archivo no encontrado.")

    def ejecutar_api_data(self):
        # Obtener el archivo abierto de api_data
        archivo_resultado = api_data(0, self.fecha_data)  # Llamar a la función que retorna un archivo abierto
        print(archivo_resultado)
        self.leer_contenido_archivo(archivo_resultado)  # Leer el contenido del archivo

    def leer_contenido_archivo(self, archivo):
        try:
            contenido = archivo.read()  # Leer todo el contenido del archivo
            self.actualizarFinished.emit((True, contenido))  # Emitir señal con el contenido leído
            archivo.close()  # Cerrar el archivo después de leer
        except Exception as e:
            self.actualizarFinished.emit((False, f"Error al leer el archivo: {str(e)}"))  # Emitir error si ocurre

    @pyqtSlot(tuple)
    def mostrar_resultado_actualizacion(self, data):
        if data[0]:
            self.texto.setPlainText(data[1])  # Mostrar el contenido en QTextEdit
            #Aqui se realiza llamada para actualizacion de base de datos 
            self.actualizar_database()

            self.etiqueta.setText("Base de datos actualizada")
        else:
            self.texto.setPlainText("")  # Limpiar el contenido anterior
            self.etiqueta.setText(data[1])  # Mostrar error en la interfaz de usuario

    def actualizar_database(self):
        #Se llama a funcion para actualizar la base de datos y se le pasa el archivo
        archivo_actualizacion = open('clientes_faltantes.txt', 'r')
        update_database(archivo_actualizacion)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("estilos.qss", "r") as f:  # leer los estilos del archivo
        app.setStyleSheet(f.read())
    ventana = Ventana()
    ventana.setGeometry(1000, 800, 1000, 800)
    ventana.show()
    sys.exit(app.exec_())
