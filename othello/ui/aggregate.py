import copy
import functools

import geopandas
from PySide2 import QtWidgets, QtCore

from othello import gis
from othello.ui import errors
from othello.ui.criterion_remover import CriterionRemover
from othello.ui.criterion_wizard import CriterionWizard
from othello.ui.popup import Popup


class AggregateTab(QtWidgets.QWidget):

    def __init__(self, parent):
        self.parent = parent

        super().__init__()

        self.setObjectName('tab_aggregate')

        self.dfs = []

        self.label_data_section = QtWidgets.QLabel(self, text='Data')
        self.label_data_section.setGeometry(QtCore.QRect(10, 10, 81, 19))

        self.btn_add_criterion = QtWidgets.QPushButton(self, text='Add criterion', clicked=self.add_criterion)
        self.btn_add_criterion.setGeometry(QtCore.QRect(20, 40, 100, 31))

        self.btn_remove_criterion = QtWidgets.QPushButton(self, text='Remove criterion', clicked=self.remove_criterion)
        self.btn_remove_criterion.setGeometry(QtCore.QRect(130, 40, 120, 31))

        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(QtCore.QRect(20, 80, 731, 400))
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Criterion', 'Layer', 'Field', 'Weight [0-1]'])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.btn_aggregate_existing_file = QtWidgets.QPushButton(
            self,
            text='Aggregate to existing file',
            clicked=lambda: self.aggregate(to_new_file=False)
        )
        self.btn_aggregate_existing_file.setGeometry(QtCore.QRect(450, 500, 151, 31))

        self.btn_aggregate_new_file = QtWidgets.QPushButton(
            self,
            text='Aggregate to new file',
            clicked=lambda: self.aggregate(to_new_file=True)
        )
        self.btn_aggregate_new_file.setGeometry(QtCore.QRect(610, 500, 151, 31))

    def add_criterion(self):
        wizard = CriterionWizard(self, choose_macbeth_file=self.parent.macbeth_parser is None)
        wizard.show()

    def aggregate(self, to_new_file: bool):
        try:
            self.assert_presence_of_at_least_2_criteria()
            self.assert_weights_are_float()
            # self.assert_weights_are_normalized()

            common_columns = functools.reduce(lambda c1, c2: set(c1).intersection(set(c2)), self.dfs)
            df = copy.deepcopy(self.dfs[0][common_columns])

            if to_new_file:
                filepath = QtWidgets.QFileDialog.getSaveFileName(self)[0]
            else:
                filepath = QtWidgets.QFileDialog.getExistingDirectory(self)

            if filepath == '':
                return
            if '.gdb' not in filepath.lower():
                popup = Popup('Only .gdb files are supported.', self)
                popup.show()
                return

            df = self.add_weighted_columns(df)
            gis.io.write(df, filepath, layer='FinalLayer')

            popup = Popup(f'The file "{filepath}" have been written.', self)
            popup.show()

        except errors.LessThenTwoCriteriaError:
            popup = Popup('At least 2 criteria must be loaded', self)
            popup.show()

        except (errors.EmptyNewCriterionNameError, errors.DuplicateNewCriterionNamesError):
            popup = Popup('All criteria must have new criterion name and be different', self)
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

    def assert_weights_are_float(self):
        for row_index in range(self.table.rowCount()):
            try:
                weight = self.table.item(row_index, 3).text()
                float(weight)

            except (ValueError, AttributeError):
                raise errors.WeightIsNotAFloatError

    def assert_weights_are_normalized(self):
        weights = []

        for row_index in range(self.table.rowCount()):
            weights.append(float(self.table.item(row_index, 3).text()))

        if round(sum(weights), 2) != 1.0:
            raise errors.SumOfWeightNotEqualsToOneError

    def add_weighted_columns(self, df: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
        weighted_columns = []

        for row_index in range(self.table.rowCount()):
            filepath = self.table.item(row_index, 0).text()
            layer = self.table.item(row_index, 1).text()
            criterion = self.table.item(row_index, 2).text()
            weight = float(self.table.item(row_index, 3).text())

            # Removing the _mb suffix
            criterion = criterion.replace('_mb', '')

            criterion_geoseries = gis.io.read(filepath, layer=layer)[criterion]
            df[criterion + '_np'] = criterion_geoseries
            df[criterion + '_p'] = weight * criterion_geoseries
            weighted_columns.append(criterion + '_p')

        # Final score in a new series
        df['FinalScore'] = [0 for _ in range(len(df))]
        for column in weighted_columns:
            df['FinalScore'] += df[column]

        return df

    def remove_criterion(self):
        if self.table.rowCount() == 0:
            popup = Popup('No criterion to remove', self)
            popup.show()
            return

        criterion_remover = CriterionRemover(self)
        criterion_remover.show()
