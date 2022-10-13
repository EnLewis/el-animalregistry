import pytest
from dataclasses import dataclass

from serializers import AnimalFactory

@dataclass
class fake_animal:
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
    return fake_animal("Erik", "4033321374", "123 Gelmer St")
    

def serialize_to_json(factory, register_factory, fake_animal):
    json_animal = factory.create_animal("JSON", **fake_animal.asdict())

    assert json_animal.to_str() == str(fake_animal.asdict())