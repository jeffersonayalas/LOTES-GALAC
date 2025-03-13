import sys
import threading
from database.inter_database import update_database, update_drafts
from app.main import execute_data
from app.api_odoo import api_data
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QPushButton, QVBoxLayout, QHBoxLayout, 
                             QFileDialog, QLineEdit, QMainWindow, QTextEdit, 
                             QTabWidget, QSplitter, QGridLayout, QDateEdit, 
                             QListWidget, QListWidgetItem)


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FACTURACION POR LOTES - ODOO/GALAC")

        # Inicializar atributos para controlar los hilos
        self.hilo_fusion = None
        self.hilo_actualizacion = None
        self.cancelar_hilos = False  # Bandera para indicar que se deben cancelar los hilos

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

        self.ventana1 = VentanaPrincipal(fecha)
        self.ventana1.setGeometry(800, 500, 800, 500)
        layoutPrincipal.addWidget(self.ventana1, 1, 1)  # Fila 1, Columna 1

        self.ventana2 = VentanaArchivo(fecha)
        self.ventana2.setGeometry(500, 500, 500, 500)
        layoutPrincipal.addWidget(self.ventana2, 1, 0)  # Fila 1, Columna 0

        layoutPrincipal.setRowStretch(1, 1)  # Asegura que la fila con las ventanas sea flexible
        layoutPrincipal.setColumnStretch(1, 1)  # Asegura que la columna con las ventanas sea flexible

        widgetCentral = QWidget()
        widgetCentral.setLayout(layoutPrincipal)

        widgetCentral.setStyleSheet("border: 0.5px solid rgb(0, 165, 248); padding: 10px; border-radius: 5px")

        # Establecer el widget central en la ventana principal
        self.setCentralWidget(widgetCentral)
        self.cancelar_hilos = False

    def closeEvent(self, event):
        # Establece la bandera para cancelar los hilos
        self.cancelar_hilos = True

        if self.ventana1.hilo_fusion is not None and self.ventana1.hilo_fusion.is_alive():
            self.ventana1.cancelar_hilos = True  # Cancelar el hilo de fusión

        if self.ventana2.hilo_actualizacion is not None and self.ventana2.hilo_actualizacion.is_alive():
            self.ventana2.cancelar_hilos = True  # Cancelar el hilo de actualización

        event.accept()  # Aceptar el evento de cierre de ventana


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
    contenido_archivo_obtenido = pyqtSignal(str)

    def __init__(self, fecha):
        super().__init__()
        
        self.estado_resultado = False
        self.ruta_excel = None
        self.setWindowTitle("FACTURACION POR LOTES - GALAC/ODOO")
        self.fecha_data = fecha

        self.etiqueta_resultado = QLabel("")
        self.etiqueta_resultado.setObjectName("etiqueta_resultado")  # Asigna ID para el QLabel resultado
        self.button_fusionar = QPushButton("FUSIONAR", self)
        self.button_actualizar = QPushButton("ACTUALIZAR BORRADORES", self)  # Nuevo botón para actualizar borradores
        self.etiqueta_tipo = QLabel("Clientes a facturar: ")

        # Crear el QListWidget para el checklist
        self.checklist = QListWidget()
        items = ['Clientes en Bolivares', 'Clientes en Divisas']
        self.checklist.setFixedSize(QSize(250, 70))

        # Añadir elementos al checklist
        for item in items:
            list_item = QListWidgetItem(item)
            list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)  # Hacer el item chequeable
            list_item.setCheckState(Qt.Unchecked)  # Estado inicial: desmarcado
            self.checklist.addItem(list_item)

        self.texto_edit = QTextEdit(self)
        self.texto_edit.setReadOnly(True)  # Para evitar modificaciones
        self.texto_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Layouts
        disenio_horizontal_monto = QHBoxLayout()
        disenio_horizontal_monto.addWidget(self.etiqueta_tipo)
        disenio_horizontal_monto.addWidget(self.checklist)

        disenio_vertical = QVBoxLayout()
        disenio_vertical.addLayout(disenio_horizontal_monto)
        disenio_vertical.addWidget(self.texto_edit)
        disenio_vertical.addWidget(self.etiqueta_resultado)
        disenio_vertical.addWidget(self.button_fusionar)
        disenio_vertical.addWidget(self.button_actualizar)  # Añadir el botón de actualización

        self.setLayout(disenio_vertical)

        # Conectar señales y slots
        self.contenido_archivo_obtenido.connect(self.mostrar_contenido_archivo)
        self.button_fusionar.clicked.connect(self.enviar_datos)
        self.button_actualizar.clicked.connect(self.actualizar_borradores)  # Conectar botón a la función
        
    # El resto de tu implementación...

    def actualizar_borradores(self):
        try:
            self.etiqueta_resultado.setText("Actualizando la base de datos, por favor espere...")
            # Llama a la función para actualizar la base de datos
            update_drafts()  # Asegúrate de pasar el archivo correcto
            self.etiqueta_resultado.setText("Base de datos actualizada.")  # Mensaje de éxito

        except FileNotFoundError:
            self.etiqueta_resultado.setText("Error: Archivo no encontrado.")
        except Exception as e:
            self.etiqueta_resultado.setText(f"Error al actualizar la base de datos: {str(e)}")

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
            
            # Inicializa la bandera de cancelación antes de crear el hilo
            self.parent().cancelar_hilos = False

            # Crea un hilo para la operación de fusión
            hilo_fusion = threading.Thread(target=self.ejecutar_api_data, args=(tipos_clientes,))
            hilo_fusion.start()

        except ValueError:
            self.etiqueta_resultado.setText("Error: Ingresa un monto válido.")
        except FileNotFoundError:
            self.etiqueta_resultado.setText("Error: Archivo no encontrado.")

    def ejecutar_api_data(self, tipos_clientes):
        self.main_window = QApplication.activeWindow()
        if not self.main_window.cancelar_hilos:
            # Aquí tus operaciones de API:
            fecha_seleccionada = self.main_window.date_edit.date().toString("yyyy-MM-dd")  # Obtener la fecha seleccionada
            try:
                archivo_resultado = api_data(1, fecha_seleccionada, tipos_clientes)
                self.leer_contenido_archivo(archivo_resultado)
            except Exception as e:
                print(f"Error en api_data: {str(e)}")
                

        if self.main_window.cancelar_hilos:
            print("Proceso cancelado.")
        

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
        self.boton_archivo = QPushButton("VERIFICAR CLIENTES", self)
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
            main_window = QApplication.activeWindow()
            # Inicializa la bandera de cancelación antes de crear el hilo
            self.parent().cancelar_hilos = False
            # Crea un hilo para la operación
            hilo_actualizacion = threading.Thread(target=self.ejecutar_api_data)
            hilo_actualizacion.start()
        except ValueError:
            self.etiqueta.setText("Error: Ingresa un monto válido.")
        except FileNotFoundError:
            self.etiqueta.setText("Error: Archivo no encontrado.")

    def ejecutar_api_data(self):
        self.main_window = QApplication.activeWindow()
        if not self.main_window.cancelar_hilos:
            
            fecha_seleccionada = self.main_window.date_edit.date().toString("yyyy-MM-dd")
            try:
                archivo_resultado = api_data(0, fecha_seleccionada)
                self.leer_contenido_archivo(archivo_resultado)
            except Exception as e:
                print(f"Error en api_data en VentanaArchivo: {str(e)}")

        if self.main_window.cancelar_hilos:
            print("Proceso cancelado en VentanaArchivo.")

       

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
            """ 
            result = self.actualizar_database()

            if result:
                self.etiqueta.setText("Base de datos actualizada")
            else:
                self.etiqueta.setText("Terminado")"
            """
            self.etiqueta.setText("Terminado")
        else:
            self.texto.setPlainText("")  # Limpiar el contenido anterior
            self.etiqueta.setText(data[1])  # Mostrar error en la interfaz de usuario

    def actualizar_database(self):
        #Se llama a funcion para actualizar la base de datos y se le pasa el archivo
        archivo_actualizacion = open('clientes_faltantes.txt', 'r')
        update_database(archivo_actualizacion)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("app/styles/estilos.qss", "r") as f:  # leer los estilos del archivo
        app.setStyleSheet(f.read())
    ventana = Ventana()
    ventana.setGeometry(1000, 800, 1000, 800)
    ventana.show()
    sys.exit(app.exec_())
