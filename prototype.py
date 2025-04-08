import copy
from abc import ABC, abstractmethod
class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass

class Car(Prototype):
    def init(self, model, color, options):
        self.model = model
        self.color = color
        self.options = options

    def clone(self):
        return copy.deepcopy(self)

    def str(self):
        return f"Car(model={self.model}, color={self.color}, options={self.options})"

if __name__ == "main":
    car1 = Car("model", 'color', ['автопилот', "панорамная крыша"])
    print("оригинал", car1)

    car2 = car1.clone()
    car2.color = 'синий'
    car2.options.append("спортивный режим")

    print("копия", car2)
    print("оригинал после клонирования", car1)