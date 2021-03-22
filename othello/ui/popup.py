from PySide2 import QtCore
from PySide2.QtWidgets import QDialog, QLabel, QPushButton


class Popup(QDialog):

    def __init__(self, message, parent=None):
        super().__init__(parent)
        width = 400
        height = 260
        self.setGeometry(400, 300, width, height)

        self.label = QLabel(message, self)
        self.label.setGeometry(QtCore.QRect(20, 20, width-20, 30))

        self.btn_ok = QPushButton('Ok', self)
        self.btn_ok.setGeometry(QtCore.QRect(width-80, height-50, 60, 30))
        self.btn_ok.clicked.connect(lambda: self.done(0))
