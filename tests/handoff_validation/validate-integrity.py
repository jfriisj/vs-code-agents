import json
import jsonschema
import hashlib
import os
import sys

def validate_artifacts(handoff):
    for artifact in handoff.get('artifacts', []):
        path = artifact.get('path')
        expected_hash = artifact.get('hash')
        
        if not os.path.exists(path):
            print(f"[!] Artifact not found: {path}")
            return False
        
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256.update(byte_block)
        
        actual_hash = sha256.hexdigest()
        if actual_hash != expected_hash:
            print(f"[!] SHA-256 Mismatch for {path}:")
            print(f"    Expected: {expected_hash}")
            print(f"    Actual:   {actual_hash}")
            return False
    return True

def validate_handoff_full(schema_path, handoff_path):
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    with open(handoff_path, 'r') as f:
        handoff = json.load(f)
    
    try:
        jsonschema.validate(instance=handoff, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        print(f"[!] Schema failure: {e.message}")
        return False
        
    if not validate_artifacts(handoff):
        return False
        
    print(f"[+] Handoff valid: {handoff_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate-integrity.py <schema> <handoff> [--warn-only]")
        sys.exit(1)
        
    warn_only = "--warn-only" in sys.argv
    success = validate_handoff_full(sys.argv[1], sys.argv[2])
    
    if warn_only and not success:
        print("[!] Warning: Validation failed but --warn-only is active.")
        sys.exit(0)
    sys.exit(0 if success else 1)
