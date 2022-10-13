import json
from typing import Any, Callable
import yaml

from abc import ABC, abstractmethod
from dataclasses import dataclass

class AnimalFactory:
    def __init__(self):
        self._serializers = {}

    @property
    def formats(self):
        return [key for key in self._serializers.keys()]

    def register_format(self, format, serializer):
        self._serializers[format] = serializer

    def create_animal(self, format, **kwargs):
        try:
            serializer = self._serializers[format]
            return serializer(**kwargs)
        except KeyError:
            raise ValueError(format)

class Serializer(ABC):
    
    @abstractmethod
    def add_param(self, key: str, val: str):
        pass

    def to_str(self) -> Callable:
        pass


class JsonSerializer(Serializer):

    def __init__(self) -> None:
        self._data = {}

    def __call__(self, **kwargs):
        for key, val in kwargs.items():
            self.add_param(key, val)
        animal = Animal(self._data, self.to_str())
        return animal

    def add_param(self, key: str, val: str):
        self._data[key] = val
    
    def to_str(self) -> Callable:
        return json.dumps


class YamlSerializer(JsonSerializer):
    def to_str(self) -> Callable:
        return yaml.dump

@dataclass
class Animal():
    data: Any
    to_str_method: Callable

    def __str__(self):
        return self.to_str_method(self.data)
