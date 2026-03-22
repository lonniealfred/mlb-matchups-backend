import csv

INPUT_CSV = "players.csv"
OUTPUT_TS = "playerPhotos.ts"

def normalize_filename(name: str) -> str:
    """
    Convert player name → filename.
    Example: 'Aaron Judge' → 'aaron_judge.jpg'
    """
    return (
        name.lower()
        .replace(".", "")
        .replace("'", "")
        .replace(" ", "_")
        + ".jpg"
    )

def main():
    players = []

    # Read CSV
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"].strip()
            filename = normalize_filename(name)
            players.append((name, filename))

    # Write TypeScript output
    with open(OUTPUT_TS, "w", encoding="utf-8") as f:
        f.write("const playerPhotos: Record<string, string> = {\n")

        for name, filename in players:
            f.write(f'  "{name}": "/players/{filename}",\n')

        f.write('  default: "/players/default_avatar.png",\n')
        f.write("};\n\nexport default playerPhotos;\n")

    print(f"Generated {OUTPUT_TS} with {len(players)} players.")

if __name__ == "__main__":
    main()
