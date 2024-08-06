import sys
from networkx import selfloop_edges
import vlc

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QFrame,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QLineEdit,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.instance: vlc.Instance = vlc.Instance()
        self.media: vlc.Media = self.instance.media_new("../assets/test_anuimal.mp4")
        self.mediaplayer: vlc.MediaPlayer = self.instance.media_player_new()
        self.mediaplayer.set_media(self.media)

        self._init_ui()

    def _init_ui(self) -> None:
        """Init UI layout"""
        self.setWindowTitle("psychounity remote")

        self.widget_main = QWidget()
        self.layout_main = QVBoxLayout()

        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.widget_main)

    def _init_infomation_group(self) -> None:
        self.group_infomation = QGroupBox("Infomation")
        self.layout_infomation = QVBoxLayout()

        self.label_trial_count = QLabel("Trial number")
        self.lineedit_trial_count = QLineEdit()
        self.layout_trial_count = QVBoxLayout()
        self.layout_trial_count.addWidget(self.label_trial_count)
        self.layout_trial_count.addWidget(self.lineedit_trial_count)

        self.layout_infomation.addLayout(self.layout_trial_count)

        self.label_correct_count = QLabel("Correct number")
        self.lineedit_correct_count = QLineEdit()
        self.layout_correct_count = QVBoxLayout()
        self.layout_correct_count.addWidget(self.label_correct_count)
        self.layout_correct_count.addWidget(self.lineedit_correct_count)

        self.layout_infomation.addLayout(self.layout_correct_count)

        self.label_correct_rate = QLabel("Current correct rate: ")
        self.lineedit_correct_rate = QLineEdit()
        self.layout_correct_rate = QHBoxLayout()
        self.layout_correct_rate.addWidget(self.label_correct_rate)
        self.layout_correct_rate.addWidget(self.lineedit_correct_rate)

        self.layout_infomation.addLayout(self.layout_correct_rate)

        self.group_infomation.setLayout(self.layout_infomation)

    def _init_rtsp_controller(self):
        self.group_rtsp_controller = QGroupBox()
        self.layout_rtsp_controller = QVBoxLayout()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
