import json
import re

INPUT_TS = "playerPhotos.ts"
OUTPUT_JSON = "playerPhotos.json"

def main():
    with open(INPUT_TS, "r", encoding="utf-8") as f:
        ts = f.read()

    # Extract the object literal inside { ... }
    match = re.search(r"\{([\s\S]*?)\}", ts)
    if not match:
        print("Could not find object in TS file.")
        return

    body = match.group(1).strip()

    photo_map = {}

    # Parse each line like: "Aaron Judge": "/players/aaron_judge.jpg",
    for line in body.splitlines():
        line = line.strip().rstrip(",")
        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip().strip('"')
        value = value.strip().strip('"')

        photo_map[key] = value

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(photo_map, f, indent=2)

    print(f"Created {OUTPUT_JSON} with {len(photo_map)} entries.")

if __name__ == "__main__":
    main()
