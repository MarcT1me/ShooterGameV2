from dataclasses import dataclass

import Engine


@dataclass
class Error(Exception):
    exc: Exception
    time_stamp: float
    category: 'Engine.error.ErrorCategory'
    level: 'Engine.error.ErrorLevel'
