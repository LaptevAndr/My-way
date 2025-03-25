from snack_controller import KioskController
from snack_model import InventoryModel, Bun, Sausage, Sauce, Topping, BulkDiscount, OrderModel
from snack_view import KioskView
import os

print(f"Текущая рабочая директория: {os.getcwd()}")

if __name__ == "__main__":
    # Инициализация моделей
    inventory_model = InventoryModel()

    if not inventory_model.inventory["buns"]:
        inventory_model.inventory["buns"]["обычная"] = Bun("обычная", 100, 5)
    if not inventory_model.inventory["sausages"]:
        inventory_model.inventory["sausages"]["говяжья"] = Sausage("говяжья", 50, 20)
    if not inventory_model.inventory["sauces"]:
        inventory_model.inventory["sauces"]["кетчуп"] = Sauce("кетчуп", 50, 3)
    if not inventory_model.inventory["toppings"]:
        inventory_model.inventory["toppings"]["лук"] = Topping("лук", 50, 2)

    inventory_model.save_inventory()

    bulk_discount = BulkDiscount(threshold=3, discount_percentage=10)
    order_model = OrderModel(discount_strategy=bulk_discount)

    # Инициализация View и Controller
    view = KioskView()
    controller = KioskController(inventory_model, order_model, view)

    # Запуск приложения
    controller.run()