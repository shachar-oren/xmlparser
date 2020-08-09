import xml.etree.ElementTree as ET


class XmlCreatedObject:
    def process_children(self, children):
        pass


class XmlCreatedObjectFactory:
    def keys(self):
        pass

    def create(self, xml_tag):
        pass


def _parse(xml, factory):
    if xml.tag not in factory.keys():
        raise ValueError('Unknown tag encountered! Provided factory keys did not match the tag ' + str(xml.tag))
    instance = factory.create(xml.tag)
    att = [a for a in dir(instance) if not a.startswith('__') and not callable(getattr(instance, a))]
    for a in att:
        if a in xml.attrib.keys():
            instance.__dict__[a] = xml.attrib[a]
    instance.process_children([_parse(child, factory) for child in xml])
    return instance


def parse(path_to_xml: str, factory, parser: ET.XMLParser = None):
    if not path_to_xml.endswith('.xml'):
        raise ValueError('The given path must point to a valid xml file!')
    if factory is None:
        raise ValueError('The given factory must not be null!')
    if not isinstance(factory, XmlCreatedObjectFactory):
        raise TypeError(str(factory) + 'must inherit XmlCreatedObjectFactory!')
    try:
        root = ET.parse(path_to_xml, parser=parser).getroot()
    except ET.ParseError:
        raise
    return _parse(root, factory)


def parse_string(xml_string, factory, parser: ET.XMLParser = None):
    if factory is None:
        raise ValueError('The given factory must not be null!')
    if not isinstance(factory, XmlCreatedObjectFactory):
        raise TypeError(str(factory) + 'must inherit XmlCreatedObjectFactory!')
    try:
        root = ET.fromstring(xml_string, parser=parser)
    except ET.ParseError:
        raise
    return _parse(root, factory)
