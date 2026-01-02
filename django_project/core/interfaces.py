from abc import ABC, abstractmethod

class IObserver:
    """Interface for notification receivers (implemented by the User)."""
    @abstractmethod
    def update(self, message: str):
        pass

class ISubscriptionStrategy(ABC):
    """Interface for subscription pricing and permission calculation."""
    @abstractmethod
    def calculate_price(self, base_price: float) -> float:
        pass

    @abstractmethod
    def get_permissions(self) -> list:
        pass

class IPublication:
    """Interface for any type of publication product (Article, BreakingNews)."""
    @abstractmethod
    def publish(self):
        pass

    @abstractmethod
    def archive(self):
        pass