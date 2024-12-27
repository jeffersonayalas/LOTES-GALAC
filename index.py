import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
                             QFileDialog, QLineEdit, QHBoxLayout)



import pandas as pd


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carga de Archivos")

        self.etiqueta_excel = QLabel("Archivo Excel:")
        self.entrada_excel = QLineEdit()
        self.boton_excel = QPushButton("Seleccionar")
        self.boton_excel.clicked.connect(self.seleccionar_excel)

        self.etiqueta_txt = QLabel("Archivo TXT:")
        self.entrada_txt = QLineEdit()
        self.boton_txt = QPushButton("Seleccionar")
        self.boton_txt.clicked.connect(self.seleccionar_txt)

        self.etiqueta_resultado = QLabel("")  # Para mostrar mensajes

        # Distribución de elementos en la interfaz
        disenio_horizontal_excel = QHBoxLayout()
        disenio_horizontal_excel.addWidget(self.etiqueta_excel)
        disenio_horizontal_excel.addWidget(self.entrada_excel)
        disenio_horizontal_excel.addWidget(self.boton_excel)

        disenio_horizontal_txt = QHBoxLayout()
        disenio_horizontal_txt.addWidget(self.etiqueta_txt)
        disenio_horizontal_txt.addWidget(self.entrada_txt)
        disenio_horizontal_txt.addWidget(self.boton_txt)

        disenio_vertical = QVBoxLayout()
        disenio_vertical.addLayout(disenio_horizontal_excel)
        disenio_vertical.addLayout(disenio_horizontal_txt)
        disenio_vertical.addWidget(self.etiqueta_resultado)
        self.setLayout(disenio_vertical)


    def seleccionar_excel(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "", "Archivos Excel (*.xlsx *.xls)")
        if ruta_archivo:
            self.entrada_excel.setText(ruta_archivo)
            try:
                pd.read_excel(ruta_archivo) #solo para verificar que el archivo se pueda leer
                self.etiqueta_resultado.setText("Archivo Excel cargado correctamente.")
            except Exception as e:
                self.etiqueta_resultado.setText(f"Error al cargar el archivo Excel: {e}")

    def seleccionar_txt(self):
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo TXT", "", "Archivos TXT (*.txt)")
        if ruta_archivo:
            self.entrada_txt.setText(ruta_archivo)
            self.etiqueta_resultado.setText("Archivo TXT cargado correctamente.")



if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(aplicacion.exec_())
