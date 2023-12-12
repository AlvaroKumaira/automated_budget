import logging
import os
from PyQt5.QtWidgets import QApplication
from interface.ui import MainWindow

# Set up logging config for the entire application.
logging.basicConfig(filename='info.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )


def main():
    """
    Entry point for the application.

    This function initializes the MainWindow and starts the PyQt event loop.
    Any unexpected errors during this process are logged and then raised.
    """
    try:
        # Create a PyQt application instance.
        app = QApplication([])

        # Create a MainWindow
        window = MainWindow()
        window.show()

        app.exec_()

    except Exception as e:
        logging.error(f"An unexpected error occurred while creating the window: {e}")


if __name__ == '__main__':
    main()
