import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit, QMainWindow, QAction, QMenu)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main import execute_data  # Asegúrate de que 'main.py' existe y tiene la función execute_data
import pandas as pd
from operate_database import main_database, update_database


class VentanaArchivo(QMainWindow):  # Nueva ventana para seleccionar archivo TXT
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Archivo TXT")
        self.ruta_txt = None
        self.initUI()

    def initUI(self):
        self.textbox = QLineEdit(self)
        self.textbox.setReadOnly(True)  # El textbox no se podrá editar directamente
        self.boton_archivo = QPushButton("Seleccionar Archivo", self)
        self.boton_archivo.clicked.connect(self.seleccionar_archivo)
        self.boton_actualizar = QPushButton("Actualizar", self)
        self.boton_actualizar.clicked.connect(self.actualizar)
        self.etiqueta_resultado = QLabel("")
        self.etiqueta_resultado.setObjectName("etiqueta_resultado") 

        layout = QVBoxLayout()
        layout.addWidget(self.textbox)
        layout.addWidget(self.etiqueta_resultado)
        layout.addWidget(self.boton_archivo)
        layout.addWidget(self.boton_actualizar)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def seleccionar_archivo(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo TXT", "", "Archivos TXT (*.txt)")
        if ruta_archivo:
            self.ruta_txt = ruta_archivo
            self.textbox.setText(ruta_archivo)
        

    def actualizar(self):
        if self.ruta_txt:
            # Aquí realizarías la actualización usando self.ruta_txt
            # ... tu lógica de actualización con el archivo TXT ...
            print(f"Archivo TXT seleccionado: {self.ruta_txt}")
            #Primero se hace drop de todos los datos de la tabla
            #Leer txt
            if update_database(self.ruta_txt): self.etiqueta_resultado.setText("Base de Datos Actualizada")
            #self.close() # Cierra la ventana después de actualizar
        else:
            print("Selecciona un archivo TXT primero")


class VentanaBD(QMainWindow):  # Nueva ventana para seleccionar archivo TXT
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Base de datos")
        self.nombre_bd = None
        self.initUI()

    def initUI(self):
        self.textbox = QLineEdit(self)
        self.textbox.setReadOnly(False)  # El textbox no se podrá editar directamente
        #self.boton_archivo = QPushButton("Seleccionar Archivo", self)
        #self.boton_archivo.clicked.connect(self.seleccionar_archivo)
        self.boton_crear = QPushButton("Crear", self) #Crear base de datos
        self.boton_crear.clicked.connect(self.crear_bd)

        layout = QVBoxLayout()
        layout.addWidget(self.textbox)
        layout.addWidget(self.boton_crear)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def crear_bd(self):
        self.nombre_bd = self.textbox.text()
        if self.nombre_bd:
            # Aquí realizarías la actualización usando self.ruta_txt
            # ... tu lógica de actualización con el archivo TXT ...
            if main_database():
                self.etiqueta_resultado.setText("Base de datos creada correctamente.")
            self.close() # Cierra la ventana después de actualizar
        else:
            print("Selecciona un archivo TXT primero")


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_excel = None
        self.setWindowTitle("FACTURACION POR LOTES - GALAC/ODOO")
        # ... (código para self.etiqueta_excel, self.entrada_excel, self.boton_excel, self.etiqueta_resultado) ...
        self.button = QPushButton("FUSIONAR", self)
        self.etiqueta_resultado = QLabel("")
        self.etiqueta_resultado.setObjectName("etiqueta_resultado") # asigna el ID para el QLabel resultado

        self.etiqueta_excel = QLabel("Archivo Excel:")
        self.entrada_excel = QLineEdit()
        self.boton_excel = QPushButton("Seleccionar")
        #self.button = QPushButton("FUSIONAR", self)
        self.boton_archivo_txt = QPushButton("Actualizar Base de Datos", self) # Nuevo boton
        self.boton_crear_bd = QPushButton("Crear Base de datos", self)

        #Accion de boton <<seleccionar excel>>
        self.boton_excel.clicked.connect(self.seleccionar_excel)

        #self.etiqueta_resultado = QLabel("")
        
        # ... (código para self.etiqueta_monto, self.entrada_monto) ...
        self.etiqueta_monto = QLabel("Tasa del Banco (BCV):")
        self.entrada_monto = QLineEdit()

        disenio_horizontal_excel = QHBoxLayout()
        disenio_horizontal_excel.addWidget(self.etiqueta_excel)
        disenio_horizontal_excel.addWidget(self.entrada_excel)
        disenio_horizontal_excel.addWidget(self.boton_excel)

        disenio_horizontal_monto = QHBoxLayout() # Layout para el campo de monto
        disenio_horizontal_monto.addWidget(self.etiqueta_monto)
        disenio_horizontal_monto.addWidget(self.entrada_monto)
        

        #self.boton_crear_bd.clicked.connect(self.crear_base_datos) <<crear base de datos>>
        self.boton_archivo_txt.clicked.connect(self.abrir_ventana_archivo) # Conecta al nuevo metodo
        self.boton_crear_bd.clicked.connect(main_database)

        disenio_vertical = QVBoxLayout()
        disenio_vertical.addLayout(disenio_horizontal_excel)
        disenio_vertical.addLayout(disenio_horizontal_monto)
        disenio_vertical.addWidget(self.etiqueta_resultado)
        disenio_vertical.addWidget(self.boton_archivo_txt) # Agrega el nuevo boton
        disenio_vertical.addWidget(self.boton_crear_bd) #Crear base de datos
        disenio_vertical.addWidget(self.button) #Fusionar
        self.setLayout(disenio_vertical) 

        self.button.clicked.connect(self.enviar_datos)
        

    def abrir_ventana_archivo(self):
        self.ventana_archivo = VentanaArchivo(self)
        self.ventana_archivo.setGeometry(300, 100, 300, 100)
        self.ventana_archivo.show()

    """ 
    def abrir_ventana_crear(self):
        self.ventana_bd = VentanaBD(self)
        self.ventana_bd.setGeometry(300, 100, 300, 100)
        self.ventana_bd.show()
    """


    # ... resto del código (seleccionar_excel, enviar_datos) ...
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
                monto = float(self.entrada_monto.text()) # Obtiene el monto y lo convierte a flotante
                execute_data(self.ruta_excel, monto) # Pasa el DataFrame y el monto a execute_data
                self.etiqueta_resultado.setText("Datos procesados correctamente.")
            except ValueError:
                self.etiqueta_resultado.setText("Error: Ingresa un monto válido.")
            except FileNotFoundError:
                self.etiqueta_resultado.setText("Error: Archivo no encontrado.")
            """ 
            except Exception as e:
                self.etiqueta_resultado.setText(f"Error al procesar los datos: {e}")
            """
        else:
            self.etiqueta_resultado.setText("Selecciona un archivo Excel primero.")

    """ 
    def configurar(self):
        self.estilos = 
            QWidget {
                background-color: #f0f0f0; /* Fondo suave */
                font-family: Arial, sans-serif; /* Fuente legible */
            }

            QLabel {
                font-weight: bold; /* Etiquetas en negrita */
                color: #333; /* Texto oscuro */
            }

            QLineEdit {
                border: 1px solid #ccc; /* Borde sutil */
                border-radius: 5px; /* Esquinas redondeadas */
                padding: 5px;
            }

            QPushButton {
                background-color: #4CAF50; /* Verde claro */
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 100px; /* Ancho mínimo para los botones */
            }

            QPushButton:hover {
                background-color: #45a049; /* Verde más oscuro al pasar el ratón */
            }

            QPushButton#fusionar { /* Estilos específicos para el botón "FUSIONAR" */
                 background-color: #2196F3; /* Azul */
            }
            QPushButton#fusionar:hover {
                background-color: #1976D2; /* Azul más oscuro al pasar el ratón */
            }

            #etiqueta_resultado { /* Estilos para el QLabel de resultado */
                color: #FF9800; /* Naranja, para destacar resultados */
                font-size: 14px;
                margin-top: 10px;
            }

        
        return self.estilos
        """



if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    with open("estilos.qss", "r") as f: # leer los estilos del archivo
          aplicacion.setStyleSheet(f.read())
    ventana = VentanaPrincipal()
    ventana.setGeometry(500, 500, 500, 500)
    ventana.show()
    sys.exit(aplicacion.exec_())

