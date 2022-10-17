import argparse
import csv
from rich.table import Table
from rich.console import Console

from serializers import JsonSerializer, PandasDFSerializer, YamlSerializer, XmlSerializer, AnimalFactory

supported_formats = {
    'JSON': JsonSerializer(),
    'XML': XmlSerializer(),
    'YAML': YamlSerializer(),
    'PANDAS': PandasDFSerializer()
}

def init_factory():
    factory = AnimalFactory()
    for format, serializer in supported_formats.items():
        factory.register_format(format, serializer)
    return factory

def main(factory, fp, format):

    # Prep data
    animals = []
    with open(fp, newline='') as f:
        freader = csv.DictReader(f)
        for row in freader:
            animals.append(row)
    
    # Serialize based on format
    serialized_animals = []
    for animal in animals:
        serialized_animals.append(factory.create_animal(format, **animal))
    
    # Display Method 0 (raw string)
    print("Display as raw strings")
    for animal in serialized_animals:
        print(animal)

    print()
    # Display Method 1 (csv with rich table)
    print("Display data as rich table.")
    table = Table(title="All Known Animals")
    headers = serialized_animals[0].to_csv()[0]
    for header in headers:
        table.add_column(header)

    for animal in serialized_animals:
        table.add_row(*(animal.to_csv()[1]))
    
    console = Console()
    console.print(table)

    
DEBUG = False

if __name__ == "__main__":
    factory = init_factory()
    if not DEBUG:
        parser = argparse.ArgumentParser(description='International Animal Registry')
        parser.add_argument('-f', metavar='FILE', type=str, required=True, help="File containing personal data.")
        parser.add_argument('--format', metavar='FORMAT', type=str, choices=list(supported_formats.keys()), required=True, help='Format to serialize data into. Allowed formats are '+', '.join(list(supported_formats.keys())))
        args = parser.parse_args()
        
        main(factory, args.f, args.format)
    else:
        f = 'src/animals.csv'
        format = "PANDAS"
        main(factory, f, format)