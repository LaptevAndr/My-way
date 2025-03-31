class Pasta:
    def __init__(self):
        self.type = None
        self.sauce = None
        self.filling = None
        self.additions = []  # Создает пустой список для хранения добавок

    def set_type(self, pasta_type):
        self.type = pasta_type

    def set_sauce(self, sauce):
        self.sauce = sauce

    def set_filling(self, filling):
        self.filling = filling

    def add_addition(self, addition):  # Метод для добавления добавки в список
        self.additions.append(addition)
        print(f"Добавлена добавка: {addition}")

    def get_details(self):
        return {
            "type": self.type,
            "sauce": self.sauce,
            "filling": self.filling,
            "additions": self.additions
        }
'''Использование Builder'''
class PastaBuilder:
    def __init__(self):
        self.pasta = Pasta()

    def set_type(self, pasta_type):
        self.pasta.set_type(pasta_type)
        return self

    def set_sauce(self, sauce):
        self.pasta.set_sauce(sauce)
        return self

    def set_filling(self, filling):
        self.pasta.set_filling(filling)
        return self

    def add_addition(self, addition):
        self.pasta.add_addition(addition)
        return self

    def build(self):
        return self.pasta

class CarbonaraBuilder(PastaBuilder):
    def __init__(self):
        super().__init__()
        self.set_type("Спагетти")
        self.set_sauce("Сливки")
        self.set_filling("Бекон")
        self.add_addition("Пармезан")

class BologneseBuilder(PastaBuilder):
    def __init__(self):
        super().__init__()
        self.set_type("Макароны Тальятелле ")
        self.set_sauce("Помидор")
        self.set_filling("Говядина")
        self.add_addition("Базилик")

class PestoBuilder(PastaBuilder):
    def __init__(self):
        super().__init__()
        self.set_type("Макароны Пенне")
        self.set_sauce("Песто")
        self.set_filling("Кедровые орехи")
        self.add_addition("Пармезан")

class PastaController:
    def __init__(self, pasta_model, pasta_view):
        self.pasta_model = pasta_model
        self.pasta_view = pasta_view

    def set_pasta_type(self, pasta_type):
        self.pasta_model.set_type(pasta_type)

    def set_sauce(self, sauce):
        self.pasta_model.set_sauce(sauce)

    def set_filling(self, filling):
        self.pasta_model.set_filling(filling)

    def add_addition(self, addition):
        self.pasta_model.add_addition(addition)

    def display_pasta(self):
        pasta_details = self.pasta_model.get_details()
        self.pasta_view.display_pasta(pasta_details)

class PastaView:
    def display_pasta(self, pasta_details):
        print("Тип пасты:", pasta_details["type"])
        print("Соус:", pasta_details["sauce"])
        print("Начинка:", pasta_details["filling"])
        print("Добавки:", ", ".join(pasta_details["additions"]))

if __name__ == "__main__":
    # Создаем Carbonara
    carbonara_builder = CarbonaraBuilder()
    carbonara_model = carbonara_builder.build()
    carbonara_view = PastaView()
    carbonara_controller = PastaController(carbonara_model, carbonara_view)
    print("Carbonara:")
    carbonara_controller.display_pasta()

    # Создаем Bolognese
    bolognese_builder = BologneseBuilder()
    bolognese_model = bolognese_builder.build()
    bolognese_view = PastaView()
    bolognese_controller = PastaController(bolognese_model, bolognese_view)
    print("\nBolognese:")
    bolognese_controller.display_pasta()

    # Создаем Pesto
    pesto_builder = PestoBuilder()
    pesto_model = pesto_builder.build()
    pesto_view = PastaView()
    pesto_controller = PastaController(pesto_model, pesto_view)
    print("\nPesto:")
    pesto_controller.display_pasta()