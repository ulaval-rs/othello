import geopandas
from PySide2 import QtWidgets, QtCore


class CriteriaMacBethTab(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet('')
        self.setObjectName('tab_criteria_macbeth')

        self.label_data_section = QtWidgets.QLabel(self)
        self.label_data_section.setGeometry(QtCore.QRect(10, 10, 81, 19))
        self.label_data_section.setObjectName('label_data_section')

        self.inline_file_to_add_criteria_filepath = QtWidgets.QLineEdit(self)
        self.inline_file_to_add_criteria_filepath.setGeometry(QtCore.QRect(20, 60, 511, 31))
        self.inline_file_to_add_criteria_filepath.setText('')
        self.inline_file_to_add_criteria_filepath.setObjectName('file_to_add_criteria')

        self.btn_browse_files_to_add = QtWidgets.QPushButton(self)
        self.btn_browse_files_to_add.setGeometry(QtCore.QRect(540, 60, 103, 31))
        self.btn_browse_files_to_add.setObjectName('btn_browse_files_to_add')
        self.btn_browse_files_to_add.clicked.connect(self.browse_files_to_add)

        self.btn_load_file_to_add_data = QtWidgets.QPushButton(self)
        self.btn_load_file_to_add_data.setGeometry(QtCore.QRect(650, 60, 103, 31))
        self.btn_load_file_to_add_data.setObjectName('btn_load_file_to_add_data')
        self.btn_load_file_to_add_data.clicked.connect(self.load_file)

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

        self.set_labels()

    def set_labels(self):
        self.label_data_section.setText('Données')

        self.label_file_to_add_criteria.setText('Sélectionner un fichier')
        self.btn_browse_files_to_add.setText('Parcourir')
        self.btn_load_file_to_add_data.setText('Charger données')

        self.label_field_to_select.setText('Champ à transformer')

        self.label_macbeth_section.setText('MacBeth')
        self.label_macbeth_file_to_select.setText('Sélectionner le fichier M-MACBETH')
        self.btn_load_macbeth_file.setText('Parcourir')

        self.btn_add_column_to_file.setText('Ajouter la colonne')

    def browse_files_to_add(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(self)

        self.inline_file_to_add_criteria_filepath.setText(filename)

    def load_file(self):
        filepath = self.inline_file_to_add_criteria_filepath.text()
        if '.gdb' in filepath.lower():
            df = geopandas.read_file(filepath, driver='FileGDB')

        else:
            df = geopandas.read_file(filepath)

        self.combobox_field_to_select.addItems(df.columns)