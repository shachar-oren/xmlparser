

import xmlparser as xp
import pprint as pp


class ThirdClass(xp.XmlCreatedObject):
    def __init__(self):
        self.num = None


class SecondClass(xp.XmlCreatedObject):
    def __init__(self):
        self.thirds = []
        self.also_an_attribute = None

    def process_children(self, children):
        for child in children:
            if isinstance(child, ThirdClass):
                self.thirds.append(child)


class ForthClass(xp.XmlCreatedObject):
    def __init__(self):
        self.num1 = None
        self.num2 = None


class FirstClass(xp.XmlCreatedObject):
    def __init__(self):
        self.an_attribute = None
        self.seconds = []
        self.forths = []

    def process_children(self, children):
        for child in children:
            if isinstance(child, SecondClass):
                self.seconds.append(child)
            elif isinstance(child, ForthClass):
                self.forths.append(child)


if __name__ == '__main__':
    instance = xp.parse('Test.xml', {
        'First': FirstClass,
        'Second': SecondClass,
        'Third': ThirdClass,
        'Forth': ForthClass,
    })
    pp.pprint(vars(instance))