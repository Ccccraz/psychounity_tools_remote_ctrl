from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        self.lable_correct_rate = QLabel("Correct Rate: ")
        self.lable_correct_rate_display = QLabel()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.lable_correct_rate)
        self.layout.addWidget(self.lable_correct_rate_display)