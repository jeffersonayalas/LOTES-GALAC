import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                             QFileDialog, QLineEdit, QHBoxLayout)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from app.main import execute_data
import pandas as pd


class VentanaPrincipal(QWidget):

    def __init__(self):
        super().__init__()
        self.ruta_excel = None
        self.setWindowTitle("FACTURACION POR LOTES - GALAC/ODOO")

        # ... (código para self.etiqueta_excel, self.entrada_excel, self.boton_excel, self.etiqueta_resultado) ...
        self.etiqueta_excel = QLabel("Archivo Excel:")
        self.entrada_excel = QLineEdit()
        self.boton_excel = QPushButton("Seleccionar")
        self.boton_excel.clicked.connect(self.seleccionar_excel)
       
        self.etiqueta_resultado = QLabel("")

        # Nuevo campo de texto para el monto
        self.etiqueta_monto = QLabel("Monto del Banco:")
        self.entrada_monto = QLineEdit()

        disenio_horizontal_excel = QHBoxLayout()
        disenio_horizontal_excel.addWidget(self.etiqueta_excel)
        disenio_horizontal_excel.addWidget(self.entrada_excel)
        disenio_horizontal_excel.addWidget(self.boton_excel)


        disenio_horizontal_monto = QHBoxLayout() # Layout para el campo de monto
        disenio_horizontal_monto.addWidget(self.etiqueta_monto)
        disenio_horizontal_monto.addWidget(self.entrada_monto)

        disenio_vertical = QVBoxLayout()
        disenio_vertical.addLayout(disenio_horizontal_excel)
        disenio_vertical.addLayout(disenio_horizontal_monto) # Agrega el layout del monto
        disenio_vertical.addWidget(self.etiqueta_resultado)
        self.setLayout(disenio_vertical)

        button = QPushButton("FUSIONAR", self)
        disenio_vertical.addWidget(button)
        button.clicked.connect(self.enviar_datos)


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

    
if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.setGeometry(500, 500, 500, 500)
    ventana.show()
    sys.exit(aplicacion.exec_())



