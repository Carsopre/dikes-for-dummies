import logging
from pathlib import Path


class DikesForDummiesLogger:
    def __init__(self):
        _logger = logging.getLogger("")
        _logger.setLevel(logging.DEBUG)

        # Defining our custom formatter
        _formatter = logging.Formatter(
            fmt="%(asctime)s - [%(filename)s:%(lineno)d] - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %I:%M:%S %p",
        )

        # Adding a console handler
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(logging.INFO)
        _console_handler.setFormatter(_formatter)
        _logger.addHandler(_console_handler)

        # Adding a file handler.
        _log_file = Path(__file__).parent / "dikes_for_dummies.log"
        _file_handler = logging.FileHandler(filename=_log_file, mode="w")
        _file_handler.setLevel(logging.INFO)
        _file_handler.setFormatter(_formatter)
        _logger.addHandler(_file_handler)
