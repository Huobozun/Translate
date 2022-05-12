from abc import ABC, abstractmethod
from asyncio.log import logger
import os


class Store(ABC):
    @abstractmethod
    def __init__(self, setting: dict):
        pass

    @abstractmethod
    def save(self, file_name, data, overwite=True) -> str:
        pass

    @abstractmethod
    def append(self, file_name, data) -> str:
        pass

    @abstractmethod
    def clean(self, file_name) -> str:
        pass

    @abstractmethod
    def file_exists(self, file_name) -> bool:
        pass

    @abstractmethod
    def full_path(self, file_name) -> bool:
        pass


class EmptyStore(Store):
    def __init__(self, setting: dict):
        pass

    def save(self, file_name, data, overwite=True) -> str:
        logger.debug(f"save data to {file_name}")
        return ""

    def append(self, file_name, data) -> str:
        logger.debug(f"append data to {file_name}")
        return ""

    def clean(self, file_name) -> str:
        logger.debug(f"clean {file_name} as empty file")
        return ""

    def file_exists(self, file_name) -> bool:
        logger.debug(f"check if {file_name} exist")
        return True

    def full_path(self, file_name) -> str:
        logger.debug(f"get full path of {file_name}")
        return ""


class FileStore(Store):
    def __init__(self, setting: dict):
        self.root_path = setting.get("FILES_STORE", ".")

    def save(self, file_name, data, overwite=True) -> str:
        file_path = os.path.join(self.root_path, file_name)
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data)
        return file_path

    def append(self, file_name, data) -> str:
        file_path = os.path.join(self.root_path, file_name)
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(data)
        return file_path

    def clean(self, file_name) -> str:
        file_path = os.path.join(self.root_path, file_name)
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        if os.path.isfile(file_path):
            os.remove(file_path)
        return file_path

    def file_exists(self, file_name) -> bool:
        file_path = os.path.join(self.root_path, file_name)
        return os.path.isfile(file_path)

    def full_path(self, file_name) -> str:
        return os.path.join(self.root_path, file_name)
