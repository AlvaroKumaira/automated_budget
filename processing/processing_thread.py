from PyQt5.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal
import logging

# Set up logging
logger = logging.getLogger(__name__)


class WorkerSignals(QObject):
    process_started = pyqtSignal()
    process_stopped = pyqtSignal()
    process_result = pyqtSignal(object)


class ProcessingRunnable(QRunnable):
    def __init__(self, function, *args, **kwargs):
        super(ProcessingRunnable, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.function(*self.args, **self.kwargs)
            self.signals.process_result.emit(result)
            logger.info(f"Processing thread successfully executed {self.function.__name__}")
        except Exception as e:
            logger.error(f"Processing thread had an error during execution of {self.function.__name__}: {e}")
        finally:
            self.signals.process_stopped.emit()
