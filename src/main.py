import argparse
import csv

from serializers import JsonSerializer, YamlSerializer, XmlSerializer, AnimalFactory

supported_formats = {
    'JSON': JsonSerializer(),
    'XML': XmlSerializer(),
    'YAML': YamlSerializer()
}

def init_factory():
    factory = AnimalFactory()
    for format, serializer in supported_formats.items():
        factory.register_format(format, serializer)
    return factory

def main(factory, fp, format):
    animals = []
    with open(fp, newline='') as f:
        freader = csv.reader(f)
        for row in freader:
            animals.append(dict(name=row[0], phone=row[1], address=row[2]))
    
    for animal in animals:
        new_animal = factory.create_animal(format, **animal)
        print(new_animal)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='International Animal Registry')
    parser.add_argument('-f', metavar='F', type=str, required=True, help="File containing personal data.")
    parser.add_argument('--format', metavar='FR', type=str, choices=list(supported_formats.keys()), required=True, help='Format to serialize data into. Allowed values are '+', '.join(list(supported_formats.keys())))
    args = parser.parse_args()
    
    factory = init_factory()
    main(factory, args.f, args.format)

# def get_random_phone():
#     return random.randint(100000000, 999999999)

# with open('animals.csv', 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile)
#     for i in range(0, len(ADDRESSES), 2):
#         spamwriter.writerow([random.choice(NAMES), str(get_random_phone()) ,ADDRESSES[i].strip('.')])