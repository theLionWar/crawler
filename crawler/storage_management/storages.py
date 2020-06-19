import json
from abc import ABC, abstractmethod
from tinydb import TinyDB
import os


class StorageManager(ABC):

    @abstractmethod
    def create(self, item: dict):
        pass

    @abstractmethod
    def truncate(self):
        pass

    @abstractmethod
    def getall(self) -> dict:
        pass


class FileStorageManager(StorageManager):

    def __init__(self, file_name: str = 'data/default.txt'):
        # creates a file if it doesn't exist
        if not os.path.exists(file_name):
            open(file_name, 'w').close()
        self.file_name = file_name

    def create(self, item: dict):
        f = open(self.file_name, 'a+')
        f.write(json.dumps(item))
        f.close()

    def truncate(self):
        open(self.file_name, 'w').close()

    def getall(self) -> dict:
        f = open(self.file_name, 'r')
        all_items = f.read()
        f.close()
        return json.loads(all_items)


class TinydbStorageManager(StorageManager):

    def __init__(self, db_name: str = 'data/default.json'):
        self.db = TinyDB(db_name)

    def create(self, item: dict):
        self.db.insert(item)

    def truncate(self):
        return self.db.truncate()

    def getall(self) -> dict:
        return self.db.all()
