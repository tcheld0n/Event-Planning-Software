# repositories/base_repository.py
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get_by_id(self, obj_id):
        pass

    @abstractmethod
    def list_all(self):
        pass

    @abstractmethod
    def remove(self, obj):
        pass