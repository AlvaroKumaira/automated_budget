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
            "Agrupamento": 1,
            "Descrição": 2,
            "Quantidade": 3,
            "Quantidade disponível": 4,
            "Custo": 5,
            "Preço calculado": 6,
            "U.V. Geral": 7,
            "U.V. Cliente": 8,
            "Desconto(%)": 9,
            "Over(%)": 10,
            "Margem(%)": 11,
            "Preço unitário": 12,
            "Preço final": 13
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

            # Create a non-editable item for the "Quantidade disponível" column
            item_quantidade_disponivel = QTableWidgetItem()
            item_quantidade_disponivel.setFlags(item_quantidade_disponivel.flags() & ~Qt.ItemIsEditable)
            self.ui.budget_table.setItem(row_count, self.column_indices["Quantidade disponível"],
                                         item_quantidade_disponivel)

            # Create a non-editable item for the "Descrição" column
            item_descricao = QTableWidgetItem()
            item_descricao.setFlags(item_descricao.flags() & ~Qt.ItemIsEditable)
            self.ui.budget_table.setItem(row_count, self.column_indices["Descrição"], item_descricao)

            # Create a non-editable item for the "Agrupamento" column
            item_group = QTableWidgetItem()
            item_group.setFlags(item_group.flags() & ~Qt.ItemIsEditable)
            self.ui.budget_table.setItem(row_count, self.column_indices["Agrupamento"], item_group)

            # Create a non-editable item for the "Quantidade" column
            quantity = QTableWidgetItem()
            quantity.setFlags(quantity.flags() & ~Qt.ItemIsEditable)
            self.ui.budget_table.setItem(row_count, self.column_indices["Quantidade"], quantity)

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
        required_columns = ["Código", "Descrição", "Quantidade", "Preço unitário", "Preço final"]
        required_column_indices = [self.column_indices[col] for col in required_columns]

        data = []
        for row in range(table_widget.rowCount()):
            row_data = []
            for column in required_column_indices:
                item = table_widget.item(row, column)
                if item is not None:
                    text = item.text()
                    if column >= self.column_indices['Quantidade'] and text != '-':
                        number = float(text.replace('.', '').replace(',', '.'))
                        row_data.append(number)
                    elif text == '-':
                        row_data.append(np.nan)
                    else:
                        row_data.append(text)
                else:
                    row_data.append("")
            data.append(row_data)

        # Create a DataFrame with only the required columns
        df = pd.DataFrame(data, columns=required_columns)

        # Convert 'Quantidade', 'Preço unitário', and 'Preço final' columns to numeric, handling '-' as NaN
        numeric_columns = ['Quantidade', 'Preço unitário', 'Preço final']
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

        return df


class TableLogic(MainLogic):

    def __init__(self, ui):
        super().__init__(ui)
        self.group_codes = {}
        self.filial = None
        self.setup_connections()

    def setup_connections(self):
        self.ui.budget_table.cellClicked.connect(self.handle_price_cell_selected)
        self.ui.budget_table.cellChanged.connect(self.handle_item_cell_change)

        # Define funtions to buttons
        self.ui.add_line_button.clicked.connect(self.add_row)
        self.ui.remove_line_button.clicked.connect(self.remove_last_row)
        self.ui.save_table_button.clicked.connect(self.save_table)
        self.ui.search_button.clicked.connect(self.search)

    def create_and_start_runnable(self, runnable_function, row, func, connect_func, include_filial=False,
                                  additional_params=[]):
        # Conditionally include 'self.filial' based on 'include_filial' flag
        all_params = [self.filial] + additional_params if include_filial else additional_params

        # Create ProcessingRunnable with the specified runnable_function
        processing_runnable = ProcessingRunnable(runnable_function, func, *all_params, self.group_codes[row])
        processing_runnable.signals.process_result.connect(lambda df, r=row: connect_func(df, r))
        processing_runnable.signals.process_stopped.connect(lambda r=row: self.update_unit_price(r))
        self.threadpool.start(processing_runnable)

    def create_and_set_table_item(self, row, column_index, value=None, item_type=FloatTableWidgetItem,
                                  alignment=Qt.AlignLeft | Qt.AlignVCenter, editable=False):
        # If value is None and item_type is FloatTableWidgetItem, use the default value of FloatTableWidgetItem
        if value is None and item_type == FloatTableWidgetItem:
            table_item = item_type()
        else:
            table_item = item_type(value)

        # Set flags
        if not editable:
            table_item.setFlags(table_item.flags() & ~Qt.ItemIsEditable)

        # Set text alignment
        table_item.setTextAlignment(alignment)

        # Add item to the table
        self.ui.budget_table.setItem(row, column_index, table_item)
        self.ui.budget_table.resizeColumnsToContents()

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
                    selected_value = 0

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
                self.create_and_set_table_item(row, self.column_indices["Preço unitário"], original_price,
                                               FloatTableWidgetItem, Qt.AlignRight | Qt.AlignVCenter)

                self.calculate_and_set_final_price(row, original_price)

                self.calculate_and_set_margin(row, selected_value)

    def calculate_and_set_margin(self, row, original_price):
        margin_column_index = self.column_indices["Margem(%)"]
        unit_price_item = self.ui.budget_table.item(row, self.column_indices["Preço unitário"])
        cost_item = self.ui.budget_table.item(row, self.column_indices["Custo"])
        discount_item = self.ui.budget_table.item(row, self.column_indices["Desconto(%)"])

        if unit_price_item is not None and cost_item is not None:
            try:
                unit_price = float(unit_price_item.data(Qt.EditRole).replace(",", "."))
                cost = float(cost_item.data(Qt.EditRole).replace(",", "."))
                if cost != 0:
                    margin = ((unit_price - cost) / cost) * 100

                    # Check for discount and margin condition
                    if discount_item is not None and float(discount_item.data(Qt.EditRole)) != 0:
                        if margin < 25:
                            QMessageBox.warning(self.ui, "Aviso", "A margem não pode ser menor que 25%")
                            self.create_and_set_table_item(row, self.column_indices["Desconto(%)"],
                                                           item_type=FloatTableWidgetItem)

                            self.create_and_set_table_item(row, self.column_indices["Preço unitário"],
                                                           original_price, FloatTableWidgetItem,
                                                           Qt.AlignRight | Qt.AlignVCenter)

                            self.calculate_and_set_final_price(row, original_price)
                            return
                else:
                    self.create_and_set_table_item(row, margin_column_index,
                                                   item_type=FloatTableWidgetItem)
            except ValueError:
                self.create_and_set_table_item(row, margin_column_index,
                                               item_type=FloatTableWidgetItem)

            self.create_and_set_table_item(row, margin_column_index, margin, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)

    def calculate_and_set_final_price(self, row, original_price):
        final_price_column_index = self.column_indices["Preço final"]
        item_at_index_quantity = self.ui.budget_table.item(row, self.column_indices["Quantidade"])
        if item_at_index_quantity is not None:
            try:
                value_at_index_quantity = float(item_at_index_quantity.data(Qt.EditRole))
                result_value = float(original_price) * value_at_index_quantity
                self.create_and_set_table_item(row, final_price_column_index, result_value,
                                               FloatTableWidgetItem, Qt.AlignRight | Qt.AlignVCenter)

            except ValueError:
                result_value = '-'
                self.create_and_set_table_item(row, final_price_column_index, result_value,
                                               FloatTableWidgetItem, Qt.AlignRight | Qt.AlignVCenter)

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

        # This second part handles the quantity column changes
        quantity_column_index = self.column_indices["Quantidade"]
        if column == quantity_column_index:  # Check if the edited cell is in the quantity column
            quant = self.ui.budget_table.item(row, column)
            if quant is not None and quant.text().strip():
                quant.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                self.create_and_start_runnable(process_table_info, row, cost_based_on_stock, self.update_cost,
                                               include_filial=False)
                self.create_and_start_runnable(process_table_info, row, sales_six_months, self.update_general_sale,
                                               include_filial=True)
                self.create_and_start_runnable(process_table_info, row, sales_six_months_client,
                                               self.update_client_sale, include_filial=True,
                                               additional_params=[self.client_code])
                self.create_and_start_runnable(process_table_info, row, item_quantity, self.update_quantity,
                                               include_filial=True)

                # Set default value for "Desconto(%)"
                discount_col_index = self.column_indices["Desconto(%)"]
                discount_item = FloatTableWidgetItem()  # Creating a QTableWidgetItem with default value "0"
                discount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.ui.budget_table.setItem(row, discount_col_index, discount_item)

                # Set default value for "Over(%)"
                over_col_index = self.column_indices["Over(%)"]
                over_item = FloatTableWidgetItem()  # Creating a QTableWidgetItem with default value "0"
                over_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.ui.budget_table.setItem(row, over_col_index, over_item)

    def update_description(self, item_df, row):
        description_column_index = self.column_indices["Descrição"]
        group_column_index = self.column_indices["Agrupamento"]
        if item_df is None or item_df.empty:
            description = "Item não encontrado!"
            self.create_and_set_table_item(row, description_column_index, description, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)
        else:
            group_code = item_df['B1_ZGRUPO'].iloc[0]
            if group_code == '        ':
                group = "Item sem agrupamento!"
                self.create_and_set_table_item(row, group_column_index, group, FloatTableWidgetItem,
                                               Qt.AlignRight | Qt.AlignVCenter)

            else:
                self.create_and_set_table_item(row, group_column_index, group_code, FloatTableWidgetItem,
                                               Qt.AlignRight | Qt.AlignVCenter)
                self.group_codes[row] = group_code

            description = item_df['B1_DESC'].iloc[0]
            self.create_and_set_table_item(row, description_column_index, description, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)

        try:
            # Attempt to access the group code for the given row
            if self.group_codes[row]:
                quant = self.ui.budget_table.item(row, self.column_indices["Quantidade"])
                if quant is not None:
                    # Set the item to be editable
                    quant.setFlags(quant.flags() | Qt.ItemIsEditable)
        except KeyError:
            pass

    def update_quantity(self, quantity_df, row):
        quantity_column_index = self.column_indices["Quantidade disponível"]
        if quantity_df is None or quantity_df.empty:
            quantity = "-"
            self.create_and_set_table_item(row, quantity_column_index, quantity, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)
        else:
            quantity = quantity_df['quantidade'].iloc[0]
            self.create_and_set_table_item(row, quantity_column_index, quantity, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)

    def update_cost(self, cost_df, row):
        cost_column_index = self.column_indices["Custo"]
        if cost_df is None or cost_df.empty:
            cost = "-"
            # Create and place TableItem
            self.create_and_set_table_item(row, cost_column_index, cost, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)
        else:
            cost_value = cost_df['Average'].iloc[0]
            # Create and place TableItem
            self.create_and_set_table_item(row, cost_column_index, cost_value, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)

    def update_general_sale(self, general_df, row):
        general_sale_column_index = self.column_indices["U.V. Geral"]
        if general_df is None or general_df.empty:
            general_sale = "-"
            self.create_and_set_table_item(row, general_sale_column_index, general_sale, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)
        else:
            sale_value = general_df['ValorUnitario'].iloc[0]
            self.create_and_set_table_item(row, general_sale_column_index, sale_value, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)

    def update_client_sale(self, client_sale_df, row):
        client_sale_column_index = self.column_indices["U.V. Cliente"]
        if client_sale_df is None or client_sale_df.empty:
            client_sale = "-"
            self.create_and_set_table_item(row, client_sale_column_index, client_sale, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)
        else:
            client_sale_value = client_sale_df['ValorUnitario'].iloc[0]
            self.create_and_set_table_item(row, client_sale_column_index, client_sale_value, FloatTableWidgetItem,
                                           Qt.AlignRight | Qt.AlignVCenter)

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
                cell_value_float = float(cell_item.data(Qt.EditRole))
                # Find the appropriate factor
                factor = next((factor for limit, factor in limits_factors if cell_value_float <= limit), None)
                if factor is not None:
                    result = cell_value_float * factor
                    self.create_and_set_table_item(row, unit_price_column_index, result, FloatTableWidgetItem,
                                                   Qt.AlignRight | Qt.AlignVCenter)
                else:
                    logger.error("No matching factor found")
            except ValueError:
                logger.error("The cell value is not a valid float number")
        else:
            logger.error("No item in specified cell")
