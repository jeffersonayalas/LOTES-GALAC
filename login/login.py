import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Ventana de Login')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label_user = QLabel('Usuario:')
        self.input_user = QLineEdit()
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)

        self.label_pass = QLabel('Contraseña:')
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)  # Ocultar texto de la contraseña
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)

        self.button_login = QPushButton('Iniciar Sesión')
        self.button_login.clicked.connect(self.handle_login)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

    def handle_login(self):
        usuario = self.input_user.text()
        contrasena = self.input_pass.text()

        # Aquí puedes validar las credenciales
        if usuario == 'admin' and contrasena == 'password':  # Ejemplo de credenciales
            QMessageBox.information(self, 'Éxito', '¡Has iniciado sesión correctamente!')
        else:
            QMessageBox.warning(self, 'Error', 'Usuario o contraseña incorrectos.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("estilos.qss", "r") as f:  # leer los estilos del archivo
        app.setStyleSheet(f.read())
    window = LoginWindow()
    window.setGeometry(400, 200, 400, 200)
    window.show()
    sys.exit(app.exec_())
