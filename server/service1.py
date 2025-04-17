import json
from dataclasses import dataclass


@dataclass
class Field:
    name: str
    type: str

def load_metadata(self,path):
     with open('server/file.json', 'r', encoding='utf-8') as f:
        data = json.load(f)      

    fields = data.get("recordSet", [])[0].get("field", [])

    # Create a list of (name, dataType) tuples.
    # Since dataType is provided as a list (e.g., ["sc:Text"]),
    # we take the first element.
    fields_list = [(field.get("name"), field.get("dataType")[0] if field.get("dataType") else None) 
                for field in fields]

if __name__ == "__main__":


    # Replace 'data.json' with the path to your JSON file
    with open('server/file.json', 'r', encoding='utf-8') as f:
        data = json.load(f)      

    # Navigate to the list of field definitions.
    # Here we assume the JSON structure has a single recordSet
    # with a "field" list.
    fields = data.get("recordSet", [])[0].get("field", [])

    # Create a list of (name, dataType) tuples.
    # Since dataType is provided as a list (e.g., ["sc:Text"]),
    # we take the first element.
    fields_list = [(field.get("name"), field.get("dataType")[0] if field.get("dataType") else None) 
                for field in fields]

    # Print the resulting list
    print(fields_list)

