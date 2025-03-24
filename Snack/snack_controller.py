from snack_model import PaymentType, InventoryModel, OrderModel

class KioskController:
    def __init__(self, inventory_model, order_model, view):
        self.inventory_model = inventory_model
        self.order_model = order_model
        self.view = view

    def run(self):
        while True:
            self.view.show_menu()
            choice = self.view.get_menu_choice()

            if choice == "1":
                self.place_order()
            elif choice == "2":
                self.view_statistics()
            elif choice == "3":
                self.check_inventory()
            elif choice == "4":
                self.view.show_message("До свидания!")
                break
            else:
                self.view.show_message("Неверный выбор. Попробуйте еще раз.")

    def place_order(self):
        hot_dogs = []
        while True:
            self.view.show_order_menu()
            recipe_choice = self.view.get_order_choice()

            if recipe_choice == "1":
                hot_dog = self.choose_standard_recipe()
                if hot_dog:
                    hot_dogs.append(hot_dog)
            elif recipe_choice == "2":
                hot_dog = self.create_custom_recipe()
                if hot_dog:
                    hot_dogs.append(hot_dog)
            elif recipe_choice == "3":
                continue
            elif recipe_choice == "4":
                break
            else:
                self.view.show_message("Неверный выбор. Попробуйте еще раз.")

        if hot_dogs:
            payment_type_str = self.view.get_payment_type()
            try:
                payment_type = PaymentType[payment_type_str]
            except KeyError:
                self.view.show_message("Неверный способ оплаты.")
                return

            total_price = sum([hd.calculate_price() for hd in hot_dogs])
            discount = self.order_model.apply_discount(len(hot_dogs), total_price)
            final_price = total_price - discount
            # Сохраняем заказ
            order_data = {
                "hot_dogs": [str(hd) for hd in hot_dogs],
                "total_price": total_price,
                "discount": discount,
                "final_price": final_price,
                "payment_type": payment_type.value,
                "bun": hot_dogs[0].bun if hot_dogs else None,
                "sausage": hot_dogs[0].sausage if hot_dogs else None
            }

            self.order_model.add_order(order_data)

            # Обновляем инвентарь (вычитаем использованные ингредиенты)
            for hot_dog in hot_dogs:
                self.update_inventory(hot_dog)

            self.view.show_final_price(final_price)
        else:
            self.view.show_message("Заказ отменен.")

    def choose_standard_recipe(self):
        # Здесь нужно предложить пользователю выбрать из стандартных рецептов
        # и создать HotDog на основе выбранного рецепта.
        # Например, можно предложить меню с номерами рецептов.
        # Важно проверить наличие ингредиентов перед созданием хот-дога.
        self.view.show_message("В разработке...")
        return None

    def create_custom_recipe(self):
        # Здесь нужно дать пользователю возможность выбрать булку, сосиску,
        # соусы и топпинги из доступных.  Также нужно проверять наличие.
        self.view.show_message("В разработке...")
        return None

    def view_statistics(self):
        stats = self.order_model.get_sales_statistics()
        self.view.show_statistics(stats)

    def check_inventory(self):
        low_stock_items = self.inventory_model.get_low_stock_items()
        self.view.show_low_stock(low_stock_items)

    def update_inventory(self, hot_dog):
        self.inventory_model.update_inventory(hot_dog.bun, -1)
        self.inventory_model.update_inventory(hot_dog.sausage, -1)
        for sauce in hot_dog.sauces:
            self.inventory_model.update_inventory(sauce, -1)
        for topping in hot_dog.toppings:
            self.inventory_model.update_inventory(topping, -1)
