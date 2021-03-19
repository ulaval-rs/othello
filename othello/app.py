import sys

from PySide2.QtWidgets import QApplication

from othello.ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
