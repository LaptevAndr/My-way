from abc import ABC, abstractmethod

class CalculationDelivery(ABC):
    @abstractmethod
    def deliver_calculation(self, calculation: float) -> float:
        """Calculates the total cost with delivery."""
        pass

class RegularDelivery(CalculationDelivery):
    def deliver_calculation(self, calculation: float) -> float:
        return calculation + 0.10 * calculation

class ExpressDelivery(CalculationDelivery):
    def deliver_calculation(self, calculation: float) -> float:
        return calculation + 0.30 * calculation

class Pickup(CalculationDelivery):
    def deliver_calculation(self, calculation: float) -> float:
        return calculation

class Order:
    def __init__(self, calculation: float, calculation_delivery: CalculationDelivery):
        self.calculation = calculation
        self.calculation_delivery = calculation_delivery

    def calculate_total(self) -> float:
        return self.calculation_delivery.deliver_calculation(self.calculation)

# Test

regular_delivery = RegularDelivery()
express_delivery = ExpressDelivery()
pickup_delivery = Pickup()

order1 = Order(1000.0, regular_delivery)
order2 = Order(1200.0, express_delivery)
order3 = Order(1400.0, pickup_delivery)

print(f"Total for order1: {order1.calculate_total()}")
print(f"Total for order2: {order2.calculate_total()}")
print(f"Total for order3: {order3.calculate_total()}")