from game.game_objects import HitObject, LaserObject

def parse_file(path):
    data = {
        "HitObjects": [],
        "LaserObjects": []
    }

    current_section = None

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("//"):
                continue

            if line.startswith("[HitObjects]"):
                current_section = "HitObjects"
                continue

            if line.startswith("[LaserObjects]"):
                current_section = "LaserObjects"
                continue

            if current_section is None:
                continue

            # CSV objects
            if "," in line:
                parts = [p.strip() for p in line.split(",")]

                if current_section == "HitObjects":
                    data["HitObjects"].append(HitObject(*parts))

                elif current_section == "LaserObjects":
                    data["LaserObjects"].append(LaserObject(*parts))

                continue

    return data