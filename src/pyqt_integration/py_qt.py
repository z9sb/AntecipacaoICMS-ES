from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("caminho_do_arquivo.ui", self)  # Carrega o arquivo .ui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
