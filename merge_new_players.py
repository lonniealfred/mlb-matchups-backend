import json
import csv

JSON_FILE = "playerPhotos.json"
CSV_FILE = "players.csv"
OUTPUT_JSON = "playerPhotos.json"

def main():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        photo_map = json.load(f)

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            if name not in photo_map:
                photo_map[name] = "/players/default_avatar.png"

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(photo_map, f, indent=2)

    print("✔ Merged new players into playerPhotos.json")

if __name__ == "__main__":
    main()
