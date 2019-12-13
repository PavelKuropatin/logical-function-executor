import sys
from typing import Dict, List

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget

from domain.expression_parser import ExpressionParser
from util.constants import OP_MAPPING
from util.generate_utils import generate_variables


class LogicalFunctionParser(QMainWindow):

    def __init__(self, file):
        super(LogicalFunctionParser, self).__init__()
        self.__init_data()
        uic.loadUi(file, self)
        self.__init_ui()
        self.show()

    def __init_data(self):
        self.__default_expression = "x1  ⋀ x2  → ( ¬ x3 / x4 )"
        self.__parser = ExpressionParser()

    def __init_ui(self):
        self.operator_table.setRowCount(len(OP_MAPPING))
        self.operator_table.setColumnCount(2)
        self.operator_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.operator_table.cellDoubleClicked.connect(self.insert_operator2)

        i = 0
        for symbol, cls in OP_MAPPING.items():
            LogicalFunctionParser.__set_table_item(self.operator_table, i, 0, str(cls.name()))
            LogicalFunctionParser.__set_table_item(self.operator_table, i, 1, str(symbol))
            i += 1

        self.expression_edit.setText(self.__default_expression)

    def insert_operator(self):
        pass

    def insert_operator2(self, row, column):
        o = list(OP_MAPPING.keys())[row]
        self.expression_edit.setText(self.expression_edit.text() + f" {o} ")

    @staticmethod
    def __set_table_item(table, i, j, value):
        item = QTableWidgetItem(value, QTableWidgetItem.Type.real)
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(i, j, item)

    def eval(self):
        try:
            expression = self.expression_edit.text()
            self.__parser.parse(expression)
            variable_names = self.__parser.variables
            data_set = generate_variables(variable_names)

            for data in data_set:
                data["f"] = self.__parser.compute(data)

            self.__render_data_set(data_set)
        except Exception as e:
            print(e)

    def __render_data_set(self, data_set: List[Dict]):
        data_set = [
            {
                key: value
                for key, value in data.items()
            }
            for data in data_set
        ]
        rows = len(data_set)
        columns = len(data_set[0])
        column_names = data_set[0].keys()

        table: QTableWidget = self.result_table
        table.clear()
        table.setRowCount(rows)
        table.setColumnCount(columns)
        table.setHorizontalHeaderLabels(column_names)

        for i, data in enumerate(data_set):
            for j, key in enumerate(data.keys()):
                LogicalFunctionParser.__set_table_item(self.result_table, i, j, str(data[key]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LogicalFunctionParser("window.ui")
    sys.exit(app.exec_())
