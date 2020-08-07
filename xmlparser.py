import xml.etree.ElementTree as ET


class XmlCreatedObject:
    def process_children(self,children):
        pass


def _parse(xml, cls):
    if xml.tag not in cls.keys():
        raise ValueError('Unknown tag encountered! Provided classes did not match the tag ' + str(xml.tag))
    instance = cls[xml.tag]()
    att = [a for a in dir(instance) if not a.startswith('__') and not callable(getattr(instance, a))]
    for a in att:
        if a in xml.attrib.keys():
            instance.__dict__[a] = xml.attrib[a]
    children = []
    for child in xml:
        children.append(_parse(child, cls))
    instance.process_children(children)
    return instance


def parse(path_to_xml, cls: dict = None):
    for c in cls.values():
        if not issubclass(c, XmlCreatedObject):
            raise TypeError(str(c) + 'must inherit XmlCreatedObject!')
    return _parse(ET.parse(path_to_xml).getroot(), cls)


def parse_string(xml_string, cls: dict = None):
    for c in cls.values():
        if not issubclass(c, XmlCreatedObject):
            raise TypeError(str(c) + 'must inherit XmlCreatedObject!')
    return _parse(ET.fromstring(xml_string), cls)
