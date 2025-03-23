"""Создайте приложение для эмуляции работа киоска
по продаже хот-догов. Приложение должно иметь следующую функциональность:
1. Пользователь может выбрать из трёх стандартных
рецептов хот-дога или создать свой рецепт.
2. Пользователь может выбирать добавлять ли майонез,
горчицу, кетчуп, топпинги (сладкий лук, халапеньо,
чили, соленный огурец и т.д.).
3. Информацию о заказанном хот-доге нужно отображать на экран и сохранять в файл.
4. Если пользователь заказывает от трёх хот-догов нужно
предусмотреть скидку.Скидка зависит от количества
хот-догов.
5. Расчет может производиться, как наличными, так и
картой.
6. Необходимо иметь возможность просмотреть количество проданных хот-догов, выручку, прибыль.
7. Необходимо иметь возможность просмотреть информацию о наличии компонентов для создания хот-дога.
8. Если компоненты для создания хот-догов заканчиваются нужно вывести информационное сообщение
о тех компонентах, которые требуется приобрести.
9. Классы приложения должны быть построены с учетом принципов SOLID и паттернов проектирования."""
import abc
import join
from enum import Enum
class Ingredient(abc.ABC):
    def __init__(self, name, quantity, cost_per):
        self.name = name
        self.quantity = quantity
        self.cost_per = cost_per
    def __repr__(self):
        return f"{self.__class__.name__}(name='{self.name}', quantity='{self.quantity} cost_per={self.cost_per})"

class Topping(Ingredient):
    def __init__(self, name, quantity, cost_per):
        super().__init__(name, quantity, cost_per)
    
class Bun(Ingredient):
    def __init__(self, name, quantity, cost_per):
    super().__init__(name, quantity, cost_per)

class Sausage(Ingredient):
    def __init__(self, name, quantity, cost_per):
    super().__init__(name, quantity, cost_per)

class Sauce(Ingredient):
    def __init__(self, name, quantity, cost_per):
    super().__init__(name, quantity, cost_per)

class HotDog:
    def __init__(self, bun, sausage, sauces=None, toppings=None):
        self.bun = bun
        self.sausage = sausage
        self.sauces = sauces if sauces else []
        self.toppings = toppings if toppings else []
    
    def calculator_price(self):
        price = self.bun.cost_per + self.sausage.cost_per
        for sauce in self.sauces:
            price += sauce.cost_per
        for topping in self.toppings:
            price += topping.cost_per
        return price
    
    def __str__(self):
        sauce_str= ", ".join([sa.name for sauce in self.sauces])
        topping_str = ", ".join([topping.name for topping in self.toppings])
        return f"Хот-Дог(Булка='{self.bun}', Сосиска='{self.sausage}', Соусы='{sauce_str or 'Нет'}', Топпинги='{topping_str or 'Нет'}')"
    
class Recipe(abc.ABC):
    @abc.abstractmethod
    def create_hot_dog(self):
        pass

class Sandart(Recipe):
    def __init__(self, bun, sausage, sauces, toppings):
        self.bun = bun
        self.sausage = sausage
        self.sauces = sauces
        self.toppings = toppings
    def create_hot_dog(self):
        return Хот-Дог(self.bun, self.sausage, self.sauces, self.toppings)
class Custom(Recipe):
    def __init__(self, bun, sausage, sauces, toppings):
        self.bun = bun
        self.sausage = sausage
        self.sauces = sauces
        self.toppings = toppings
    def create_hot_dog(self):
        return Хот-Дог(self.bun, self.sausage, self.sauces, self.toppings)
class PaymentType(Enum):
    CASH = "Наличные"
    CARD = "Карта"

class 

