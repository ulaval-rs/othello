import configparser
from typing import Optional, List

import fiona
import geopandas
from PySide2 import QtWidgets, QtCore
from fiona.errors import DriverError
from scipy.interpolate import interp1d

from othello import gis
from othello.macbeth.criterion import Criterion
from othello.macbeth.criterion_parameters import CriterionParameters
from othello.macbeth.errors import MacbethParserError
from othello.macbeth.parser import MacbethParser
from othello.macbeth.util import evaluate_new_values
from othello.ui.macbeth_scale import MacbethScale
from othello.ui.popup import Popup


class CriteriaTab(QtWidgets.QWidget):

    def __init__(self):
        self.df: Optional[geopandas.GeoDataFrame] = None
        self.macbeth_parser: Optional[MacbethParser] = None
        self.geo_filepath: Optional[str] = None

        self.criterion_parameters: Optional[CriterionParameters] = None

        super().__init__()

        self.setStyleSheet('')
        self.setObjectName('tab_criteria_macbeth')

        self.label_data_section = QtWidgets.QLabel(self, text='Data')
        self.label_data_section.setGeometry(QtCore.QRect(10, 10, 81, 19))

        self.inline_file_to_add_criteria_filepath = QtWidgets.QLineEdit(self, text='')
        self.inline_file_to_add_criteria_filepath.setGeometry(QtCore.QRect(20, 60, 621, 31))

        self.btn_browse_geo_file = QtWidgets.QPushButton(self, text='Browse', clicked=self.browse_geo_file)
        self.btn_browse_geo_file.setGeometry(QtCore.QRect(650, 60, 103, 31))

        self.label_file_to_add_criteria = QtWidgets.QLabel(self, text='Select a file')
        self.label_file_to_add_criteria.setGeometry(QtCore.QRect(20, 40, 311, 19))

        self.label_layer_to_select = QtWidgets.QLabel(self, text='Layer to transform')
        self.label_layer_to_select.setGeometry(QtCore.QRect(20, 100, 311, 19))
        self.combobox_layer = QtWidgets.QComboBox(self)
        self.combobox_layer.setGeometry(QtCore.QRect(20, 120, 351, 31))
        self.combobox_layer.activated.connect(self.layer_has_been_selected)

        self.label_field_to_select = QtWidgets.QLabel(self, text='Field to transform')
        self.label_field_to_select.setGeometry(QtCore.QRect(401, 100, 311, 19))
        self.combobox_field = QtWidgets.QComboBox(self)
        self.combobox_field.setGeometry(QtCore.QRect(401, 120, 351, 31))

        self.label_macbeth_section = QtWidgets.QLabel(self, text='MacBeth')
        self.label_macbeth_section.setGeometry(QtCore.QRect(10, 170, 81, 19))

        self.label_macbeth_file_to_select = QtWidgets.QLabel(self, text='Select M-MACBETH file')
        self.label_macbeth_file_to_select.setGeometry(QtCore.QRect(20, 200, 311, 19))

        self.inline_macbeth_filepath = QtWidgets.QLineEdit(self)
        self.inline_macbeth_filepath.setGeometry(QtCore.QRect(20, 220, 621, 31))

        self.btn_load_macbeth_file = QtWidgets.QPushButton(self, text='Browse', clicked=self.browse_macbeth_file)
        self.btn_load_macbeth_file.setGeometry(QtCore.QRect(650, 220, 103, 31))

        self.label_macbeth_criterion = QtWidgets.QLabel(self, text='Criterion to evaluate')
        self.label_macbeth_criterion.setGeometry(QtCore.QRect(20, 260, 311, 19))

        self.combobox_macbeth_criterion = QtWidgets.QComboBox(self)
        self.combobox_macbeth_criterion.setGeometry(QtCore.QRect(20, 280, 731, 31))
        self.combobox_macbeth_criterion.activated.connect(self.macbeth_criterion_has_been_selected)

        self.btn_add_column_to_file = QtWidgets.QPushButton(self, text='Add column', clicked=self.write_file)
        self.btn_add_column_to_file.setGeometry(QtCore.QRect(610, 500, 151, 31))

        self.macbeth_scale = MacbethScale(self)
        self.macbeth_scale.setGeometry(QtCore.QRect(20, 340, 731, 140))

    def layer_has_been_selected(self):
        try:
            layer = self.combobox_layer.currentText()

            self.df = gis.io.read(self.geo_filepath, layer=layer)
            self.combobox_field.clear()
            self.combobox_field.addItems(self.df.columns)
        except DriverError as e:
            popup = Popup(f"Failed to read the file: {e}", self)
            popup.show()

    def macbeth_criterion_has_been_selected(self):
        try:
            criterion_name = self.combobox_macbeth_criterion.currentText()
            criterion = self.macbeth_parser.find_criterion(criterion_name)
            self.criterion_parameters = self.macbeth_parser.get_criterion_parameters(criterion)
            self.macbeth_scale.set_values(self.criterion_parameters.levels, self.criterion_parameters.weights)
        except KeyError as e:
            popup = Popup(f"Value not found in the macbeth file for this criterion: {e}", self)
            popup.show()

    def browse_geo_file(self):
        self.geo_filepath = QtWidgets.QFileDialog.getExistingDirectory(self)
        if self.geo_filepath == '':
            return

        try:
            self.combobox_layer.clear()
            self.combobox_layer.addItems(fiona.listlayers(self.geo_filepath))
            self.inline_file_to_add_criteria_filepath.setText(self.geo_filepath)
        except DriverError as e:
            popup = Popup(f"Failed to read the file: {e}", self)
            popup.show()

    def browse_macbeth_file(self):
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self)
        if filepath == '':
            return

        try:
            self.macbeth_parser = MacbethParser(filepath)
            self.inline_macbeth_filepath.setText(filepath)
            self.combobox_macbeth_criterion.addItems(
                [c.name for c in self.macbeth_parser.get_criteria()]
            )
        except (MacbethParserError, configparser.MissingSectionHeaderError) as e:
            popup = Popup(f"Failed to read the file: {e}", self)
            popup.show()

    def write_file(self):
        if self.df is None:
            popup = Popup("No data has been loaded", self)
            popup.show()
            return

        filepath = QtWidgets.QFileDialog.getSaveFileName(self)
        if filepath == '':
            return

        try:
            self.df['macbeth'] = evaluate_new_values(
                series=self.df[self.combobox_field.currentText()],
                criterion_parameters=self.criterion_parameters
            )

            gis.io.write(self.df, filepath[0])
        except Exception as e:
            popup = Popup(str(e), self)
            popup.show()


