import sys
import json

from PySide6 import QtWidgets

from ui.main_view import MainWindow


with open(r"./src/config/default.json", "r") as file:
    config = json.load(file)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow(config)
window.show()

sys.exit(app.exec())
