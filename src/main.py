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
        freader = csv.reader(f)
        for row in freader:
            animals.append(dict(name=row[0], phone=row[1], address=row[2]))
    
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
        parser.add_argument('-f', metavar='F', type=str, required=True, help="File containing personal data.")
        parser.add_argument('--format', metavar='FR', type=str, choices=list(supported_formats.keys()), required=True, help='Format to serialize data into. Allowed formats are '+', '.join(list(supported_formats.keys())))
        args = parser.parse_args()
        
        main(factory, args.f, args.format)
    else:
        f = 'src/animals.csv'
        format = "PANDAS"
        main(factory, f, format)

# def get_random_phone():
#     return random.randint(100000000, 999999999)

# with open('animals.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile)
#     for i in range(0, len(ADDRESSES), 2):
#         spamwriter.writerow([random.choice(NAMES), str(get_random_phone()) ,ADDRESSES[i].strip('.')])