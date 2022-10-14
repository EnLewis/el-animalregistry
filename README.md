# el-animalregistry
A database for registering animals in multiple formats.

# Approach
This feels like a prime opportunity to use the factory design pattern. Using this pattern also lets me reuse some boilerplate to get started since I've done something similar to this before.
<p>
</p>
The main goal is to create a standard interface for serializing and deserializing data, and if the developer wants to mutate the data with format specific tools (working with a pandas dataframe for example) they can do so as well.

### Pitfalls
I initially started with a factory that stores serializers for each format and uses them to generate serialized objects on demand. This way it is very easy to add, edit, and swap out new serializers for new formats at will. The issue I ran into was that I needed the outputted objects to be able to have format specific methods for deserialization. (to_str, to_csv) which would mean creating format specific objects which felt like overkill to me. If I already have a format specific serializer then I shouldn't need another format specific object definition (e.g: JsonSerializer + JsonAnimal). So I used some dynamic object creation to reuse a generic `Animal` object. This way I can keep all my format specific code corralled to the serializer object definition.

# Usage
To use the program use
```bash
python src/main.py -f <path_to_input_file> --format <format>
```

### Query supported formats
The help action will list the supported formats
ex:
```
python src/main.py -h | --help
```

# Clarifications
- 'query a list of supported formats', query implies searchability. Does this need to support search or is it enough to provide the supported formats in a help string.
- I'm not sure where to go with display the data. Does this want me to display in different applications? (Webpage, console output, excel) or different styles? (Dataframe, graph, list, table). For now I've chosen to display it in console as raw strings and in a table, would that be sufficient?

