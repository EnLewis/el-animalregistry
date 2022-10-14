import random
import functools
from typing import Any, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Formats
import xml.etree.ElementTree as element_tree
import json
import yaml
from pandas import DataFrame

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
    
    @property
    def to_str_callable(self) -> Callable:
        pass

    @property
    def to_csv_callable(self) -> Callable:
        pass

    @abstractmethod
    def init_data(self):
        pass

class JsonSerializer(Serializer):

    @property
    def to_str_callable(self) -> Callable:
        return json.dumps

    @property
    def to_csv_callable(self):
        def _to_csv(data) -> tuple[list[str], list[str]]:
            column_headers=list(data.keys())
            values=list(data.values())
            return ([column_headers, values])
        return _to_csv
    
    def init_data(self):
        self._data = {}
    
    def __call__(self, **kwargs):
        self.init_data()
        for key, val in kwargs.items():
            self.add_param(key, val)
        animal = Animal(data=self._data, 
                        to_str_method=self.to_str_callable,
                        to_csv_method=self.to_csv_callable)
        return animal

    def add_param(self, key: str, val: str):
        self._data[key] = val


class YamlSerializer(JsonSerializer):
    @property
    def to_str_callable(self) -> Callable:
        return yaml.dump

class XmlSerializer(Serializer):

    header="animal"

    @property
    def to_str_callable(self) -> Callable:
        return element_tree.tostring

    @property
    def to_csv_callable(self):
        def _to_csv(xml) -> tuple[list[str], list[str]]:
            column_headers=[ele.tag for ele in xml.findall('*')]
            values=[ele.text for ele in xml.findall('*')]
            return ([column_headers, values])
        return _to_csv
    
    def init_data(self):
        self._data = element_tree.Element(self.header, attrib={'id': str(random.randint(0,1000))})
    
    def __call__(self, **kwargs):
        self.init_data()
        for key, val in kwargs.items():
            self.add_param(key, val)
        # This is a bit tricky, to preserve the simplicity of the Animal generic can we use partial 
        # functions to add to the callables default args.
        animal = Animal(data=self._data, 
                        to_str_method=functools.partial(self.to_str_callable, encoding='unicode'), 
                        to_csv_method=self.to_csv_callable)
        return animal
    
    def add_param(self, key, value):
        prop = element_tree.SubElement(self._data, key)
        prop.text = str(value)

class PandasDFSerializer(Serializer):
    
    @property
    def to_str_callable(self) -> Callable:
        return DataFrame.to_string

    @property
    def to_csv_callable(self):
        def _to_csv(data) -> tuple[list[str], list[str]]:
            dict_data = data.to_dict(orient='records')[0]
            column_headers=list(dict_data.keys())
            values=list(dict_data.values())
            return ([column_headers, values])
        return _to_csv

    def init_data(self, data):
        self._data = DataFrame(data={key: [value] for key, value in data.items()})
    
    def __call__(self, **kwargs):
        self.init_data(kwargs)
        animal = Animal(data=self._data, 
                        to_str_method=self.to_str_callable, 
                        to_csv_method=self.to_csv_callable)
        return animal

@dataclass
class Animal():
    data: Any
    to_str_method: Callable
    to_csv_method: Callable

    def __str__(self):
        return self.to_str_method(self.data)
    
    def to_csv(self):
        return self.to_csv_method(self.data)