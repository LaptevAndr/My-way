import abc
import json
from enum import Enum

class Ingredient(abc.ABC):
    def __init__(self, name, quantity, cost_per_unit):
        self.name = name
        self.quantity = quantity
        self.cost_per_unit = cost_per_unit

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', quantity={self.quantity}, cost_per_unit={self.cost_per_unit})"

class Bun(Ingredient):
    def __init__(self, name, quantity, cost_per_unit):
        super().__init__(name, quantity, cost_per_unit)

class Sausage(Ingredient):
    def __init__(self, name, quantity, cost_per_unit):
        super().__init__(name, quantity, cost_per_unit)

class Sauce(Ingredient):
    def __init__(self, name, quantity, cost_per_unit):
        super().__init__(name, quantity, cost_per_unit)

class Topping(Ingredient):
    def __init__(self, name, quantity, cost_per_unit):
        super().__init__(name, quantity, cost_per_unit)

class HotDog:
    def __init__(self, bun, sausage, sauces=None, toppings=None):
        self.bun = bun
        self.sausage = sausage
        self.sauces = sauces if sauces else []
        self.toppings = toppings if toppings else []

    def calculate_price(self):
        price = self.bun.cost_per_unit + self.sausage.cost_per_unit
        for sauce in self.sauces:
            price += sauce.cost_per_unit
        for topping in self.toppings:
            price += topping.cost_per_unit
        return price

    def __str__(self):
        sauce_str = ", ".join([sauce.name for sauce in self.sauces])
        topping_str = ", ".join([topping.name for topping in self.toppings])
        return f"Хот-дог: Булка - {self.bun.name}, Сосиска - {self.sausage.name}, Соусы - {sauce_str or 'нет'}, Топпинги - {topping_str or 'нет'}"

class Recipe(abc.ABC):  # Интерфейс для рецептов
    @abc.abstractmethod
    def create_hot_dog(self):
        pass
class StandardHotDog(Recipe):
    def __init__(self, bun, sausage, sauces, toppings):
        self.bun = bun
        self.sausage = sausage
        self.sauces = sauces
        self.toppings = toppings
    def create_hot_dog(self):
         return HotDog(self.bun, self.sausage, self.sauces, self.toppings)
#Исправлен!
class ClassicHotDogRecipe(Recipe):
    def __init__(self, bun, sausage, ketchup, mustard):
        self.bun = bun
        self.sausage = sausage
        self.ketchup = ketchup
        self.mustard = mustard

    def create_hot_dog(self):
      # Создаем список соусов
        sauces = [self.ketchup, self.mustard]

        # Создаем объект HotDog с булочкой, сосиской и соусами
        hot_dog = HotDog(self.bun, self.sausage, sauces=sauces)
        return hot_dog
    
class SpicyHotDogRecipe(Recipe):
    def __init__(self, bun, sausage, spicy_sauce, jalapenos):
        self.bun = bun
        self.sausage = sausage
        self.spicy_sauce = spicy_sauce
        self.jalapenos = jalapenos

    def create_hot_dog(self):
        return HotDog(self.bun, self.sausage, sauces=[self.spicy_sauce], toppings=[self.jalapenos])
class CustomHotDog(Recipe):
    def __init__(self, bun, sausage, sauces, toppings):
        self.bun = bun
        self.sausage = sausage
        self.sauces = sauces
        self.toppings = toppings
    def create_hot_dog(self):
         return HotDog(self.bun, self.sausage, self.sauces, self.toppings)

class PaymentType(Enum):
    CASH = "Наличные"
    CARD = "Карта"
    
class InventoryModel:  # Управление данными инвентаря
    def __init__(self, inventory_file="inventory.json"):
        self.inventory_file = inventory_file
        self.inventory = self.load_inventory(inventory_file)

    def load_inventory(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                inventory = {}
                for item_type, items in data.items():
                    inventory[item_type] = {}
                    for item_name, details in items.items():
                        if item_type == "buns":
                            inventory[item_type][item_name] = Bun(item_name, details["quantity"], details["cost_per_unit"])
                        elif item_type == "sausages":
                            inventory[item_type][item_name] = Sausage(item_name, details["quantity"], details["cost_per_unit"])
                        elif item_type == "sauces":
                            inventory[item_type][item_name] = Sauce(item_name, details["quantity"], details["cost_per_unit"])
                        elif item_type == "toppings":
                            inventory[item_type][item_name] = Topping(item_name, details["quantity"], details["cost_per_unit"])
                return inventory
        except FileNotFoundError:
            print("Файл инвентаря не найден. Создается новый.")
            return {
                "buns": {},
                "sausages": {},
                "sauces": {},
                "toppings": {}
            }

    def save_inventory(self):
        with open(self.inventory_file, 'w') as f:
            data = {}
            for item_type, items in self.inventory.items():
                data[item_type] = {}
                for item_name, item in items.items():
                    data[item_type][item_name] = {
                        "quantity": item.quantity,
                        "cost_per_unit": item.cost_per_unit
                    }
            json.dump(data, f, indent=4)

    def get_ingredient(self, ingredient_type, ingredient_name):
        if ingredient_type in self.inventory and ingredient_name in self.inventory[ingredient_type]:
            return self.inventory[ingredient_type][ingredient_name]
        return None

    def check_availability(self, ingredient, quantity=1):
        ingredient_type = ingredient.__class__.__name__.lower() + "s"
        if ingredient.name in self.inventory[ingredient_type] and self.inventory[ingredient_type][ingredient.name].quantity >= quantity:
            return True
        return False

    def update_inventory(self, ingredient, quantity_change):
        ingredient_type = ingredient.__class__.__name__.lower() + "s"
        if ingredient.name in self.inventory[ingredient_type]:
            self.inventory[ingredient_type][ingredient.name].quantity += quantity_change
            self.save_inventory()
        else:
            print(f"Ингредиент {ingredient.name} не найден в инвентаре.")

    def get_low_stock_items(self, threshold=5):
        low_stock = []
        for item_type, items in self.inventory.items():
            for item_name, item in items.items():
                if item.quantity <= threshold:
                    low_stock.append(item)
        return low_stock

class OrderModel:  # Управление данными заказов
    def __init__(self, discount_strategy=None, order_file="orders.json"):
        self.orders = []
        self.total_revenue = 0.0
        self.total_cost = 0.0
        self.discount_strategy = discount_strategy
        self.order_file = order_file
        self.load_orders(order_file)

    def load_orders(self, file_path):
        try:
            with open(file_path, 'r') as f:
                self.orders = json.load(f)
        except FileNotFoundError:
            print("Файл заказов не найден. Создается новый.")
            self.orders = []

    def save_orders(self):
        with open(self.order_file, 'w') as f:
            json.dump(self.orders, f, indent=4)

    def apply_discount(self, quantity, total_price):
        if self.discount_strategy:
            return self.discount_strategy.apply_discount(quantity, total_price)
        return 0.0

    def calculate_cost(self, hot_dog):
        cost = hot_dog.bun.cost_per_unit + hot_dog.sausage.cost_per_unit
        for sauce in hot_dog.sauces:
            cost += sauce.cost_per_unit
        for topping in hot_dog.toppings:
            cost += topping.cost_per_unit
        return cost

    def get_sales_statistics(self):
        profit = self.total_revenue - self.total_cost
        return {
            "total_hot_dogs_sold": len(self.orders),
            "total_revenue": self.total_revenue,
            "profit": profit
        }

    def add_order(self, order_data):
        self.orders.append(order_data)
        self.save_orders()
        self.total_revenue += order_data["final_price"]
        self.total_cost += sum([self.calculate_cost(HotDog(order_data["bun"], order_data["sausage"])) for hot_dog in order_data["hot_dogs"]])

class DiscountStrategy(abc.ABC): # Интерфейс для скидок (Strategy)
    @abc.abstractmethod
    def apply_discount(self, quantity, total_price):
        pass

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold, discount_percentage):
        self.threshold = threshold
        self.discount_percentage = discount_percentage

    def apply_discount(self, quantity, total_price):
        if quantity >= self.threshold:
            return total_price * (self.discount_percentage / 100)
        return 0.0

