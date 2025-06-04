from typing import Any, Optional, final
from abc import ABC, abstractmethod
from pathlib import Path

import Engine


class AssetLoader(ABC):
    """ asset factory for the selected asset type """

    @abstractmethod
    def load(
            self, asset_file: 'Engine.assets.AssetFileData'
    ) -> Any:
        """ The logic of loading data from a file """

    @abstractmethod
    def create(
            self, asset_file: 'Engine.assets.AssetFileData', dependencies: 'Optional[list[Engine.assets.AssetData]]',
            content: Any
    ) -> 'Engine.assets.AssetData':
        """ The logic of processing previously uploaded data """

    @staticmethod
    @final
    def __read_text_file__(path: Path):
        """ reading text data from file """
        return path.open(mode="r").read()

    @staticmethod
    @final
    def __read_binary_file__(path: Path):
        """ reading binary data from file """
        return path.open(mode="br").read()
