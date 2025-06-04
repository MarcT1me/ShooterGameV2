from abc import abstractmethod

import Engine
from Engine.error.error import Error


class IErrorHandler:
    error_category: 'Engine.error.ErrorCategory'
    error_level: 'Engine.error.ErrorLevel'

    @abstractmethod
    def on_error(self, err: Error):
        """ Handling failure from catching """
