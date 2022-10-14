# el-animalregistry
A database for registering animals in multiple formats.

# Approach
This feels like a prime opportunity to use the factory design pattern. Using this pattern also lets me reuse some boilerplate to get started since I've done something similar to this before.

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