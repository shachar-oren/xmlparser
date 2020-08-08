from unittest.mock import call, MagicMock

import pytest
import xmlparser as xp
import xml.etree.ElementTree as ET

from examples.simple.main import FirstClass, SecondClass, ThirdClass, ForthClass


@pytest.fixture
def xml_file_path():
    return 'examples/simple/Test.xml'


def test_from_text(xml_file_path):
    m_factory = MagicMock(spec=xp.XmlCreatedObjectFactory)

    instances = {
        'First': lambda: FirstClass(),
        'Second': lambda: SecondClass(),
        'Third': lambda: ThirdClass(),
        'Forth': lambda: ForthClass(),
    }

    def side_effect(*args, **kwargs):
        return instances[args[0]]()

    m_factory.keys.return_value = instances.keys()
    m_factory.create.side_effect = side_effect
    root = ET.parse(xml_file_path).getroot()
    factory_calls = []

    file = open(xml_file_path, 'r')
    result = xp.parse_string(file.read(), m_factory)
    file.close()

    _test_from_element(root, result, factory_calls)
    m_factory.assert_has_calls(factory_calls)


def test_from_file(xml_file_path):
    m_factory = MagicMock(spec=xp.XmlCreatedObjectFactory)

    instances = {
        'First': lambda: FirstClass(),
        'Second': lambda: SecondClass(),
        'Third': lambda: ThirdClass(),
        'Forth': lambda: ForthClass(),
    }

    def side_effect(*args, **kwargs):
        return instances[args[0]]()
    m_factory.keys.return_value = instances.keys()
    m_factory.create.side_effect = side_effect
    root = ET.parse(xml_file_path).getroot()
    factory_calls = []

    result = xp.parse(xml_file_path, m_factory)

    _test_from_element(root, result, factory_calls)
    m_factory.assert_has_calls(factory_calls)


def _test_from_element(xml, result, factory_calls):
    factory_calls.append(call.keys())
    factory_calls.append(call.create(xml.tag))
    child_count = 0
    for a in result.__dict__.keys():
        if a is not None:
            if a in xml.keys():
                assert vars(result)[a] == xml.get(a)
            else:
                for instance in vars(result)[a]:
                    _test_from_element(list(xml)[child_count], instance, factory_calls)
                    child_count += 1

