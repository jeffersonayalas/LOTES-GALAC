import sys
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit, QMainWindow, QTextEdit, QTabWidget, QSplitter, QGridLayout, QDateEdit)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from create_database import main_database, update_database
from main import execute_data


class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FACTURACION POR LOTES - ODOO/GALAC")

        # Layout de grilla
        layoutPrincipal = QGridLayout()
        ventana1 = VentanaPrincipal()
        ventana1.setGeometry(800, 500, 800, 500)
        ventana2 = VentanaArchivo()
        ventana2.setGeometry(500, 500, 500, 500)
        layoutPrincipal.addWidget(ventana1, 0, 1)
        layoutPrincipal.addWidget(ventana2, 0, 0)  # Fila 0, Columna 0
        layoutPrincipal.setRowStretch(0, 1)
        layoutPrincipal.setColumnStretch(1, 1)
        widgetCentral = QWidget()
        widgetCentral.setLayout(layoutPrincipal)
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


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.estado_resultado = False
        self.ruta_excel = None
        self.setWindowTitle("FACTURACION POR LOTES - GALAC/ODOO")

        self.etiqueta_resultado = QLabel("")
        self.etiqueta_resultado.setObjectName("etiqueta_resultado")  # asigna el ID para el QLabel resultado

        self.etiqueta_excel = QLabel("Archivo Excel:")
        self.entrada_excel = QLineEdit()
        self.boton_excel = QPushButton("Seleccionar")
        self.boton_crear_bd = QPushButton("Crear Base de datos", self)
        self.button = QPushButton("FUSIONAR", self)

        self.boton_excel.clicked.connect(self.seleccionar_excel)
        self.texto_edit = QTextEdit(self)
        self.texto_edit.setReadOnly(True)  # Para evitar modificaciones
        self.texto_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.etiqueta_monto = QLabel("Tasa del Banco (BCV):")
        self.entrada_monto = QLineEdit()

        self.etiqueta_impuesto = QLabel("Aplicar impuestos")
    
        self.fecha = QLabel("Seleccione una fecha:")

        # Crear el campo de fecha
        self.date_edit = QDateEdit(self)
        self.date_edit.setDate(QDate.currentDate())  # Establecer la fecha actual como valor por defecto
        self.date_edit.setDisplayFormat("yyyy-MM-dd")  # Formato de visualización

        disenio_horizontal_excel = QHBoxLayout()
        disenio_horizontal_excel.addWidget(self.etiqueta_excel)
        disenio_horizontal_excel.addWidget(self.entrada_excel)
        disenio_horizontal_excel.addWidget(self.boton_excel)

        disenio_horizontal_monto = QHBoxLayout()
        disenio_horizontal_monto.addWidget(self.etiqueta_monto)
        disenio_horizontal_monto.addWidget(self.entrada_monto)

        disenio_horizontal_monto.addWidget(self.fecha)
        disenio_horizontal_monto.addWidget(self.date_edit)

        disenio_horizontal_impuestos = QHBoxLayout()

        self.boton_crear_bd.clicked.connect(self.create_database)

        disenio_vertical = QVBoxLayout()
        disenio_vertical.addLayout(disenio_horizontal_excel)
        disenio_vertical.addLayout(disenio_horizontal_monto)
        disenio_vertical.addWidget(self.texto_edit)
        disenio_vertical.addWidget(self.etiqueta_resultado)
        disenio_vertical.addWidget(self.boton_crear_bd)
        disenio_vertical.addWidget(self.button)
        self.setLayout(disenio_vertical)

        self.button.clicked.connect(self.enviar_datos)

    def seleccionar_excel(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Archivos Excel (*.xlsx *.xls)")
        print(ruta_archivo)
        self.ruta_excel = ruta_archivo
        if ruta_archivo:
            self.entrada_excel.setText(ruta_archivo)
            try:
                pd.read_excel(ruta_archivo)
                self.etiqueta_resultado.setText("Archivo Excel cargado correctamente.")
            except Exception as e:
                self.etiqueta_resultado.setText(f"Error al cargar el archivo Excel: {e}")

    def enviar_datos(self):
        if self.ruta_excel:
            try:
                monto = float(self.entrada_monto.text())  # Obtiene el monto y lo convierte a flotante
                
                # Muestra el mensaje de espera
                self.etiqueta_resultado.setText("Espere unos segundos...")

                # Crea un hilo para la operación de fusión
                hilo_fusion = threading.Thread(target=self.procesar_fusion, args=(self.ruta_excel, monto))
                hilo_fusion.start()

            except ValueError:
                self.etiqueta_resultado.setText("Error: Ingresa un monto válido.")
            except FileNotFoundError:
                self.etiqueta_resultado.setText("Error: Archivo no encontrado.")
        else:
            self.etiqueta_resultado.setText("Selecciona un archivo Excel primero.")

    def procesar_fusion(self, ruta_excel, monto):
        # Este método se ejecuta en un hilo separado
        try:
            result = execute_data(ruta_excel, monto)

            # Actualiza la interfaz en el hilo principal
            QMetaObject.invokeMethod(self, "actualizar_resultado", Qt.QueuedConnection, Q_ARG(str, result))
            QMetaObject.invokeMethod(self, "mensaje_exito", Qt.QueuedConnection)
        
        except Exception as e:
            QMetaObject.invokeMethod(self, "mensaje_error", Qt.QueuedConnection, Q_ARG(str, str(e)))

    @pyqtSlot(str)
    def actualizar_resultado(self, result):
        self.texto_edit.setText("")
        self.texto_edit.setText(result)

    @pyqtSlot()
    def mensaje_exito(self):
        self.etiqueta_resultado.setText("Datos procesados correctamente.")

    @pyqtSlot(str)
    def mensaje_error(self, error_message):
        self.etiqueta_resultado.setText(f"Error al procesar los datos: {error_message}")

    def create_database(self):
        if main_database():
            self.etiqueta_resultado.setText("Base de datos creada exitosamente")


class VentanaArchivo(QMainWindow):
    actualizarFinished = pyqtSignal(tuple)  # Señal para comunicar la actualización completada

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Archivo TXT")
        self.ruta_txt = None
        self.initUI()

    def initUI(self):
        self.label_archive = QLabel("Suba archivo TXT para actualizar: ")
        self.textbox = QLineEdit(self)
        self.textbox.setReadOnly(True)  # El textbox no se podrá editar directamente
        self.boton_archivo = QPushButton("Seleccionar Archivo", self)
        self.boton_archivo.clicked.connect(self.seleccionar_archivo)
        self.boton_actualizar = QPushButton("Actualizar", self)
        self.boton_actualizar.clicked.connect(self.actualizar)
        self.etiqueta = QLabel("")
        self.etiqueta.setObjectName("etiqueta_resultado")
        self.texto = QTextEdit(self)
        self.texto.setReadOnly(True)  # Para evitar modificaciones

        layout = QVBoxLayout()
        layout.addWidget(self.label_archive)
        layout.addWidget(self.textbox)
        layout.addWidget(self.texto)
        layout.addWidget(self.etiqueta)
        layout.addWidget(self.boton_archivo)
        layout.addWidget(self.boton_actualizar)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Conectar señal a la función para actualizar GUI
        self.actualizarFinished.connect(self.mostrar_resultado_actualizacion)

    def seleccionar_archivo(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo TXT", "", "Archivos TXT (*.txt)")
        if ruta_archivo:
            self.ruta_txt = ruta_archivo
            self.textbox.setText(ruta_archivo)

    def actualizar(self):
        if self.ruta_txt:
            self.etiqueta.setText("Espere unos segundos...")

            # Crear un hilo para la actualización
            hilo_actualizacion = threading.Thread(target=self.actualizar_base_datos, args=(self.ruta_txt,))
            hilo_actualizacion.start()

        else:
            self.etiqueta.setText("Selecciona un archivo TXT primero")
    
    def actualizar_base_datos(self, ruta):
        try:
            data = update_database(ruta)
            self.actualizarFinished.emit(tuple(data))  # Emitir señal con los datos de resultado
        except Exception as e:
            self.actualizarFinished.emit((False, f"Error en update_database: {e}"))

    @pyqtSlot(tuple)
    def mostrar_resultado_actualizacion(self, data):
        if data[0]:
            self.texto.setText("")
            self.texto.setText(data[1])  # Actualizar la interfaz de usuario con el texto de resultado
            self.etiqueta.setText("Base de datos actualizada")
        else:
            self.texto.setText(data[1])  # Mostrar error en la interfaz de usuario
            self.etiqueta.setText("Error al actualizar la base de datos")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("estilos.qss", "r") as f:  # leer los estilos del archivo
        app.setStyleSheet(f.read())
    ventana = Ventana()
    ventana.setGeometry(1000, 800, 1000, 800)
    ventana.show()
    sys.exit(app.exec_())



