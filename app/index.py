import sys
import threading
from database.inter_database import update_database, update_drafts
from app.api_odoo import api_data
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QPushButton, QVBoxLayout, QHBoxLayout, 
                             QMainWindow, QTextEdit, 
                             QGridLayout, QDateEdit, 
                             QListWidget, QListWidgetItem)

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FACTURACION POR LOTES - ODOO/GALAC")
        
        # Inicializar atributos para controlar los hilos
        self.cancelar_hilos = False

        # Crear el campo de fecha
        self.fecha = QLabel("Seleccione una fecha:")
        self.date_edit = QDateEdit(self)
        self.date_edit.setDate(QDate.currentDate())  # Establecer la fecha actual como valor por defecto
        self.date_edit.setDisplayFormat("yyyy-MM-dd")  # Formato de visualización

        # Crear un layout horizontal para la fecha
        layout_fecha = QHBoxLayout()
        layout_fecha.addWidget(self.fecha)
        layout_fecha.addWidget(self.date_edit)

        # Layout de grilla principal
        layoutPrincipal = QGridLayout()
        layoutPrincipal.addLayout(layout_fecha, 0, 0, 1, 2)

        self.ventana1 = VentanaPrincipal(self.date_edit.date())
        layoutPrincipal.addWidget(self.ventana1, 1, 1)

        self.ventana2 = VentanaArchivo(self.date_edit.date())
        layoutPrincipal.addWidget(self.ventana2, 1, 0)

        layoutPrincipal.setRowStretch(1, 1)  # Asegura que la fila con las ventanas sea flexible
        layoutPrincipal.setColumnStretch(1, 1)  # Asegura que la columna con las ventanas sea flexible

        widgetCentral = QWidget()
        widgetCentral.setLayout(layoutPrincipal)

        widgetCentral.setStyleSheet("border: 0.5px solid rgb(0, 165, 248); padding: 10px; border-radius: 5px")

        # Establecer el widget central en la ventana principal
        self.setCentralWidget(widgetCentral)

    def closeEvent(self, event):
        self.cancelar_hilos = True
        event.accept()  # Aceptar el evento de cierre de ventana

class VentanaPrincipal(QWidget):
    contenido_archivo_obtenido = pyqtSignal(str)

    def __init__(self, fecha):
        super().__init__()
        self.setWindowTitle("FACTURACION POR LOTES - GALAC/ODOO")
        self.fecha_data = fecha

        self.etiqueta_resultado = QLabel("")
        self.button_fusionar = QPushButton("FUSIONAR", self)

        # Crear el QListWidget para el checklist
        self.checklist = QListWidget()
        items = ['Clientes en Bolivares', 'Clientes en Divisas']
        for item in items:
            list_item = QListWidgetItem(item)
            list_item.setFlags(list_item.flags() | Qt.ItemIsUserCheckable)  # Hacer el item chequeable
            list_item.setCheckState(Qt.Unchecked)  # Estado inicial: desmarcado
            self.checklist.addItem(list_item)

        self.texto_edit = QTextEdit(self)
        self.texto_edit.setReadOnly(True)  # Para evitar modificaciones

        # Layouts
        disenio_vertical = QVBoxLayout()
        disenio_vertical.addWidget(self.checklist)
        disenio_vertical.addWidget(self.texto_edit)
        disenio_vertical.addWidget(self.etiqueta_resultado)
        disenio_vertical.addWidget(self.button_fusionar)

        self.setLayout(disenio_vertical)

        # Conectar señales y slots
        self.contenido_archivo_obtenido.connect(self.mostrar_contenido_archivo)
        self.button_fusionar.clicked.connect(self.enviar_datos)  # Ahora solo enviar_datos


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
            self.etiqueta_resultado.setText("Espere unos segundos...")
            tipos_clientes = self.obtener_tipos_clientes()
            if not tipos_clientes:
                self.etiqueta_resultado.setText("Selecciona al menos un tipo de cliente.")
                return
            
            self.parent().cancelar_hilos = False  # Inicializa la bandera de cancelación

            # Crea un hilo para la operación
            hilo_fusion = threading.Thread(target=self.ejecutar_api_data, args=(tipos_clientes,))
            hilo_fusion.start()

        except ValueError:
            self.etiqueta_resultado.setText("Error: Ingresa un monto válido.")
        except FileNotFoundError:
            self.etiqueta_resultado.setText("Error: Archivo no encontrado.")

    def ejecutar_api_data(self, tipos_clientes):
        main_window = QApplication.activeWindow()
        if not main_window.cancelar_hilos:
            fecha_seleccionada = main_window.date_edit.date().toString("yyyy-MM-dd")
            try:
                archivo_resultado = api_data(1, fecha_seleccionada, tipos_clientes)
                self.leer_contenido_archivo(archivo_resultado)
            except Exception as e:
                print(f"Error en api_data: {str(e)}")

    def leer_contenido_archivo(self, archivo):
        try:
            with open(archivo, 'r') as f:  # Asegurarse de manejar el archivo correctamente
                contenido = f.read()
                self.contenido_archivo_obtenido.emit(contenido)
        except Exception as e:
            self.etiqueta_resultado.setText(f"Error al leer el archivo: {str(e)}")

    @pyqtSlot(str)
    def mostrar_contenido_archivo(self, contenido):
        self.texto_edit.setPlainText(contenido)
        self.etiqueta_resultado.setText("Contenido cargado correctamente.")

class VentanaArchivo(QWidget):
    actualizarFinished = pyqtSignal(tuple)

    def __init__(self, fecha, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Archivo TXT")
        self.fecha_data = fecha
        self.initUI()

    def initUI(self):
        self.boton_archivo = QPushButton("VERIFICAR CLIENTES", self)
        self.boton_archivo.clicked.connect(self.enviar_datos)
        self.etiqueta = QLabel("")
        self.texto = QTextEdit(self)
        self.texto.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.texto)
        layout.addWidget(self.etiqueta)
        layout.addWidget(self.boton_archivo)
        self.setLayout(layout)

        self.actualizarFinished.connect(self.mostrar_resultado_actualizacion)

    def enviar_datos(self):
        try:
            self.etiqueta.setText("Espere unos segundos...")
            main_window = QApplication.activeWindow()
            main_window.cancelar_hilos = False  # Inicializa la bandera de cancelación
            hilo_actualizacion = threading.Thread(target=self.ejecutar_api_data)
            hilo_actualizacion.start()
        except Exception as e:
            self.etiqueta.setText(f"Error: {str(e)}")

    def ejecutar_api_data(self):
        main_window = QApplication.activeWindow()
        if not main_window.cancelar_hilos:
            fecha_seleccionada = main_window.date_edit.date().toString("yyyy-MM-dd")
            try:
                archivo_resultado = api_data(0, fecha_seleccionada)
                self.leer_contenido_archivo(archivo_resultado)
            except Exception as e:
                print(f"Error en api_data en VentanaArchivo: {str(e)}")

    def leer_contenido_archivo(self, archivo):
        try:
            with open(archivo, 'r') as f:
                contenido = f.read()
                self.actualizarFinished.emit((True, contenido))
        except Exception as e:
            self.actualizarFinished.emit((False, f"Error al leer el archivo: {str(e)}"))

    @pyqtSlot(tuple)
    def mostrar_resultado_actualizacion(self, data):
        if data[0]:
            self.texto.setPlainText(data[1])
            self.etiqueta.setText("Base de datos actualizada")
        else:
            self.texto.setPlainText("")
            self.etiqueta.setText(data[1])  # Mostrar error en la interfaz de usuario

if __name__ == "__main__":
    import os
    os.environ['QT_QPA_PLATFORM'] = 'xcb'  # Cambiar a 'xcb' si hay problemas con Wayland

    app = QApplication(sys.argv)
    with open("app/styles/estilos.qss", "r") as f:
        app.setStyleSheet(f.read())
    ventana = Ventana()
    ventana.setGeometry(1000, 800, 1000, 800)
    ventana.show()
    sys.exit(app.exec_())
