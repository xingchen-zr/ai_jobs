"""职位向量化与 Chroma 查询。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from langchain_ollama import OllamaEmbeddings

from csv_source import load_job


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_CSV_PATH = PROJECT_ROOT / "job_positions_sample_200.csv"
DEFAULT_CHROMA_PATH = PROJECT_ROOT / "chroma_db"
DEFAULT_COLLECTION_NAME = "job_positions"
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text:latest"


class JobVectorStore:
    """职位向量库对象。"""

    def __init__(
        self,
        csv_path: str | Path = DEFAULT_CSV_PATH,
        persist_path: str | Path = DEFAULT_CHROMA_PATH,
        collection_name: str = DEFAULT_COLLECTION_NAME,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    ):
        self.csv_path = Path(csv_path)
        self.persist_path = Path(persist_path)
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.embeddings = OllamaEmbeddings(model=self.embedding_model)

    def build_vector_store(self, reset_collection: bool = True) -> int:
        """创建职位向量，并保存到 Chroma。"""
        import chromadb

        jobs = load_job(str(self.csv_path))

        ids = []
        texts = []
        metadatas = []

        for job in jobs:
            skills_text = "、".join(job.skills)

            ids.append(job.job_id)
            texts.append(
                f"""
    职位ID：{job.job_id}
    职位名称：{job.title}
    公司名称：{job.company_name}
    城市：{job.city}
    薪资范围：{job.salary_min_k}K-{job.salary_max_k}K
    学历要求：{job.education}
    技能要求：{skills_text}
    """.strip()
            )
            metadatas.append(
                {
                    "job_id": job.job_id,
                    "title": job.title,
                    "company_name": job.company_name,
                    "city": job.city,
                    "salary_min_k": job.salary_min_k,
                    "salary_max_k": job.salary_max_k,
                    "education": job.education,
                    "skills": skills_text,
                }
            )

        vectors = self.embeddings.embed_documents(texts)

        client = chromadb.PersistentClient(path=str(self.persist_path))
        collection = client.get_or_create_collection(name=self.collection_name)

        if reset_collection:
            old_data = collection.get()
            old_ids = old_data.get("ids", [])
            if old_ids:
                collection.delete(ids=old_ids)

        collection.add(
            ids=ids,
            documents=texts,
            embeddings=vectors,
            metadatas=metadatas,
        )

        return len(jobs)

    def search_jobs(self, question: str, top_k: int = 15) -> list[dict[str, Any]]:
        """从 Chroma 中搜索相似向量，并读取对应职位内容。"""
        import chromadb

        query_vector = self.embeddings.embed_query(question)

        client = chromadb.PersistentClient(path=str(self.persist_path))
        collection = client.get_collection(name=self.collection_name)

        result = collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]

        return [
            {
                "document": document,
                "metadata": metadata,
                "distance": distance,
            }
            for document, metadata, distance in zip(documents, metadatas, distances)
        ]


def build_vector_store(
    csv_path: str | Path = DEFAULT_CSV_PATH,
    persist_path: str | Path = DEFAULT_CHROMA_PATH,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    reset_collection: bool = True,
) -> int:
    vector_store = JobVectorStore(
        csv_path=csv_path,
        persist_path=persist_path,
        collection_name=collection_name,
        embedding_model=embedding_model,
    )
    return vector_store.build_vector_store(reset_collection=reset_collection)


def search_jobs(
    question: str,
    top_k: int = 15,
    persist_path: str | Path = DEFAULT_CHROMA_PATH,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
) -> list[dict[str, Any]]:
    vector_store = JobVectorStore(
        persist_path=persist_path,
        collection_name=collection_name,
        embedding_model=embedding_model,
    )
    return vector_store.search_jobs(question=question, top_k=top_k)


if __name__ == "__main__":
    count = build_vector_store()
    print(f"已写入 {count} 条职位向量")
