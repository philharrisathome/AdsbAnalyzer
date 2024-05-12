from abc import ABC, abstractmethod

class ReceiverInterface(ABC):

    # Returns True on success, False on failed
    @abstractmethod
    def open(self) -> bool:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    # Returns complete messages only as list[str], or []
    @abstractmethod
    def getMessages(self) -> list[str]:
        pass

