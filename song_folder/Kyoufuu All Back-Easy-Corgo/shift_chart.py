import re

SHIFT_AMOUNT = 55  # milliseconds
INPUT_FILE = "Kyoufuu All Back-Easy-Corgo.txt"
OUTPUT_FILE = "Kyoufuu All Back-Easy-Corgo1.txt"

def shift_hit_object(line):
    # Format: lane, hold, time
    parts = line.strip().split(",")
    if len(parts) == 3:
        parts[2] = str(int(parts[2].strip()) + SHIFT_AMOUNT)
        return ", ".join(parts)
    return line

def shift_laser_object(line):
    # Format: start, end, start_pos, end_pos
    parts = line.strip().split(",")
    if len(parts) == 4:
        parts[0] = str(int(parts[0].strip()) + SHIFT_AMOUNT)
        parts[1] = str(int(parts[1].strip()) + SHIFT_AMOUNT)
        return ", ".join(parts)
    return line

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    shifted_lines = []
    section = None

    for line in lines:
        stripped = line.strip()

        if stripped == "[HitObjects]":
            section = "hit"
            shifted_lines.append(line)
            continue
        elif stripped == "[LaserObjects]":
            section = "laser"
            shifted_lines.append(line)
            continue
        elif stripped.startswith("[") and stripped.endswith("]"):
            section = None
            shifted_lines.append(line)
            continue

        if section == "hit" and stripped and not stripped.startswith("//"):
            shifted_lines.append(shift_hit_object(line) + "\n")
        elif section == "laser" and stripped and not stripped.startswith("//"):
            shifted_lines.append(shift_laser_object(line) + "\n")
        else:
            shifted_lines.append(line)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(shifted_lines)

    print(f"Done! Shifted chart saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()