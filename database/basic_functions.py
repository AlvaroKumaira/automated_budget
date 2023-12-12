import pandas as pd
import logging
import os
import datetime
from .db_class import Database, config


# Get the logger
logger = logging.getLogger(__name__)


def database_query(query, params=None):
    """
        Retreives data from the database using a specified SQL query. Can be used with or without params.

        Parameters:
        - query (str): SQL query to execute.
        - params (dict, optional): Parameter for the SQL query.

        Returns:
        - DataFrame: DataFrame containing the results or None if an error occurred.
        """
    # Create an instante of the Database class and establish a connection.
    db_instance = Database(db_config=config)
    db = db_instance.connect()

    try:
        # Execute the SQL query and store the result in a DataFrame.
        if params:
            data_frame = pd.read_sql(query, db, params=params)
        else:
            data_frame = pd.read_sql(query, db)
        logger.info("database_query function ran successfully")
    except Exception as e:
        logger.error(f"Error when running the database_query function: {e}")
        data_frame = None

    return data_frame


def save_to_excel(data_frame, filename_prefix, other_info, open_file=False):
    """
    Saves a DataFrame to an Excel file on the user's Desktop in a folder named 'Resultado'.

    Parameters:
    - data_frame (DataFrame): The data to save.
    - filename_prefix (str): Prefix for the Excel filename.
    - other_info (str): Additional information for the Excel filename.
    - open_file (bool, optional): If True, the Excel file will be opened. Defaults to False.

    Returns:
    - str: Path to the saved Excel file. If open_file is True, also opens the Excel file.
    """
    # Set up path to the user's desktop
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    # Determine the current date to append into the filename
    current_timestamp = datetime.datetime.now().strftime('%Y%m%d')

    # Define the Excel file path
    excel_file_path = os.path.join(desktop_path, f'{filename_prefix}_{other_info}_{current_timestamp}.xlsx')

    # Save the DataFrame to Excel
    data_frame.to_excel(excel_file_path, index=False)
    logger.info(f"Function save_to_excel ran successfully: {excel_file_path}")

    # If open_file is True, open the Excel file
    if open_file:
        try:
            os.startfile(excel_file_path)
        except Exception as e:
            logger.error(f"The save_to_excel function couldn't open the file: {e}")

    # VER SE PRECISA DISSO MESMO!
    return excel_file_path