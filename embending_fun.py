"""Job embedding and Chroma vector-store helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from langchain_ollama import OllamaEmbeddings

from csv_source import load_job
from job import JobPosition


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_CSV_PATH = PROJECT_ROOT / "job_positions_sample_200.csv"
DEFAULT_CHROMA_PATH = PROJECT_ROOT / "chroma_db"
DEFAULT_COLLECTION_NAME = "job_positions"
DEFAULT_EMBEDDING_MODEL = "nomic-embed-text:latest"


def build_job_text(job: JobPosition) -> str:
    """Convert one job object into structured text for semantic search."""
    skills_text = "、".join(job.skills)

    return f"""
职位ID：{job.job_id}
职位名称：{job.title}
公司名称：{job.company_name}
城市：{job.city}
薪资范围：{job.salary_min_k}K-{job.salary_max_k}K
学历要求：{job.education}
技能要求：{skills_text}
""".strip()


def build_job_metadata(job: JobPosition) -> dict[str, Any]:
    """Keep fields that are useful for filtering and result display."""
    return {
        "job_id": job.job_id,
        "title": job.title,
        "company_name": job.company_name,
        "city": job.city,
        "salary_min_k": job.salary_min_k,
        "salary_max_k": job.salary_max_k,
        "education": job.education,
        "skills": "、".join(job.skills),
    }


def load_chromadb():
    """Import Chroma lazily so the error message stays easy to understand."""
    try:
        import chromadb
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "缺少 chromadb 依赖，请先运行：pip install chromadb"
        ) from exc

    return chromadb


def build_vector_store(
    csv_path: str | Path = DEFAULT_CSV_PATH,
    persist_path: str | Path = DEFAULT_CHROMA_PATH,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    reset_collection: bool = True,
) -> int:
    """Read jobs from CSV, embed them, and save them into Chroma."""
    chromadb = load_chromadb()

    jobs = load_job(str(csv_path))
    ids = [job.job_id for job in jobs]
    texts = [build_job_text(job) for job in jobs]
    metadatas = [build_job_metadata(job) for job in jobs]

    embeddings = OllamaEmbeddings(model=embedding_model)
    vectors = embeddings.embed_documents(texts)

    client = chromadb.PersistentClient(path=str(persist_path))

    if reset_collection:
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

    collection = client.get_or_create_collection(name=collection_name)
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=vectors,
        metadatas=metadatas,
    )

    return len(jobs)


def search_jobs(
    question: str,
    top_k: int = 5,
    persist_path: str | Path = DEFAULT_CHROMA_PATH,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
) -> list[dict[str, Any]]:
    """Search similar jobs from the Chroma collection."""
    chromadb = load_chromadb()

    embeddings = OllamaEmbeddings(model=embedding_model)
    query_vector = embeddings.embed_query(question)

    client = chromadb.PersistentClient(path=str(persist_path))
    collection = client.get_collection(name=collection_name)

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


if __name__ == "__main__":
    count = build_vector_store()
    print(f"已写入 {count} 条职位向量")
