import pytest
import json
from dataclasses import dataclass, asdict

from serializers import AnimalFactory, JsonSerializer

@dataclass
class fake_animal_class:
    name: str
    phone: str
    address: str

@pytest.fixture
def factory():
    factory = AnimalFactory()
    return factory

@pytest.fixture
def register_factory(factory):
    factory.register_format("JSON", JsonSerializer())

@pytest.fixture
def fake_animal():
    return fake_animal_class("Erik", "4033321374", "123 Gelmer St")
    

def test_serialize_to_json(factory, register_factory, fake_animal):
    json_animal = factory.create_animal("JSON", **asdict(fake_animal))

    assert json.dumps(json_animal) == json.dumps(asdict(fake_animal))