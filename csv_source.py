#数据清洗
import pandas as pd

from job import JobPosition


def load_job(csv_path: str) -> list[dict]:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
        df = df.fillna("")
        df = df.drop_duplicates(subset=["job_id"])

        text_columns = [
            "job_id",
            "title",
            "company_name",
            "company_industry",
            "company_size",
            "city",
            "district",
            "job_category",
            "education",
            "employment_type",
            "source",
            "source_url",
        ]

        for column in text_columns:
            df[column] = df[column].astype(str).str.strip()

        number_columns = [
            "salary_min_k",
            "salary_max_k",
            "experience_years_min",
            "experience_years_max",
            "headcount",
        ]

        for column in number_columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0).astype(int)

        df["skills"] = df["skills"].apply(
            lambda value: [item.strip() for item in str(value).split(";") if item.strip()]
        )
        df["benefits"] = df["benefits"].apply(
            lambda value: [item.strip() for item in str(value).split(";") if item.strip()]
        )

        records = df.to_dict("records")

        jobs = []

        for record in records:
            job = JobPosition(
                job_id=record["job_id"],
                title=record["title"],
                company_name=record["company_name"],
                city=record["city"],
                salary_min_k=record["salary_min_k"],
                salary_max_k=record["salary_max_k"],
                education=record["education"],
                skills=record["skills"],           
            )
            jobs.append(job)

        return jobs

if __name__ == "__main__":
    res = pd.read_csv("./samples/job_positions_sample_200.csv")
    print(res.columns)