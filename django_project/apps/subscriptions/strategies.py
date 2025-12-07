from core.interfaces import ISubscriptionStrategy

class StudentStrategy(ISubscriptionStrategy):
    """Concrete strategy for calculating student pricing (50% discount)."""
    def calculate_price(self, base_price: float) -> float:
        return base_price * 0.5

    def get_permissions(self) -> list:
        return ["read_news", "view_ads", "comment"]

class CorporateStrategy(ISubscriptionStrategy):
    """Concrete strategy for corporate pricing (price is 0 for the employee)."""
    def calculate_price(self, base_price: float) -> float:
        return 0.0

    def get_permissions(self) -> list:
        return ["read_news", "no_ads", "read_exclusive", "archive"]

class PremiumStrategy(ISubscriptionStrategy):
    """Concrete strategy for standard full-price premium access."""
    def calculate_price(self, base_price: float) -> float:
        return base_price

    def get_permissions(self) -> list:
        return ["read_news", "no_ads", "read_exclusive", "priority_support"]