import sys
from threading import Thread
import threading
import vlc

from listener import Listener

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
    QSizePolicy,
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
        self.setWindowTitle("psychounity remote controller")

        self.widget_main = QWidget()
        self.layout_main = QVBoxLayout()
        self.layout_controller = QHBoxLayout()

        self._init_player()
        self._init_infomation_group()
        self._init_rtsp_controller()

        self.layout_controller.addWidget(self.group_infomation)
        self.layout_controller.addWidget(self.group_rtsp_controller)

        self.layout_main.addWidget(self.group_vlc_frame)
        self.layout_main.addLayout(self.layout_controller)

        self.widget_main.setLayout(self.layout_main)
        self.setCentralWidget(self.widget_main)

    def _init_player(self):
        self.vlc_instance: vlc.Instance = vlc.Instance()
        self.vlc_player: vlc.MediaPlayer = self.vlc_instance.media_player_new()
        self.vlc_media: vlc.Media | None = None
        self.vlc_player.set_media(self.vlc_media)

        self.group_vlc_frame = QGroupBox("Monitor")
        self.layout_vlc_frame = QVBoxLayout()

        self.vlc_frame = QFrame()
        self.vlc_frame.setMinimumSize(640, 480)
        self.layout_vlc_frame.addWidget(self.vlc_frame)
        self.vlc_player.set_hwnd(self.vlc_frame.winId())

        self.layout_vlc_controller = QHBoxLayout()

        self.pushbutton_vlc_play = QPushButton("Play")
        self.layout_vlc_controller.addWidget(self.pushbutton_vlc_play)

        self.pushbutton_vlc_stop = QPushButton("Stop")
        self.layout_vlc_controller.addWidget(self.pushbutton_vlc_stop)

        self.pushbutton_vlc_record = QPushButton("Record")
        self.layout_vlc_controller.addWidget(self.pushbutton_vlc_record)

        self.layout_vlc_frame.addLayout(self.layout_vlc_controller)

        self.group_vlc_frame.setLayout(self.layout_vlc_frame)

    def _play_video(self):
        rtsp_address: str = self.lineedit_rtsp_address.text()
        self.media = self.vlc_instance.media_new(rtsp_address)
        self.vlc_player.set_media(self.media)
        self.vlc_player.play()

    def _stop_video(self) -> None:
        pass

    def _record_video(self) -> None:
        pass

    def _init_infomation_group(self) -> None:
        self.group_infomation = QGroupBox("Infomation")
        self.group_infomation.setMaximumHeight(200)
        self.layout_infomation = QVBoxLayout()

        self.label_game_server_address = QLabel("Server : ")
        self.lineedit_game_server_address = QLineEdit()
        self.layout_game_server_address = QHBoxLayout()
        self.layout_game_server_address.addWidget(self.label_game_server_address)
        self.layout_game_server_address.addWidget(self.lineedit_game_server_address)

        self.label_game_server_port = QLabel("Port : ")
        self.lineedit_game_server_port = QLineEdit()
        self.layout_game_server_port = QHBoxLayout()
        self.layout_game_server_port.addWidget(self.label_game_server_port)
        self.layout_game_server_port.addWidget(self.lineedit_game_server_port)

        self.pushbutton_game_server_link = QPushButton("link")
        self.pushbutton_game_server_link.clicked.connect(self._link_infomation)
        self.pushbutton_game_server_close = QPushButton("close")
        self.pushbutton_game_server_close.clicked.connect(self._close_link)
        self.layout_game_server_ctrl = QHBoxLayout()
        self.layout_game_server_ctrl.addWidget(self.pushbutton_game_server_close)
        self.layout_game_server_ctrl.addWidget(self.pushbutton_game_server_link)

        self.layout_game_server = QVBoxLayout()
        self.layout_game_server.addLayout(self.layout_game_server_address)
        self.layout_game_server.addLayout(self.layout_game_server_port)
        self.layout_game_server.addLayout(self.layout_game_server_ctrl)

        self.layout_infomation.addLayout(self.layout_game_server)

        self.label_trial_count = QLabel("Trial number : ")
        self.lineedit_trial_count = QLineEdit()
        self.lineedit_trial_count.setReadOnly(True)
        self.layout_trial_count = QHBoxLayout()
        self.layout_trial_count.addWidget(self.label_trial_count)
        self.layout_trial_count.addWidget(self.lineedit_trial_count)

        self.layout_infomation.addLayout(self.layout_trial_count)

        self.label_correct_count = QLabel("Correct number : ")
        self.lineedit_correct_count = QLineEdit()
        self.lineedit_correct_count.setReadOnly(True)
        self.layout_correct_count = QHBoxLayout()
        self.layout_correct_count.addWidget(self.label_correct_count)
        self.layout_correct_count.addWidget(self.lineedit_correct_count)

        self.layout_infomation.addLayout(self.layout_correct_count)

        self.label_correct_rate = QLabel("Current correct rate : ")
        self.lineedit_correct_rate = QLineEdit()
        self.lineedit_correct_rate.setReadOnly(True)
        self.layout_correct_rate = QHBoxLayout()
        self.layout_correct_rate.addWidget(self.label_correct_rate)
        self.layout_correct_rate.addWidget(self.lineedit_correct_rate)

        self.layout_infomation.addLayout(self.layout_correct_rate)

        self.group_infomation.setLayout(self.layout_infomation)

    def _init_rtsp_controller(self):
        self.group_rtsp_controller = QGroupBox("Rtsp")
        self.group_rtsp_controller.setMaximumHeight(120)
        self.layout_rtsp_controller = QVBoxLayout()

        self.label_rtsp_address = QLabel("RTSP address : ")
        self.lineedit_rtsp_address = QLineEdit()
        self.pushbutton_rtsp_address = QPushButton("Link")
        self.layout_rtsp_address = QHBoxLayout()
        self.layout_rtsp_address.addWidget(self.label_rtsp_address)
        self.layout_rtsp_address.addWidget(self.lineedit_rtsp_address)
        self.layout_rtsp_address.addWidget(self.pushbutton_rtsp_address)

        self.layout_rtsp_controller.addLayout(self.layout_rtsp_address)

        self.group_rtsp_controller.setLayout(self.layout_rtsp_controller)

    def _link_infomation(self):
        self._info_client = Listener(
            self.lineedit_game_server_address.text(),
            int(self.lineedit_game_server_port.text()),
        )
        self._info_thread = threading.Thread(
            target=self._info_client.start, args=(self._update_info,)
        )
        self._info_thread.start()

    def _close_link(self):
        self._info_client.close()
        self._info_thread.join(1)
        print("closed")

    def _update_info(self, trial_count, trial_count_true, correct_rate):
        self.lineedit_trial_count.setText(str(trial_count))
        self.lineedit_correct_count.setText(str(trial_count_true))
        self.lineedit_correct_rate.setText(str(correct_rate))

    def __del__(self):
        self._info_thread.join(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
