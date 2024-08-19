from queue import Queue
import sys
from threading import Thread
import time
from tkinter import W
from tkinter.messagebox import NO
from tokenize import Single
import numpy as np

from shared.http_listener import HttpListener

from PySide6.QtCore import (
    Qt,
    QObject,
    QAbstractTableModel,
    QModelIndex,
    QThread,
    Slot,
    Signal,
)
from PySide6.QtGui import QCloseEvent, QFont
from PySide6.QtWidgets import (
    QWidget,
    QTableView,
    QTableWidget,
    QVBoxLayout,
    QApplication,
)


class JsonTableModel(QAbstractTableModel):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self._data = [data] or []

    def rowCount(self, index) -> int:
        return len(self._data) if self._data else 0

    def columnCount(self, index) -> int:
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row = self._data[index.row()]
            keys = list(row.keys())
            return row[keys[index.column()]]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignVCenter + Qt.AlignmentFlag.AlignHCenter

        if role == Qt.ItemDataRole.FontRole:
            return QFont(["Arial"], pointSize=10)

        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Horizontal:
                return list(self._data[0].keys())[section]

        if role == Qt.ItemDataRole.FontRole:
            font = QFont(["Arial"], pointSize=13)
            font.setBold(True)
            return font
        return None

    def insert_new_data(self, row_data: dict):
        position = len(self._data)
        self.beginInsertRows(QModelIndex(), position, position)
        self._data.append(row_data)
        self.endInsertRows()


class DataTableView(QWidget):
    received = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        self.table = QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(10)
        self.layout_main.addWidget(self.table)

        self.listener: HttpListener | None = None

    def init_listener(self, address) -> None:
        self.data_queue: Queue[dict] = Queue()
        self.listener = HttpListener(address, self.data_queue)

        self.listening_thread = Thread(target=self.listener.listening)
        self.listening_thread.start()

        self.received.connect(self._update_view)
        self.is_init = False

        self.update_thread = Thread(target=self._update_data)
        self.update_thread.start()

    def _update_data(self) -> None:
        self.is_running = True
        self.reading = False
        while self.is_running:
            time.sleep(1)
            if self.data_queue.empty() is not True and self.reading is not True:
                self.received.emit()

    def _update_view(self) -> None:
        self.reading = True
        data = self.data_queue.get()
        if self.is_init and data is not None:
            self.data_model.insert_new_data(data)
            self.table.resizeColumnsToContents()
            self.table.scrollToBottom()
        else:
            self.layout_main.removeWidget(self.table)
            self.table.deleteLater()

            self.data_model = JsonTableModel(data)
            self.table = QTableView()
            self.table.setModel(self.data_model)
            self.layout_main.addWidget(self.table)
            self.is_init = True

        self.reading = False

    def stop(self) -> None:
        if self.listener is not None:
            self.listener.stop()
            self.is_running = False
            self.data_queue.put(None)
            self.listening_thread.join()
            self.update_thread.join()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    test = {"age": 10, "name": "nihao"}

    window = DataTableView(test)
    window.show()

    window.data_model.insert_new_data(test)

    sys.exit(app.exec())
