import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


class FloatTableWidgetItem(QTableWidgetItem):
    def __init__(self, value=None):
        super().__init__()
        self.default_value = "0"  # Default value to fall back to
        self.setData(Qt.EditRole, value if value is not None else self.default_value)

    def setData(self, role, value):
        # If the role is EditRole and the value is either None or an empty string, set to default value
        if role == Qt.EditRole:
            if value in [None, ""]:
                value = self.default_value

            if isinstance(value, float):
                formatted_value = format(value, '.2f').replace('.', ',')
                super().setData(Qt.DisplayRole, formatted_value)
            else:
                super().setData(role, value)
        else:
            super().setData(role, value)

    def data(self, role):
        if role == Qt.EditRole:
            return self.text().replace(',', '.')
        return super().data(role)

