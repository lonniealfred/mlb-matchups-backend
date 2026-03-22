import os
import re
import httpx
import json

INPUT_JSON = "playerPhotos.json"   # convert TS → JSON once
OUTPUT_DIR = "public/players/"
OUTPUT_TS = "playerPhotos.ts"


def normalize_filename(name: str) -> str:
    """Convert player name → local filename."""
    return (
        name.lower()
        .replace(".", "")
        .replace("'", "")
        .replace(" ", "_")
        + ".jpg"
    )


def load_photo_map():
    """Load the JSON version of your player photo map."""
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def download_image(url: str, path: str):
    """Download a single image safely."""
    try:
        with httpx.stream("GET", url, timeout=10) as r:
            if r.status_code == 200:
                with open(path, "wb") as f:
                    for chunk in r.iter_bytes():
                        f.write(chunk)
                print(f"Downloaded: {path}")
            else:
                print(f"Failed ({r.status_code}): {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    photo_map = load_photo_map()
    local_map = {}

    for name, url in photo_map.items():
        if name == "default":
            local_map[name] = "/players/default_avatar.png"
            continue

        if not url.startswith("http"):
            # Already local
            local_map[name] = url
            continue

        filename = normalize_filename(name)
        local_path = os.path.join(OUTPUT_DIR, filename)

        download_image(url, local_path)

        local_map[name] = f"/players/{filename}"

    # Write updated TS file
    with open(OUTPUT_TS, "w", encoding="utf-8") as f:
        f.write("const playerPhotos: Record<string, string> = {\n")
        for name, path in local_map.items():
            f.write(f'  "{name}": "{path}",\n')
        f.write("};\n\nexport default playerPhotos;\n")

    print(f"\nDone! Updated {OUTPUT_TS} with local image paths.")


if __name__ == "__main__":
    main()
