class KioskView:  # Консольный интерфейс (можно заменить на GUI)
    def show_menu(self):
        print("\n--- Киоск хот-догов ---")
        print("1. Заказать хот-дог")
        print("2. Просмотреть статистику")
        print("3. Проверить запасы")
        print("4. Выход")

    def get_menu_choice(self):
        return input("Выберите действие: ")

    def show_order_menu(self):
        print("\n--- Создание хот-дога ---")
        print("1. Выбрать стандартный рецепт")
        print("2. Создать свой рецепт")
        print("3. Добавить еще хот-дог в заказ")
        print("4. Закончить заказ")

    def get_order_choice(self):
        return input("Выберите действие: ")

    def get_payment_type(self):
        return input("Выберите способ оплаты (наличные/карта): ").upper()

    def show_final_price(self, price):
        print(f"Сумма к оплате: {price}")

    def show_statistics(self, stats):
        print("\n--- Статистика продаж ---")
        print(f"Всего продано хот-догов: {stats['total_hot_dogs_sold']}")
        print(f"Выручка: {stats['total_revenue']}")
        print(f"Прибыль: {stats['profit']}")

    def show_low_stock(self, items):
        if items:
            print("\n--- Требуется пополнение запасов ---")
            for item in items:
                print(f"{item.name}: осталось {item.quantity}")
        else:
            print("Все компоненты в достаточном количестве.")

    def show_message(self, message):
        print(message)