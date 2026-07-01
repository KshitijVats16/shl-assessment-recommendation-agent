import json
import re

INPUT = "data/shl_catalog.json"
OUTPUT = "data/shl_catalog_fixed.json"

with open(INPUT, "r", encoding="utf-8") as f:
    text = f.read()

# Replace raw newlines inside quoted strings
text = re.sub(
    r'"([^"\\]*(?:\\.[^"\\]*)*)"',
    lambda m: m.group(0).replace("\n", " "),
    text,
    flags=re.DOTALL,
)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed file written to", OUTPUT)