import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

with open(
    "data/shl_catalog.json", "r",
    encoding="utf-8") as f:
    catalog = json.load(f)

texts = []

for item in catalog:
    text = f"""
    Name: {item.get('name','')}
    Description: {item.get('description','')}
    Job Levels: {' '.join(item.get('job_levels', []))}
    Test Type: {' '.join(item.get('keys', []))}
    """

    texts.append(text)

embeddings = model.encode(
    texts,
    convert_to_numpy=True
)

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)

index.add(
    embeddings.astype(np.float32)
)

Path("data").mkdir(
    exist_ok=True
)

faiss.write_index(
    index,
    "data/shl.index"
)

print("Index built.")