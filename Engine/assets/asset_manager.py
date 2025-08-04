from typing_extensions import Optional, Iterable, Dict, Set, Any, List, final
from pprint import pformat

from loguru import logger

import Engine


@final
class DependencyResolver:
    def __init__(self, loading_func):
        self.loading_func = loading_func
        self._loading_stack: Set[str] = set()

    def resolve(self, asset_file: 'Engine.assets.AssetFileData') -> 'List[Engine.assets.AssetData]':
        """
        Retrieves the list of downloaded dependencies for the specified cassette
        with loop handling and caching
        """
        dependencies: List[Engine.assets.AssetData] = []

        if asset_file.dependencies is None:
            return dependencies
        else:
            logger.info(f"DependencyResolver - loading dependencies for {asset_file.name}\n")
            cache_key = str(asset_file.path)

            # Checking cycles
            if cache_key in self._loading_stack:
                raise Exception(
                    f"Cyclic dependency detected: {asset_file.path}"
                )

            self._loading_stack.add(cache_key)

            try:
                # Recursively loading all dependencies
                dependencies = [self.loading_func(dep) for dep in asset_file.dependencies]
            except Exception as e:
                raise Exception(f"Failed to load asset {asset_file.path}") from e
            finally:
                self._loading_stack.remove(cache_key)

            logger.success(
                f"DependencyResolver - Dependencies for {asset_file.name} loaded:\n"
                f"deps:\n"
                f"{pformat(dependencies)}\n"
            )

        return dependencies


@final
class AssetManager:
    def __init__(self, asset_types: 'Iterable[Engine.assets.AssetType]'):
        # Initializing the root Roster
        self.storage: dict[str, dict[str, Engine.assets.AssetData]] = {}
        self._dependency_resolver = DependencyResolver(self.load)

        # Registering asset types as branches in the Roster
        self._register_asset_type(asset_types)

        logger.success("AssetManager - init")

    def __getitem__(self, path: str) -> 'Optional[Engine.assets.AssetData]':
        category, name = path.split('/')

        branch = self.storage.get(category)

        if branch is None: return

        return branch.get(name)

    def _register_asset_type(self, asset_types: 'Iterable[Engine.assets.AssetType]'):
        already_registered_asset_types: Dict[str, Engine.assets.AssetLoader] = {}

        for asset_type in asset_types:
            name = asset_type.type_name
            if name in already_registered_asset_types:
                raise Exception(f"Asset type '{name}' already registered")

            logger.info(
                f"Register asset type:\n"
                f"loader: {asset_type.asset_loader}\n"
                f"type {asset_type.type_name}"
            )

            # Creating a new branch in the Roster
            self.storage[name] = {"__loader__": asset_type.asset_loader}

            # Saving the config for quick access
            already_registered_asset_types[name] = asset_type

    def load(
            self, asset_file: 'Engine.assets.AssetFileData', *,
            loaded_dependencies: 'list[Engine.assets.AssetData]' = []
    ) -> 'Engine.assets.AssetData':
        try:
            logger.info(
                f"AssetManager - Loading asset:\n"
                f"id: {asset_file.name}" + str(
                    f"\npath: {asset_file.path}" if asset_file.path else ""
                ) + str(
                    f"\ndeps: \n{pformat(asset_file.dependencies)}\n" if asset_file.dependencies else ""
                )
            )
            # Dependency Resolution
            dependencies: list[Engine.assets.AssetData] = self._dependency_resolver.resolve(asset_file)

            # We get the corresponding branch
            branch: dict = self.storage[asset_file.type_name]

            # Uploading content
            loader: Engine.assets.AssetLoader = branch["__loader__"]
            content: Any = loader.load(asset_file)

            # Creating an asset object_node
            dependencies.extend(loaded_dependencies)

            asset_data = loader.create(
                asset_file=asset_file,
                dependencies=dependencies,
                content=content
            )

            # Saving to the appropriate branch
            branch[asset_data.name] = asset_data

            logger.success(f"AssetManager - Asset {asset_file.name} loaded\n")
            return asset_data

        except KeyError as e:
            raise Exception(f"Unregistered type: {asset_file.type_name}") from e
