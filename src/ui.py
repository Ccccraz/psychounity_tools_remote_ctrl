import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("psychounity remote")
        self.widget_main = QWidget()
        self.layout_main = QVBoxLayout()

        self.lable_correct_rate = QLabel("Correct Rate: ")
        self.lable_correct_rate_display = QLabel()
        self.layout_correct_rate = QHBoxLayout()
        self.layout_correct_rate.addWidget(self.lable_correct_rate)
        self.layout_correct_rate.addWidget(self.lable_correct_rate_display)

        self.lable_rtsp_address = QLabel("Streaming Address: ")
        self.lineedit_rtsp_address = QLineEdit()
        self.push_button_rtsp_address = QPushButton("Confirm")
        self.layout_rtsp_address = QHBoxLayout()
        self.layout_rtsp_address.addWidget(self.lable_rtsp_address)
        self.layout_rtsp_address.addWidget(self.lineedit_rtsp_address)
        self.layout_rtsp_address.addWidget(self.push_button_rtsp_address)

        self.layout_main.addLayout(self.layout_correct_rate)
        self.layout_main.addLayout(self.layout_rtsp_address)


        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.widget_main)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())