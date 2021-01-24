
from atlas.config import get_default

from atlas.core import Scheduler, MultiScheduler
from atlas.conditions import AlwaysFalse
from atlas.parse import parse_condition
from atlas.log import CsvHandler

from textwrap import dedent

import sys
import logging

def test_logger():
    get_default("csv_logging")
    loggers = {name: logging.getLogger(name) for name in logging.root.manager.loggerDict}

    # Some of the atlas.task handlers must have two way logger (ability to read log file)
    assert any(hasattr(handler, "read") for handler in loggers["atlas.task"].handlers)
