import xmlparser as xp
import pprint as pp


class ThirdClass(xp.XmlCreatedObject):
    def __init__(self):
        self.num = None

    def process_children(self, children):
        pass


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

    def process_children(self, children):
        pass


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


class Factory(xp.XmlCreatedObjectFactory):
    def __init__(self):
        self.mapping = {
            'First': lambda: FirstClass(),
            'Second': lambda: SecondClass(),
            'Third': lambda: ThirdClass(),
            'Forth': lambda: ForthClass()
        }

    def keys(self):
        return self.mapping.keys()

    def create(self, xml_tag):
        return self.mapping[xml_tag]()


if __name__ == '__main__':
    instance = xp.parse('Test.xml', Factory())
    pp.pprint(vars(instance))