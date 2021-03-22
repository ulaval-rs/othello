from PySide2 import QtWidgets, QtCore
from fiona.errors import DriverError

from othello import gis
from othello.ui.popup import Popup


class CriteriaTab(QtWidgets.QWidget):

    def __init__(self):
        self.df = None

        super().__init__()

        self.setStyleSheet('')
        self.setObjectName('tab_criteria_macbeth')

        self.label_data_section = QtWidgets.QLabel(self)
        self.label_data_section.setGeometry(QtCore.QRect(10, 10, 81, 19))
        self.label_data_section.setObjectName('label_data_section')

        self.inline_file_to_add_criteria_filepath = QtWidgets.QLineEdit(self)
        self.inline_file_to_add_criteria_filepath.setGeometry(QtCore.QRect(20, 60, 621, 31))
        self.inline_file_to_add_criteria_filepath.setText('')
        self.inline_file_to_add_criteria_filepath.setObjectName('file_to_add_criteria')

        self.btn_browse_files_to_add = QtWidgets.QPushButton(self)
        self.btn_browse_files_to_add.setGeometry(QtCore.QRect(650, 60, 103, 31))
        self.btn_browse_files_to_add.setObjectName('btn_browse_files_to_add')
        self.btn_browse_files_to_add.clicked.connect(self.browse_files_to_add)

        self.label_file_to_add_criteria = QtWidgets.QLabel(self)
        self.label_file_to_add_criteria.setGeometry(QtCore.QRect(20, 40, 311, 19))
        self.label_file_to_add_criteria.setObjectName('label_file_to_add_criteria')

        self.combobox_field_to_select = QtWidgets.QComboBox(self)
        self.combobox_field_to_select.setGeometry(QtCore.QRect(20, 120, 731, 31))
        self.combobox_field_to_select.setObjectName('combobox_field_to_select')

        self.label_field_to_select = QtWidgets.QLabel(self)
        self.label_field_to_select.setGeometry(QtCore.QRect(20, 100, 311, 19))
        self.label_field_to_select.setObjectName('label_field_to_select')

        self.label_macbeth_section = QtWidgets.QLabel(self)
        self.label_macbeth_section.setGeometry(QtCore.QRect(10, 170, 81, 19))
        self.label_macbeth_section.setObjectName('label_macbeth_section')

        self.label_macbeth_file_to_select = QtWidgets.QLabel(self)
        self.label_macbeth_file_to_select.setGeometry(QtCore.QRect(20, 200, 311, 19))
        self.label_macbeth_file_to_select.setObjectName('label_macbeth_file_to_select')

        self.inline_macbeth_filepath = QtWidgets.QLineEdit(self)
        self.inline_macbeth_filepath.setGeometry(QtCore.QRect(20, 220, 621, 31))
        self.inline_macbeth_filepath.setText('')
        self.inline_macbeth_filepath.setObjectName('inline_macbeth_filepath')

        self.btn_load_macbeth_file = QtWidgets.QPushButton(self)
        self.btn_load_macbeth_file.setGeometry(QtCore.QRect(650, 220, 103, 31))
        self.btn_load_macbeth_file.setObjectName('btn_load_macbeth_file')

        self.btn_add_column_to_file = QtWidgets.QPushButton(self)
        self.btn_add_column_to_file.setGeometry(QtCore.QRect(610, 500, 151, 31))
        self.btn_add_column_to_file.setObjectName('btn_add_column_to_file')
        self.btn_add_column_to_file.clicked.connect(self.write_file)

        self.set_labels()

    def set_labels(self):
        self.label_data_section.setText('Données')

        self.label_file_to_add_criteria.setText('Sélectionner un fichier')
        self.btn_browse_files_to_add.setText('Parcourir')

        self.label_field_to_select.setText('Champ à transformer')

        self.label_macbeth_section.setText('MacBeth')
        self.label_macbeth_file_to_select.setText('Sélectionner le fichier M-MACBETH')
        self.btn_load_macbeth_file.setText('Parcourir')

        self.btn_add_column_to_file.setText('Ajouter la colonne')

    def browse_files_to_add(self):
        filepath = QtWidgets.QFileDialog.getExistingDirectory(self)

        try:
            self.df = gis.io.read(filepath)
            self.inline_file_to_add_criteria_filepath.setText(filepath)
            self.combobox_field_to_select.addItems(self.df.columns)
        except DriverError as e:
            popup = Popup(f"Erreur de lecture du fichier : {e}"*80, self)
            popup.show()

    def write_file(self):
        if self.df is None:
            popup = Popup("Aucune donnée n'a été chargée", self)
            popup.show()

        else:
            filename = QtWidgets.QFileDialog.getSaveFileName(self)
            gis.io.write(self.df, filename[0])

