import logging
import pandas as pd
from database.basic_functions import database_query
from database.queries import orders_six_months, cost_based_on_stock

logger = logging.getLogger(__name__)


def process_table_info(query_func, *args):
    """
    General function to process data based on a query.

    Parameters:
    query_func: Function to generate the query.
    *args: Arguments to be passed to the query_func.
    """
    try:
        query = query_func(*args)
        result_df = database_query(query)

        if query_func == cost_based_on_stock:
            if not result_df.empty and 'Average' in result_df.columns:
                quant_value = result_df['Average'].iloc[0]
                if quant_value is None:
                    logger.info("Average value is None, running orders_six_months query.")
                    query = orders_six_months(*args)
                    result_df = database_query(query)
            else:
                logger.warning("DataFrame is empty or 'Average' column is missing.")
        else:
            logger.info(f"Running query for {query_func.__name__}.")

        return result_df

    except Exception as e:
        logger.error(f"Error processing table information: {e}")
        # Depending on your use case, you might want to re-raise the exception or return an empty DataFrame, etc.
        raise
