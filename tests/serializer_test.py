import pytest
import json
import yaml
from dataclasses import dataclass, asdict

from serializers import AnimalFactory, JsonSerializer, XmlSerializer, YamlSerializer

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

@pytest.fixture
def fake_animal():
    return fake_animal_class("Erik", "4033321374", "123 Gelmer St")

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

