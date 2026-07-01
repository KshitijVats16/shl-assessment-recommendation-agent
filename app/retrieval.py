import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

from app.catalog import load_catalog
from app.config import settings


class Retriever:
    def __init__(self):
        self.catalog = load_catalog()

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        self.docs = [
            self.build_document(x)
            for x in self.catalog
        ]

        self.embeddings = self.model.encode(
            self.docs,
            normalize_embeddings=True
        )

        self.index = faiss.IndexFlatIP(
            self.embeddings.shape[1]
        )

        self.index.add(
            np.array(self.embeddings).astype(np.float32)
        )

        self.bm25 = BM25Okapi(
            [doc.split() for doc in self.docs]
        )

    def build_document(self, item):
        text = f"""
        Assessment Name:
        {item.get('name', '')}

        Description:
        {item.get('description', '')}

        Job Levels:
        {' '.join(item.get('job_levels', []))}

        Languages:
        {' '.join(item.get('languages', []))}

        Categories:
        {' '.join(item.get('keys', []))}
        """

        return text.lower()

    def expand_query(self, query):
        q = query.lower()

        additions = []

        if "java" in q:
            additions.extend([
                "java",
                "software developer",
                "backend developer",
                "programming"
            ])

        if "python" in q:
            additions.extend([
                "python",
                "backend developer",
                "software engineer",
                "programming"
            ])

        if "developer" in q:
            additions.extend([
                "software engineer",
                "programmer"
            ])

        if "backend" in q:
            additions.extend([
                "api",
                "database",
                "programming"
            ])

        if "sql" in q:
            additions.extend([
                "database",
                "data"
            ])

        if "fastapi" in q:
            additions.extend([
                "python",
                "backend"
            ])

        return q + " " + " ".join(additions)

    def search(self, query, top_k=10):
        query = self.expand_query(query)

        q_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )

        semantic_scores, semantic_idx = self.index.search(
            np.array(q_embedding).astype(np.float32),
            top_k
        )

        bm25_scores = self.bm25.get_scores(
            query.split()
        )

        final_scores = {}

        for rank, i in enumerate(semantic_idx[0]):
            final_scores[i] = (
                final_scores.get(i, 0)
                + float(semantic_scores[0][rank]) * 5
            )

        for i, score in enumerate(bm25_scores):
            final_scores[i] = (
                final_scores.get(i, 0)
                + float(score)
            )

        ranked = sorted(
            final_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            self.catalog[i]
            for i, _ in ranked[:top_k]
        ]