# el-animalregistry
A tool for registering animals in multiple formats.

# Quick-Start
```bash
git clone https://github.com/EnLewis/el-animalregistry.git
cd el-animalregistry
```
To use the app, users can get started with either a local python venv or docker.
### Python Venv
To get started with the app ensure you have Python3.8 or greater installed and run the following commands in terminal.  

0. If you already have `python-venv` installed skip this step.
```bash
pip install virtualenv
```
1. Setup Venv.
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker
0. If you don't have docker installed follow the instruction at the [docker install guide](https://docs.docker.com/engine/install/ubuntu/).
1. Build and run docker container.
```bash
docker build -t animal_image:test -f docker/Dockerfile.test .
DOCKER_CONTAINER_ID=$(docker run -dit animal_image:test)
docker exec -it $DOCKER_CONTAINER_ID bash
```
# Usage
To use the program run
```bash
python src/main.py -f src/animals.csv --format <format>
```
This command will display your data in it's raw string form (to_str) for the selected format, and in a rich text table (to_csv). 

### Query supported formats
The help action will list the supported formats.  

ex:
```
> python src/main.py -h | --help
usage: main.py [-h] -f FILE --format FORMAT

International Animal Registry

options:
  -h, --help   show this help message and exit
  -f FILE      File containing personal data.
  --format FR  Format to serialize data into. Allowed formats are JSON, XML, YAML, PANDAS
```
### Testing 
To run the included tests use
```bash
pytest -v
```

# Approach
This feels like a prime opportunity to use the factory design pattern. Using this pattern also lets me reuse some boilerplate to get started since I've done something similar to this before.  

The main goal is to create a standard interface for serializing and deserializing data, and if the developer wants to mutate the data with format specific tools after serialization (working with a pandas dataframe for example) they can do so as well.  

I achieve this by using a factory with pre-defined `Serializer()` objects for each supported format to produce `Animal()` objects with deserialization methods defined by the serializer at object creation time. The serialized data is held in a `<Animal>.data` property and retains its type (JSON, XML, PANDASDF).

## Swapping Out Serializers
Changing the serializer for a given format is as easy as registering a new `Serializer()` for that format with the factory. This is done in the `test_serialize_json_to_yaml` test in `tests/serializer_test.py`. 

## Adding support for additional formats
An example of this is on the `add_pickle_support` branch, which adds support for the python pickle data format.

## Pitfalls
An issue I ran into was that I needed the outputed `Animal()` objects to be able to have format specific methods for deserialization. (to_str, to_csv) which meant creating format specific objects which felt like overkill to me. If I already have a format specific serializer then I shouldn't need another format specific object definition (e.g: JsonSerializer + JsonAnimal). So I used some dynamic object creation strategies to reuse a generic `Animal` object. This way I can keep all my format specific code corralled to the serializer object definition.   

This does make some of the definitions in the `Serializer` objects a bit clunky. (Notably the @property methods which are part of the objects but never invoke `self`) but it makes the code a lot more organized to my eye.

# Enhancements
Adding support for collecting animals together into groups rather than individual data points. This could be done through overriding the concatonation operator for the animal object with the serializer, then contonating the objects instead of appending them to a list.  
I began implementing this for the PANDAS dataframe format, but it is not fully implemented.
