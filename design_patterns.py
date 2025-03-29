class Car:
    def __init__(self, engine=None, wheels=None, interior=None, color=None):
        self.engine = engine
        self.wheels = wheels
        self.interior = interior
        self.color = color

    def __str__(self):
        return f"Цвет: {self.color}, двигатель: {self.engine}, колеса: {self.wheels}, интерьер: {self.interior}"

class CarBuilder:
    def __init__(self):
        self.car = Car()

    def reset(self):
        self.car = Car()

    def set_engine(self, engine):
        self.car.engine = engine
        return self

    def set_wheels(self, wheels):
        self.car.wheels = wheels
        return self

    def set_interior(self, interior):
        self.car.interior = interior
        return self

    def set_color(self, color):
        self.car.color = color
        return self

    def get_car(self):
        return self.car

class SportCarBuilder(CarBuilder):
    def __init__(self):
        super().__init__()
        self.set_engine("V8")
        self.set_wheels("Michelin Pilot Sport 5")
        self.set_interior("Кожа")
        self.set_color("Красный")

class FamilyCarBuilder(CarBuilder):
    def __init__(self):
        super().__init__()
        self.set_engine("4-цилиндра")
        self.set_wheels("Steel")
        self.set_interior("Ткань")
        self.set_color("Голубой")

if __name__ == "__main__":
    sport_builder = SportCarBuilder()
    sport_car = sport_builder.get_car()
    print("Спортивный автомобиль:")
    print(sport_car)

    family_builder = FamilyCarBuilder()
    family_car = family_builder.get_car()
    print("\nСемейный автомобиль:")
    print(family_car)









