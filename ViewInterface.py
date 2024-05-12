from abc import ABC, abstractmethod

class ViewInterface(ABC):

    # Returns True on success, False on failed
    @abstractmethod
    def create(self) -> bool:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

