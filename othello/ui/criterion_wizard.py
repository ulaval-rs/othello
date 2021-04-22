import configparser
import copy
from typing import Optional

import fiona
import geopandas
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QDialog, QTableWidgetItem
from fiona.errors import DriverError

from othello import gis
from othello.macbeth.errors import MacbethParserError
from othello.macbeth.parser import MacbethParser
from othello.ui.popup import Popup


class CriterionWizard(QDialog):

    def __init__(self, parent, choose_macbeth_file: bool):
        self.geo_filepath: Optional[str] = None
        self.df: Optional[geopandas.GeoDataFrame] = None

        super().__init__(parent)

        self.resize(800, 400)

        self.inline_geofile = QtWidgets.QLineEdit(self, text='')
        self.inline_geofile.setGeometry(QtCore.QRect(20, 60, 621, 31))

        self.btn_browse_geo_file = QtWidgets.QPushButton(self, text='Browse', clicked=self.browse_geo_file)
        self.btn_browse_geo_file.setGeometry(QtCore.QRect(650, 60, 103, 31))

        self.label_select_geofile = QtWidgets.QLabel(self, text='Select a file')
        self.label_select_geofile.setGeometry(QtCore.QRect(20, 40, 311, 19))

        self.label_layer_to_select = QtWidgets.QLabel(self, text='Layer to transform')
        self.label_layer_to_select.setGeometry(QtCore.QRect(20, 100, 311, 19))
        self.combobox_layer = QtWidgets.QComboBox(self)
        self.combobox_layer.setGeometry(QtCore.QRect(20, 120, 351, 31))
        self.combobox_layer.activated.connect(self.layer_has_been_selected)

        self.label_field_to_select = QtWidgets.QLabel(self, text='Criteria')
        self.label_field_to_select.setGeometry(QtCore.QRect(401, 100, 311, 19))
        self.combobox_field = QtWidgets.QComboBox(self)
        self.combobox_field.setGeometry(QtCore.QRect(401, 120, 351, 31))

        # MacBeth
        self.label_macbeth_file_to_select = QtWidgets.QLabel(self, text='Select M-MACBETH file')
        self.label_macbeth_file_to_select.setGeometry(QtCore.QRect(20, 200, 311, 19))

        self.btn_load_macbeth_file = QtWidgets.QPushButton(self, text='Browse', clicked=self.browse_macbeth_file)
        self.btn_load_macbeth_file.setGeometry(QtCore.QRect(650, 220, 103, 31))

        self.inline_macbeth_filepath = QtWidgets.QLineEdit(self)
        self.inline_macbeth_filepath.setGeometry(QtCore.QRect(20, 220, 621, 31))

        self.combobox_macbeth_weights = QtWidgets.QComboBox(self)
        self.combobox_macbeth_weights.setGeometry(QtCore.QRect(20, 280, 731, 31))

        if not choose_macbeth_file:
            self.inline_macbeth_filepath.setText(self.parent().parent.macbeth_parser.filepath)
            weights = self.parent().parent.macbeth_parser.get_weights()
            weights_str = [f'{value}: {weight}' for value, weight in weights.items()]

            self.combobox_macbeth_weights.clear()
            self.combobox_macbeth_weights.addItems(weights_str)

        self.btn_add_criterion = QtWidgets.QPushButton(self, text='Add criterion', clicked=self.add_criterion)
        self.btn_add_criterion.setGeometry(QtCore.QRect(610, 350, 151, 31))

    def browse_geo_file(self):
        self.geo_filepath = QtWidgets.QFileDialog.getExistingDirectory(self)
        if self.geo_filepath == '':
            return

        try:
            self.combobox_layer.clear()
            self.combobox_layer.addItems(fiona.listlayers(self.geo_filepath))
            self.inline_geofile.setText(self.geo_filepath)
        except DriverError as e:
            popup = Popup(f"Failed to read the file: {e}", self)
            popup.show()

    def browse_macbeth_file(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self)
        if filepath == '':
            return

        try:
            self.parent().parent.macbeth_parser = MacbethParser(filepath)
            self.inline_macbeth_filepath.setText(filepath)

            weights = self.parent().parent.macbeth_parser.get_weights()
            weights_str = [f'{value}: {weight}' for value, weight in weights.items()]

            self.combobox_macbeth_weights.clear()
            self.combobox_macbeth_weights.addItems(weights_str)

        except (MacbethParserError, configparser.MissingSectionHeaderError) as e:
            popup = Popup(f"Failed to read the file: {e}", self)
            popup.show()

    def layer_has_been_selected(self):
        try:
            layer = self.combobox_layer.currentText()

            self.df = gis.io.read(self.geo_filepath, layer=layer)
            self.combobox_field.clear()
            self.combobox_field.addItems(self.df.columns)
        except DriverError as e:
            popup = Popup(f"Failed to read the file: {e}", self)
            popup.show()

    def add_criterion(self):
        if not self.are_data_ready():
            popup = Popup(f"Select file, layer and a field.", self)
            popup.show()

            return

        nbr_of_rows = self.parent().table.rowCount()
        self.parent().table.setRowCount(nbr_of_rows + 1)

        new_row_index = nbr_of_rows
        self.parent().table.setItem(new_row_index, 0, QTableWidgetItem(self.get_geo_filepath()))
        self.parent().table.setItem(new_row_index, 1, QTableWidgetItem(self.get_layer()))
        self.parent().table.setItem(new_row_index, 2, QTableWidgetItem(self.get_field()))
        self.parent().table.setItem(new_row_index, 3, QTableWidgetItem(self.get_weight()))

        # Adding dataframe to aggregate tab
        self.parent().dfs.append(copy.deepcopy(self.df))

        self.accept()

    def are_data_ready(self) -> bool:
        return not self.get_field() == ''

    def get_geo_filepath(self) -> str:
        return self.geo_filepath

    def get_layer(self) -> str:
        return self.combobox_layer.currentText()

    def get_field(self) -> str:
        return self.combobox_field.currentText()

    def get_weight(self) -> str:
        return self.combobox_macbeth_weights.currentText().split(':')[1].strip()
