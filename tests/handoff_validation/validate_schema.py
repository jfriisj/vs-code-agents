import json
import jsonschema
import sys
import os

def validate_handoff(schema_path, json_path):
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    with open(json_path, 'r') as f:
        instance = json.load(f)
    
    try:
        jsonschema.validate(instance=instance, schema=schema)
        print(f"Validation successful for {json_path}")
        return True
    except jsonschema.exceptions.ValidationError as err:
        print(f"Validation error in {json_path}: {err.message}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_schema.py <schema_path> <json_path>")
        sys.exit(1)
    
    success = validate_handoff(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
