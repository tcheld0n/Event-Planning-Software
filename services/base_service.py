from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def create(self, *args, **kwargs):
        """Cria um novo objeto"""
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """Atualiza um objeto existente"""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Exclui um objeto identificado por obj_id"""
        pass
