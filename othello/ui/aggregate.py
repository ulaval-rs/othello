import functools

import geopandas
from PySide2 import QtWidgets, QtCore

from othello import gis
from othello.ui import errors
from othello.ui.criterion_wizard import CriterionWizard
from othello.ui.popup import Popup


class AggregateTab(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName('tab_aggregate')

        self.dfs = []

        self.label_data_section = QtWidgets.QLabel(self, text='Data')
        self.label_data_section.setGeometry(QtCore.QRect(10, 10, 81, 19))

        self.btn_add_criterion = QtWidgets.QPushButton(self, text='Add criterion', clicked=self.add_criterion)
        self.btn_add_criterion.setGeometry(QtCore.QRect(20, 40, 100, 31))

        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(QtCore.QRect(20, 80, 731, 260))
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Criterion', 'Layer', 'Field', 'New Name', 'Weight [0-1]'])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        self.btn_aggregate = QtWidgets.QPushButton(self, text='Aggregate to new file', clicked=self.aggregate)
        self.btn_aggregate.setGeometry(QtCore.QRect(610, 500, 151, 31))

    def add_criterion(self):
        wizard = CriterionWizard(self)
        wizard.show()

    def aggregate(self):
        try:
            self.assert_presence_of_at_least_2_criteria()
            self.assert_no_empty_new_criterion_names()
            self.assert_no_duplicate_in_mew_criterion_names()
            self.assert_weights_are_float()
            self.assert_weights_are_normalized()

            common_columns = functools.reduce(lambda c1, c2: set(c1).intersection(set(c2)), self.dfs)
            df = self.dfs[0][common_columns]

            filepath = QtWidgets.QFileDialog.getSaveFileName(self)
            if filepath[0] == '':
                return

            del self.dfs  # Saving memory space
            df = self._add_weighted_columns(df)
            gis.io.write(df, filepath[0])

        except errors.LessThenTwoCriteriaError:
            popup = Popup("At least 2 criteria must be loaded", self)
            popup.show()

        except (errors.EmptyNewCriterionNameError, errors.DuplicateNewCriterionNamesError):
            popup = Popup("All criteria must have new criterion name and be different", self)
            popup.show()

        except errors.WeightIsNotAFloatError:
            popup = Popup(f'Weights must be a float', self)
            popup.show()

        except errors.SumOfWeightNotEqualsToOneError:
            popup = Popup(f"Sum of weight must be equal to 1", self)
            popup.show()

        except Exception as e:
            popup = Popup(str(e), self)
            popup.show()

    def assert_presence_of_at_least_2_criteria(self):
        if len(self.dfs) < 2:
            raise errors.LessThenTwoCriteriaError

    def assert_no_empty_new_criterion_names(self):
        for row_index in range(self.table.rowCount()):
            try:
                # An error is raised when no text have been entered
                self.table.item(row_index, 3).text()
            except AttributeError:
                raise errors.EmptyNewCriterionNameError

    def assert_no_duplicate_in_mew_criterion_names(self):
        criteria = []
        for row_index in range(self.table.rowCount()):
            criterion = self.table.item(row_index, 3).text()

            if criterion in criteria:
                raise errors.DuplicateNewCriterionNamesError

            criteria.append(criterion)

    def assert_weights_are_float(self):
        for row_index in range(self.table.rowCount()):
            try:
                weight = self.table.item(row_index, 4).text()
                float(weight)

            except (ValueError, AttributeError):
                raise errors.WeightIsNotAFloatError

    def assert_weights_are_normalized(self):
        weights = []

        for row_index in range(self.table.rowCount()):
                weights.append(float(self.table.item(row_index, 4).text()))

        if round(sum(weights), 2) != 1.0:
            raise errors.SumOfWeightNotEqualsToOneError

    def _add_weighted_columns(self, df: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
        for row_index in range(self.table.rowCount()):
            filepath = self.table.item(row_index, 0).text()
            layer = self.table.item(row_index, 1).text()
            criterion = self.table.item(row_index, 2).text()
            criterion_name = self.table.item(row_index, 3).text()
            weight = float(self.table.item(row_index, 4).text())

            criterion_geoseries = gis.io.read(filepath, layer=layer)[criterion]
            df[criterion_name + '_np'] = criterion_geoseries
            df[criterion_name + '_p'] = weight * criterion_geoseries

        return df
