
from uuid import uuid4

class Purchase:
    def __init__(self, name: str, amount: float, commission_rate: float, id: str = None):
        self.id = id or str(uuid4())
        self.name = name
        self.amount = amount
        self.commission_rate = commission_rate
        self.commission = self.calculate_commission()

    def calculate_commission(self) -> float:
        return self.amount * (self.commission_rate / 100)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "commission_rate": self.commission_rate,
            "commission": self.commission,
        }