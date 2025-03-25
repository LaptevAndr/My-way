from snack_model import PaymentType, InventoryModel, OrderModel, HotDog, ClassicHotDogRecipe, SpicyHotDogRecipe

class KioskController:
    def __init__(self, inventory_model, order_model, view):
        self.inventory_model = inventory_model
        self.order_model = order_model
        self.view = view
        self.standard_recipes = {
            "1": {"name": "Классический", "description": "Булка, говяжья сосиска, кетчуп, горчица"},
            "2": {"name": "Острый", "description": "Булка, говяжья сосиска, острый соус, халапеньо"},
            "3": {"name": "Простой", "description": "Булка, говяжья сосиска, без добавок"}
        }

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
                    self.view.show_message(f"Добавлен хот-дог: {hot_dog}")
            elif recipe_choice == "2":
                hot_dog = self.create_custom_recipe()
                if hot_dog:
                    hot_dogs.append(hot_dog)
                    self.view.show_message(f"Добавлен хот-дог: {hot_dog}")
            elif recipe_choice == "3":
                if not hot_dogs:
                    self.view.show_message("Сначала добавьте хотя бы один хот-дог!")
                continue
            elif recipe_choice == "4":
                break
            else:
                self.view.show_message("Неверный выбор. Попробуйте еще раз.")

        if hot_dogs:
            while True:
                payment_type_str = self.view.get_payment_type()
                try:
                    payment_type = PaymentType[payment_type_str.upper()]
                    break
                except KeyError:
                    self.view.show_message("Неверный способ оплаты. Доступные варианты: наличные, карта")

            total_price = sum([hd.calculate_price() for hd in hot_dogs])
            discount = self.order_model.apply_discount(len(hot_dogs), total_price)
            final_price = total_price - discount

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

            for hot_dog in hot_dogs:
                self.update_inventory(hot_dog)

            self.view.show_message("\n--- Итог заказа ---")
            for i, hd in enumerate(hot_dogs, 1):
                self.view.show_message(f"{i}. {hd}")
            self.view.show_message(f"\nСкидка: {discount}")
            self.view.show_final_price(final_price)
            self.view.show_message(f"Способ оплаты: {payment_type.value}")
        else:
            self.view.show_message("Заказ отменен.")

    def choose_standard_recipe(self):
        self.view.show_message("\nДоступные стандартные рецепты:")
        for num, recipe in self.standard_recipes.items():
            self.view.show_message(f"{num}. {recipe['name']} - {recipe['description']}")

        while True:
            choice = input("Выберите рецепт (или 'отмена' для отмены): ")
            if choice.lower() == 'отмена':
                return None
            if choice in self.standard_recipes:
                break
            self.view.show_message("Неверный выбор. Попробуйте еще раз.")

        try:
            if choice == "1":  # Классический
                bun = self.inventory_model.get_ingredient("buns", "обычная")
                sausage = self.inventory_model.get_ingredient("sausages", "говяжья")
                ketchup = self.inventory_model.get_ingredient("sauces", "кетчуп")
                mustard = self.inventory_model.get_ingredient("sauces", "горчица")

                if not all([bun, sausage, ketchup, mustard]):
                    self.view.show_message("Не хватает ингредиентов для этого рецепта")
                    return None

                recipe = ClassicHotDogRecipe(bun, sausage, ketchup, mustard)
                return recipe.create_hot_dog()

            elif choice == "2":  # Острый
                bun = self.inventory_model.get_ingredient("buns", "обычная")
                sausage = self.inventory_model.get_ingredient("sausages", "говяжья")
                spicy_sauce = self.inventory_model.get_ingredient("sauces", "острый")
                jalapeno = self.inventory_model.get_ingredient("toppings", "халапеньо")

                if not all([bun, sausage, spicy_sauce, jalapeno]):
                    self.view.show_message("Не хватает ингредиентов для этого рецепта")
                    return None

                recipe = SpicyHotDogRecipe(bun, sausage, spicy_sauce, jalapeno)
                return recipe.create_hot_dog()

            elif choice == "3":  # Простой
                bun = self.inventory_model.get_ingredient("buns", "обычная")
                sausage = self.inventory_model.get_ingredient("sausages", "говяжья")

                if not all([bun, sausage]):
                    self.view.show_message("Не хватает ингредиентов для этого рецепта")
                    return None

                return HotDog(bun, sausage)

        except Exception as e:
            self.view.show_message(f"Ошибка при создании хот-дога: {e}")
            return None

    def create_custom_recipe(self):
        self.view.show_message("\nСоздание собственного рецепта:")

        # Выбор булки
        buns = self.inventory_model.inventory["buns"]
        self.view.show_message("\nДоступные булки:")
        for i, (name, bun) in enumerate(buns.items(), 1):
            self.view.show_message(f"{i}. {name} - {bun.cost_per_unit} руб. (осталось: {bun.quantity})")

        bun_choice = input("Выберите булку (номер): ")
        try:
            bun_name = list(buns.keys())[int(bun_choice)-1]
            bun = buns[bun_name]
        except (ValueError, IndexError):
            self.view.show_message("Неверный выбор булки")
            return None

        # Выбор сосиски
        sausages = self.inventory_model.inventory["sausages"]
        self.view.show_message("\nДоступные сосиски:")
        for i, (name, sausage) in enumerate(sausages.items(), 1):
            self.view.show_message(f"{i}. {name} - {sausage.cost_per_unit} руб. (осталось: {sausage.quantity})")

        sausage_choice = input("Выберите сосиску (номер): ")
        try:
            sausage_name = list(sausages.keys())[int(sausage_choice)-1]
            sausage = sausages[sausage_name]
        except (ValueError, IndexError):
            self.view.show_message("Неверный выбор сосиски")
            return None

        # Выбор соусов
        sauces = []
        available_sauces = self.inventory_model.inventory["sauces"]
        if available_sauces:
            self.view.show_message("\nДоступные соусы (можно выбрать несколько через запятую):")
            for i, (name, sauce) in enumerate(available_sauces.items(), 1):
                self.view.show_message(f"{i}. {name} - {sauce.cost_per_unit} руб. (осталось: {sauce.quantity})")

            sauce_choices = input("Выберите соусы (номера через запятую или 0 чтобы пропустить): ")
            if sauce_choices != "0":
                for choice in sauce_choices.split(','):
                    try:
                        sauce_name = list(available_sauces.keys())[int(choice.strip())-1]
                        sauces.append(available_sauces[sauce_name])
                    except (ValueError, IndexError):
                        self.view.show_message(f"Пропущен неверный выбор соуса: {choice}")

        # Выбор топпингов
        toppings = []
        available_toppings = self.inventory_model.inventory["toppings"]
        if available_toppings:
            self.view.show_message("\nДоступные топпинги (можно выбрать несколько через запятую):")
            for i, (name, topping) in enumerate(available_toppings.items(), 1):
                self.view.show_message(f"{i}. {name} - {topping.cost_per_unit} руб. (осталось: {topping.quantity})")

            topping_choices = input("Выберите топпинги (номера через запятую или 0 чтобы пропустить): ")
            if topping_choices != "0":
                for choice in topping_choices.split(','):
                    try:
                        topping_name = list(available_toppings.keys())[int(choice.strip())-1]
                        toppings.append(available_toppings[topping_name])
                    except (ValueError, IndexError):
                        self.view.show_message(f"Пропущен неверный выбор топпинга: {choice}")

        return HotDog(bun, sausage, sauces, toppings)

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