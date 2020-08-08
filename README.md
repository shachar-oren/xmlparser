xmlparser
=========
A python package for parsing xml files into data structures.

Installation
------------
Using pip:
```
pip install py-xmlparser
```

Usage
-----

Create concrete classes with variable names matching the attributes of the element.
They will be filled automatically when parsing.
Those classes must inherit from `xp.XmlCreatedObject`.

Override `process_children(self, children)` to handle created instances from the inner xml.

Provide a factory that inherits from `xp.XmlCreatedObjectFactory` to create the instances with.

Then simply call `xp.parse(path_to_xml, factory)` or `xp.parse_string(xml_text, factory)`. 

#### XML
```
<First an_attribute="my-attribute">
    <Second also_an_attribute="my-second-attribute">
        <Third num="1"/>
        <Third num="2"/>
        <Third num="3"/>
        <Third num="4"/>
    </Second>
    <Second also_an_attribute="my-second-attribute">
        <Third num="5"/>
        <Third num="6"/>
    </Second>
    <Forth num1="1" num2="2"/>
</First>
```
#### Python
```
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
```