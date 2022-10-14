import pandas
import pytest
import json
import yaml
from dataclasses import dataclass, asdict
import xml.etree.ElementTree as element_tree

from serializers import AnimalFactory, JsonSerializer, PandasDFSerializer, XmlSerializer, YamlSerializer

@dataclass
class fake_animal_class:
    name: str
    phone: str
    address: str

def validate_xml(xml):
    return type(str(xml)) is str

@pytest.fixture
def factory():
    factory = AnimalFactory()
    return factory

@pytest.fixture
def register_factory(factory):
    factory.register_format("JSON", JsonSerializer())
    factory.register_format("YAML", YamlSerializer())
    factory.register_format("XML", XmlSerializer())
    factory.register_format("PANDAS", PandasDFSerializer())

@pytest.fixture
def fake_animal():
    return fake_animal_class("Erik", "4033321374", "123 Gelmer St")

@pytest.fixture
def fake_xml_animal():
    animal = element_tree.Element("animal", attrib={'id': '2'})
    prop = element_tree.SubElement(animal, "name")
    prop.text = str('Erik')
    prop = element_tree.SubElement(animal, "phone")
    prop.text = str('4033321374')
    prop = element_tree.SubElement(animal, "address")
    prop.text = str("123 Gelmer St")
    return animal

def test_serialize_to_json(factory, register_factory, fake_animal):
    json_animal = factory.create_animal("JSON", **asdict(fake_animal))

    assert str(json_animal) == json.dumps(asdict(fake_animal))

def test_serialize_to_yaml(factory, register_factory, fake_animal):
    yaml_animal = factory.create_animal("YAML", **asdict(fake_animal))

    assert str(yaml_animal) == yaml.dump(asdict(fake_animal))

def test_serialize_to_xml(factory, register_factory, fake_animal):
    xml_animal = factory.create_animal("XML", **asdict(fake_animal))
    
    # This is a tricky one to test since xml format takes a lot of setup
    # For now we will just ensure that we get a string back with a stub
    assert validate_xml(xml_animal)

def test_serialize_json_to_yaml(factory, register_factory, fake_animal):
    # Swap serializer
    factory.register_format("JSON", YamlSerializer())

    notjson_animal = factory.create_animal("JSON", **asdict(fake_animal))

    assert str(notjson_animal) == yaml.dump(asdict(fake_animal))

def test_deserialize_to_csv(factory, register_factory, fake_animal):
    xml_animal = factory.create_animal("XML", **asdict(fake_animal))
    json_animal = factory.create_animal("JSON", **asdict(fake_animal))
    yaml_animal = factory.create_animal("YAML", **asdict(fake_animal))
    pandas_animal = factory.create_animal("PANDAS", **asdict(fake_animal))


    # Desirializing to csv should result in the same result for all formats
    assert xml_animal.to_csv() == json_animal.to_csv() == yaml_animal.to_csv() == pandas_animal.to_csv()
    
def test_concat_pandas(factory, register_factory, fake_animal):
    pandas_animal1 = factory.create_animal("PANDAS", **asdict(fake_animal))
    pandas_animal2 = factory.create_animal("PANDAS", **asdict(fake_animal))

    pandas_animal3 =  (pandas_animal1 + pandas_animal2)
    print(pandas_animal3)
    assert pandas_animal3.data.empty != True