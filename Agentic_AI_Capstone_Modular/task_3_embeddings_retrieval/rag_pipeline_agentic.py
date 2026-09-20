"""Vector-store-backed RAG pipeline for the banking demo.

Dependencies:
    pip install chromadb sentence-transformers

The first run downloads the embedding model. Subsequent runs reuse the
persistent Chroma database stored under memory_embeddings/banking_policy_db.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


POLICY_DOCS = {
    "gold_card_fee": (
        "Gold Credit Card: Annual Fee is $50. The annual fee is waived if annual "
        "card spending exceeds $10,000. Interest rate is 18% APR."
    ),
    "student_account": (
        "Student Account: Zero minimum balance is required. There are no monthly "
        "maintenance fees. Maximum daily cash withdrawal is $500."
    ),
    "loan_eligibility": (
        "Personal Loan: Applicants generally require a credit score above 700 and "
        "annual income above $50,000. Maximum loan tenure is five years."
    ),
    "kyc_policy": (
        "KYC policy: A valid government-issued ID, such as a passport or driver's "
        "license, is required. Address proof is required for standard accounts."
    ),
    "fraud_policy": (
        "Fraud policy: Suspected unauthorized transactions must be escalated to a "
        "human fraud-support specialist. The assistant must not investigate or modify "
        "the account directly."
    ),
}

PROJECT_ROOT = r"C:\Users\HP\OneDrive\emeritius\Capstone Project\Agentic_AI_Capstone_Modular"

class BankingRAG:
    """Persistent ChromaDB collection that returns semantically relevant policy text."""

    def __init__(
        self,
        persist_directory: str | Path | None = None,
        collection_name: str = "banking_policies",
        embedding_model: str = "all-MiniLM-L6-v2",
    ) -> None:
        # project_root = Path(__file__).resolve().parents[1]
        db_path = (
            Path(persist_directory)
            if persist_directory
            else project_root / "memory_embeddings" / "banking_policy_db"
        )
        db_path.mkdir(parents=True, exist_ok=True)

        self.embedding_function = SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )
        self.client = chromadb.PersistentClient(path=str(db_path))
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
            metadata={"description": "Mock banking policy knowledge base"},
        )
        self._seed_collection()

    def _seed_collection(self) -> None:
        """Add mock policies only once; Chroma ignores already-known IDs safely."""
        existing = self.collection.count()
        if existing > 0:
            return

        self.collection.add(
            ids=list(POLICY_DOCS.keys()),
            documents=list(POLICY_DOCS.values()),
            metadatas=[{"source": "mock_banking_policy", "policy_id": key} for key in POLICY_DOCS],
        )

    def retrieve_with_metadata(self, query: str, k: int = 3) -> list[dict[str, Any]]:
        """Return top-k semantically retrieved policy chunks and their metadata."""
        results = self.collection.query(
            query_texts=[query],
            n_results=min(k, max(1, self.collection.count())),
            include=["documents", "metadatas", "distances"],
        )

        documents = results.get("documents", [[]])[0] or []
        metadatas = results.get("metadatas", [[]])[0] or []
        distances = results.get("distances", [[]])[0] or []
        return [
            {
                "text": document,
                "metadata": metadata or {},
                "distance": round(float(distance), 4),
            }
            for document, metadata, distance in zip(documents, metadatas, distances)
        ]

    def retrieve(self, query: str, k: int = 3) -> str | None:
        """Compatibility method used by the agent; returns joined RAG context."""
        chunks = self.retrieve_with_metadata(query, k=k)
        if not chunks:
            return None
        return "\n\n".join(
            f"[{chunk['metadata'].get('policy_id', 'policy')}] {chunk['text']}"
            for chunk in chunks
        )


if __name__ == "__main__":
    rag = BankingRAG(persist_directory = PROJECT_ROOT)
    for item in rag.retrieve_with_metadata("What is the Gold Card annual fee?"):
        print(item)
