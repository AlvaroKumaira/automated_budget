import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


class FloatTableWidgetItem(QTableWidgetItem):
    def __init__(self, value=None):
        super().__init__()
        self.default_value = "0,00"  # Default value to fall back to
        self.setData(Qt.EditRole, value if value is not None else self.default_value)

    def setData(self, role, value):
        if role == Qt.EditRole:
            if value in [None, ""]:
                value = self.default_value

            if isinstance(value, float):
                # Format the number with a thousand separators and comma as decimal separator
                formatted_value = "{:,.2f}".format(value).replace(',', 'X').replace('.', ',').replace('X', '.')
                super().setData(Qt.DisplayRole, formatted_value)
            else:
                super().setData(role, value)
        else:
            super().setData(role, value)

    def data(self, role):
        if role == Qt.EditRole:
            # Remove formatting for internal processing
            return self.text().replace('.', '').replace(',', '.')
        return super().data(role)


