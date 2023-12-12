import logging
import os
import pandas as pd
from database.basic_functions import database_query
from database.queries import client_name

logger = logging.getLogger(__name__)


def search_function(user_search):
    logger.info("search_function starting.")

    query = client_name(user_search)
    data_frame = database_query(query)

    if not data_frame.empty:
        client = data_frame.iloc[0]['A1_NOME']
        return client
    else:
        logger.error("An error occurred during the search_function")
        return "Cliente"
