import yaml
import os
import json

def get_config(filename):
    # Read settings from a YAML file and return the configuration.
    print(f"Read configuration file {filename}")
    try:
        with open(filename, 'r') as file:
            settings = yaml.safe_load(file)
            return settings
    except Exception as e:
        print(f"Failed to read settings from {filename}: {e}")
        return {}


script_directory = os.path.dirname(os.path.abspath(__file__))
input_directory = os.path.join(script_directory, 'subscriberInfo.yaml')

projects = get_config(input_directory)
parsed = json.loads(json.dumps((projects)))
print(json.dumps(projects, indent=4))