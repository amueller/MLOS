#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
import logging
import time


class BufferingHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.buffered_log_records = []
        self.level = None

    def setLevel(self, level):
        self.level = level

    def set_level_by_name(self, new_level_name):
        try:
            self.level = logging._nameToLevel[new_level_name] # pylint: disable=protected-access
        except:
            pass

    def emit(self, record):
        if self.level <= record.levelno:
            event = {
                'timestamp': record.asctime,
                'level': record.levelname,
                'filename': record.filename,
                'line': record.lineno,
                'function': record.funcName,
                'message': record.message.replace("'", '"'),
                'exception_text': record.exc_text.replace("'", '"') if record.exc_text is not None else None
            }
            self.buffered_log_records.append(event)

    def get_records(self, clear_buffer=False):
        records = self.buffered_log_records
        if clear_buffer:
            self.buffered_log_records = []
        return records


def create_logger(logger_name, create_console_handler=True, create_file_handler=False, create_buffering_handler=False, logging_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    logger.propagate = False
    formatter = logging.Formatter('%(asctime)s - %(name)26s - %(levelname)7s - [%(filename)20s:%(lineno)4s - %(funcName)25s() ] %(message)s')
    formatter.converter = time.gmtime
    formatter.datefmt = '%m/%d/%Y %H:%M:%S'

    if create_console_handler:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    if create_file_handler:
        file_handler = logging.FileHandler(logger_name + ".log")
        file_handler.setLevel(logging_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    buffering_handler = None
    if create_buffering_handler:
        buffering_handler = BufferingHandler()
        buffering_handler.setLevel(logging_level)
        buffering_handler.setFormatter(formatter)
        logger.addHandler(buffering_handler)

    # TODO: Fix this, as sometimes we are returning a tuple + logger and sometimes just the logger.
    if create_buffering_handler:
        return logger, buffering_handler

    return logger
