import logging
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from PyQt5.QtCore import QItemSelectionModel, Qt, QThreadPool
from . import resources_rc
from interface.item_class import FloatTableWidgetItem
from database.basic_functions import save_to_excel
from database.queries import item_info, sales_six_months_client, sales_six_months, cost_based_on_stock, item_quantity
from processing.client_search import search_function
from processing.processing_thread import ProcessingRunnable
from processing.table_function import process_table_info

logger = logging.getLogger(__name__)


class MainLogic:
    def __init__(self, ui):
        self.ui = ui
        self.threadpool = QThreadPool()
        self.client_name = None
        self.client_code = None

        self.column_indices = {
            "Código": 0,
            "Descrição": 1,
            "Quantidade": 2,
            "Quantidade disponível": 3,
            "Custo": 4,
            "Preço calculado": 5,
            "U.V. Geral": 6,
            "U.V. Cliente": 7,
            "Desconto(%)": 8,
            "Over(%)": 9,
            "Margem(%)": 10,
            "Preço unitário": 11,
            "Preço final": 12
        }

    def start_process(self):
        self.ui.save_progressbar.show()

    def stop_process(self):
        self.ui.save_progressbar.hide()

    def search(self):
        client_code = self.ui.client_search.text()
        self.client_code = client_code

        processing_runnable_client = ProcessingRunnable(search_function, client_code)
        processing_runnable_client.signals.process_result.connect(self.update_label)

        self.threadpool.start(processing_runnable_client)

    def update_label(self, name):
        if name == "Cliente":
            self.ui.info_label.setText("Info: Cliente não encontrado!")
            self.client_name = "Geral"
        else:
            formated_name = name.strip().title()
            self.ui.info_label.setText(formated_name)
            self.client_name = formated_name

    def add_row(self):
        if self.ui.filial_select.currentText() == '':
            QMessageBox.warning(self.ui, "Aviso", "Você precisa selecionar uma filial antes de continuar!")
        else:
            row_count = self.ui.budget_table.rowCount()
            self.ui.budget_table.insertRow(row_count)

    def remove_last_row(self):
        if self.ui.budget_table.rowCount() > 0:
            self.ui.budget_table.removeRow(self.ui.budget_table.rowCount() - 1)

    def save_table(self):
        if self.ui.budget_table.rowCount() > 0:
            df = self.table_to_dataframe(self.ui.budget_table)
            processing_runnable_save = ProcessingRunnable(save_to_excel, df, "Orçamento", self.client_name,
                                                          open_file=True)

            self.threadpool.start(processing_runnable_save)
        else:
            QMessageBox.warning(self.ui, "Aviso", "Você não pode salvar uma tabela vazia!")

    def table_to_dataframe(self, table_widget):
        data = []
        for row in range(table_widget.rowCount()):
            row_data = []
            for column in range(table_widget.columnCount()):
                item = table_widget.item(row, column)
                if item is not None:
                    text = item.text()
                    # Convert to float if the column is supposed to be numeric and the text is not '-'
                    if column >= self.column_indices['Quantidade'] and text != '-':
                        # Remove formatting and convert to float
                        number = float(text.replace('.', '').replace(',', '.'))
                        row_data.append(number)
                    elif text == '-':
                        # Append a NaN where '-' is found
                        row_data.append(np.nan)
                    else:
                        row_data.append(text)
                else:
                    row_data.append("")
            data.append(row_data)

        # Use the keys from column_indices as column names
        column_names = [name for name, index in sorted(self.column_indices.items(), key=lambda pair: pair[1])]

        # Create a DataFrame
        df = pd.DataFrame(data, columns=column_names)

        # Convert columns after 'Quantidade' to numeric, errors='coerce' will handle '-' as NaN
        numeric_columns = column_names[self.column_indices['Quantidade'] + 1:]
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        return df


class TableLogic(MainLogic):

    def __init__(self, ui):
        super().__init__(ui)
        self.group_codes = {}
        self.costs = {}
        self.filial = None
        self.unit_prices = {}
        self.setup_connections()

    def setup_connections(self):
        self.ui.budget_table.cellClicked.connect(self.handle_price_cell_selected)
        self.ui.budget_table.cellChanged.connect(self.handle_item_cell_change)

        # Define funtions to buttons
        self.ui.add_line_button.clicked.connect(self.add_row)
        self.ui.remove_line_button.clicked.connect(self.remove_last_row)
        self.ui.save_table_button.clicked.connect(self.save_table)
        self.ui.search_button.clicked.connect(self.search)

    def handle_price_cell_selected(self, row, column):
        # Get the selection model of the table
        selection_model = self.ui.budget_table.selectionModel()

        # Deselect cells in the same row, except the clicked one
        for col in range(self.ui.budget_table.columnCount()):
            if col != column:
                index = self.ui.budget_table.model().index(row, col)
                selection_model.select(index, QItemSelectionModel.Deselect)

        # Check if the selected column is "Preço calculado", "U.V. Geral", or "U.V. Cliente"
        if column in [self.column_indices["Preço calculado"],
                      self.column_indices["U.V. Geral"],
                      self.column_indices["U.V. Cliente"]]:
            # Get the value of the selected cell
            selected_item = self.ui.budget_table.item(row, column)
            if selected_item is not None:
                cell_value = selected_item.data(Qt.EditRole)
                if cell_value != '-':
                    selected_value = float(cell_value)
                else:
                    selected_value = cell_value

                # Calculate the adjusted price for "Preço Unitário"
                original_price = float(selected_value)
                discount_item = self.ui.budget_table.item(row, self.column_indices["Desconto(%)"])
                over_item = self.ui.budget_table.item(row, self.column_indices["Over(%)"])

                if discount_item and discount_item.data(Qt.EditRole) != '':
                    discount_percentage = float(discount_item.data(Qt.EditRole).replace(",", "."))
                    original_price *= (1 - discount_percentage / 100)
                else:
                    discount_percentage = 0
                    original_price *= (1 - discount_percentage / 100)

                if over_item and over_item.data(Qt.EditRole) != '':
                    over_percentage = float(over_item.data(Qt.EditRole).replace(",", "."))
                    original_price *= (1 + over_percentage / 100)
                else:
                    over_percentage = 0
                    original_price *= (1 + over_percentage / 100)

                # Create QTableWidgetItem with the adjusted price
                adjusted_price_item = FloatTableWidgetItem(original_price)
                adjusted_price_item.setFlags(adjusted_price_item.flags() & ~Qt.ItemIsEditable)
                adjusted_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                # Set the adjusted price to "Preço Unitário"
                self.ui.budget_table.setItem(row, self.column_indices["Preço unitário"], adjusted_price_item)

                # Try to get the value at column index of "Quantidade" and multiply for the Preço Final column
                item_at_index_quantity = self.ui.budget_table.item(row, self.column_indices["Quantidade"])
                if item_at_index_quantity is not None:
                    try:
                        # Retrieve the float value directly
                        value_at_index_quantity = float(item_at_index_quantity.data(Qt.EditRole))
                        result_value = float(original_price) * value_at_index_quantity

                        # Use FloatTableWidgetItem for setting the result
                        result_value_to_table = FloatTableWidgetItem(result_value)
                        result_value_to_table.setFlags(result_value_to_table.flags() & ~Qt.ItemIsEditable)
                        result_value_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                        # Set the result to the column at index of "Preço final"
                        self.ui.budget_table.setItem(row, self.column_indices["Preço final"], result_value_to_table)
                    except ValueError:
                        # Handle cases where conversion to float fails
                        result_value = '-'
                        self.ui.budget_table.setItem(row, self.column_indices["Preço final"],
                                                     QTableWidgetItem(result_value))

                    # Additional code to calculate and set profit margin
                    unit_price_item = self.ui.budget_table.item(row, self.column_indices["Preço unitário"])
                    cost_item = self.ui.budget_table.item(row, self.column_indices["Custo"])

                    if unit_price_item is not None and cost_item is not None:
                        try:
                            unit_price = float(unit_price_item.data(Qt.EditRole).replace(",", "."))
                            cost = float(cost_item.data(Qt.EditRole).replace(",", "."))
                            if cost != 0:
                                margin = ((unit_price - cost) / cost) * 100
                                margin_item = FloatTableWidgetItem(margin)
                            else:
                                margin_item = QTableWidgetItem("-")
                        except ValueError:
                            margin_item = QTableWidgetItem("-")

                        margin_item.setFlags(margin_item.flags() & ~Qt.ItemIsEditable)
                        margin_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        self.ui.budget_table.setItem(row, self.column_indices["Margem(%)"], margin_item)

    def handle_item_cell_change(self, row, column):
        # Handles the selected filial
        filial_codes = {
            "Matriz - MG": "0101",
            "Poconé - MT": "0103",
            "Cariacica - ES": "0104",
            "Parauapebas - PA": "0105"
        }
        filial_name = self.ui.filial_select.currentText()
        self.filial = filial_codes.get(filial_name)

        # This first part handles the item column changes
        item_code_column_index = self.column_indices["Código"]
        if column == item_code_column_index:  # Check if the edited cell is in the item code column
            item = self.ui.budget_table.item(row, column)
            if item is not None and item.text().strip():  # Check if the cell is not empty
                item_code = item.text()
                # Create ProcessingRunnable instance
                processing_runnable_item = ProcessingRunnable(process_table_info, item_info, item_code)
                # Connect signals
                processing_runnable_item.signals.process_result.connect(lambda df: self.update_description(df, row))
                # Start the task with QThreadPool
                self.threadpool.start(processing_runnable_item)
            else:
                # Handle the case where the cell is empty (if needed)
                pass

        # This second part handles the quantity column changes
        quantity_column_index = self.column_indices["Quantidade"]
        if column == quantity_column_index:  # Check if the edited cell is in the quantity column
            quant = self.ui.budget_table.item(row, column)
            if quant is not None and quant.text().strip():  # Check is the cell is not empty
                # Create ProcessingRunnable instance for cost_based_on_stock
                processing_runnable = ProcessingRunnable(process_table_info, cost_based_on_stock, self.group_codes[row])
                # Connect signals
                processing_runnable.signals.process_result.connect(lambda df: self.update_cost(df, row))
                processing_runnable.signals.process_stopped.connect(lambda: self.update_unit_price(row))
                # Start the task with QThreadPool
                self.threadpool.start(processing_runnable)

                # Create ProcessingRunnable instance for sales_six_months
                processing_runnable1 = ProcessingRunnable(process_table_info, sales_six_months, self.filial,
                                                          self.group_codes[row])
                # Connect signals
                processing_runnable1.signals.process_result.connect(lambda df: self.update_general_sale(df, row))
                # Start the task with QThreadPool
                self.threadpool.start(processing_runnable1)

                # Create ProcessingRunnable instance
                processing_runnable2 = ProcessingRunnable(process_table_info, sales_six_months_client, self.filial,
                                                          self.group_codes[row], self.client_code)
                # Connect signals
                processing_runnable2.signals.process_result.connect(lambda df: self.update_client_sale(df, row))
                # Start the task with QThreadPool
                self.threadpool.start(processing_runnable2)

                # Create ProcessingRunnable instance
                processing_runnable3 = ProcessingRunnable(process_table_info, item_quantity, self.filial,
                                                          self.group_codes[row])
                # Connect signals
                processing_runnable3.signals.process_result.connect(lambda df: self.update_quantity(df, row))
                # Start the task with QThreadPool
                self.threadpool.start(processing_runnable3)

                # Set default value for "Desconto(%)"
                discount_col_index = self.column_indices["Desconto(%)"]
                discount_item = FloatTableWidgetItem()  # Creating a QTableWidgetItem with default value "0"
                self.ui.budget_table.setItem(row, discount_col_index, discount_item)

                # Set default value for "Over(%)"
                over_col_index = self.column_indices["Over(%)"]
                over_item = FloatTableWidgetItem()  # Creating a QTableWidgetItem with default value "0"
                self.ui.budget_table.setItem(row, over_col_index, over_item)

    def update_description(self, item_df, row):
        description_column_index = self.column_indices["Descrição"]
        if item_df is None or item_df.empty:
            description = "Item não encontrado!"
            description_to_table = QTableWidgetItem(description)

            # Apply setFlags to description_to_table
            description_to_table.setFlags(description_to_table.flags() & ~Qt.ItemIsEditable)
            description_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.budget_table.setItem(row, description_column_index, description_to_table)
            self.ui.budget_table.resizeColumnsToContents()
        else:
            group_code = item_df['B1_ZGRUPO'].iloc[0]
            self.group_codes[row] = group_code  # Store the group code for the row
            description = item_df['B1_DESC'].iloc[0]
            description_to_table = QTableWidgetItem(description)

            # Apply setFlags to description_to_table
            description_to_table.setFlags(description_to_table.flags() & ~Qt.ItemIsEditable)
            description_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.budget_table.setItem(row, description_column_index, description_to_table)
            self.ui.budget_table.resizeColumnsToContents()

    def update_quantity(self, quantity_df, row):
        quantity_column_index = self.column_indices["Quantidade disponível"]
        if quantity_df is None or quantity_df.empty:
            quantity = "-"
            quantity_to_table = QTableWidgetItem(quantity)

            # Apply setFlags to cost_to_table
            quantity_to_table.setFlags(quantity_to_table.flags() & ~Qt.ItemIsEditable)
            quantity_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.budget_table.setItem(row, quantity_column_index, quantity_to_table)
            self.ui.budget_table.resizeColumnsToContents()
        else:
            quantity = quantity_df['quantidade'].iloc[0]
            quantity_to_table = FloatTableWidgetItem(quantity)

            # Apply setFlags to cost_to_table
            quantity_to_table.setFlags(quantity_to_table.flags() & ~Qt.ItemIsEditable)
            quantity_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.budget_table.setItem(row, quantity_column_index, quantity_to_table)
            self.ui.budget_table.resizeColumnsToContents()

    def update_cost(self, cost_df, row):
        cost_column_index = self.column_indices["Custo"]
        if cost_df is None or cost_df.empty:
            cost = "-"
            cost_to_table = QTableWidgetItem(cost)

            # Apply setFlags to cost_to_table
            cost_to_table.setFlags(cost_to_table.flags() & ~Qt.ItemIsEditable)
            cost_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.budget_table.setItem(row, cost_column_index, cost_to_table)
            self.ui.budget_table.resizeColumnsToContents()
        else:
            cost_value = cost_df['Average'].iloc[0]
            cost_to_table = FloatTableWidgetItem(cost_value)

            # Apply setFlags to cost_to_table
            cost_to_table.setFlags(cost_to_table.flags() & ~Qt.ItemIsEditable)
            cost_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.costs[row] = cost_value
            self.ui.budget_table.setItem(row, cost_column_index, cost_to_table)
            self.ui.budget_table.resizeColumnsToContents()

    def update_general_sale(self, general_df, row):
        general_sale_column_index = self.column_indices["U.V. Geral"]
        if general_df is None or general_df.empty:
            general_sale = "-"
            general_sale_to_table = FloatTableWidgetItem(general_sale)

            # Apply setFlags to general_sale_to_table
            general_sale_to_table.setFlags(general_sale_to_table.flags() & ~Qt.ItemIsEditable)
            general_sale_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.budget_table.setItem(row, general_sale_column_index, general_sale_to_table)
            self.ui.budget_table.resizeColumnsToContents()
        else:
            sale_value = general_df['ValorUnitario'].iloc[0]
            general_sale_to_table = FloatTableWidgetItem(sale_value)

            # Apply setFlags to general_sale_to_table
            general_sale_to_table.setFlags(general_sale_to_table.flags() & ~Qt.ItemIsEditable)
            general_sale_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.budget_table.setItem(row, general_sale_column_index, general_sale_to_table)
            self.ui.budget_table.resizeColumnsToContents()

    def update_client_sale(self, client_sale_df, row):
        client_sale_column_index = self.column_indices["U.V. Cliente"]
        if client_sale_df is None or client_sale_df.empty:
            client_sale = "-"
            client_sale_to_table = QTableWidgetItem(client_sale)

            # Apply setFlags to client_sale_to_table
            client_sale_to_table.setFlags(client_sale_to_table.flags() & ~Qt.ItemIsEditable)
            client_sale_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.budget_table.setItem(row, client_sale_column_index, client_sale_to_table)
            self.ui.budget_table.resizeColumnsToContents()
        else:
            client_sale_value = client_sale_df['ValorUnitario'].iloc[0]
            client_sale_to_table = FloatTableWidgetItem(client_sale_value)

            # Apply setFlags to client_sale_to_table
            client_sale_to_table.setFlags(client_sale_to_table.flags() & ~Qt.ItemIsEditable)
            client_sale_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.ui.budget_table.setItem(row, client_sale_column_index, client_sale_to_table)
            self.ui.budget_table.resizeColumnsToContents()

    def update_unit_price(self, row):
        cost_column_index = self.column_indices["Custo"]
        unit_price_column_index = self.column_indices["Preço calculado"]
        limits_factors = [
            (0.25, 25),
            (1.00, 10),
            (10.00, 7.5),
            (100.00, 2.5),
            (200.00, 2.5),
            (400.00, 2),
            (600.00, 2),
            (800.00, 2),
            (1000.00, 1.5),
            (10000.00, 1.25),
            (100000.00, 1.25),
            (200000.00, 1.25),
            (1000000.00, 1.25)
        ]

        cell_item = self.ui.budget_table.item(row, cost_column_index)
        if cell_item is not None:
            try:
                cell_value_float = float(cell_item.data(Qt.EditRole).replace(",", "."))
                # Find the appropriate factor
                factor = next((factor for limit, factor in limits_factors if cell_value_float <= limit), None)
                if factor is not None:
                    result = cell_value_float * factor
                    self.unit_prices[row] = result
                    result_to_table = FloatTableWidgetItem(result)

                    # Apply setFlags to client_sale_to_table
                    result_to_table.setFlags(result_to_table.flags() & ~Qt.ItemIsEditable)
                    result_to_table.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                    self.ui.budget_table.setItem(row, unit_price_column_index, result_to_table)
                    self.ui.budget_table.resizeColumnsToContents()
                else:
                    logger.error("No matching factor found")
            except ValueError:
                logger.error("The cell value is not a valid float number")
        else:
            logger.error("No item in specified cell")
