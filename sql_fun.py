#数据库的各种操作
import sqlalchemy as sq

from fastapi import HTTPException
from csv_source import load_job
from job_table import JobContent


def add_jobs(db):

    records = load_job("./job_positions_sample_200.csv")

    for record in records:
        new_job = JobContent(
            job_id=record["job_id"],
            title=record["title"],
            company_name=record["company_name"],
            city=record["city"],
            salary_min_k=record["salary_min_k"],
            salary_max_k=record["salary_max_k"],
            education=record["education"],
            skills=";".join(record["skills"]),
        )
        db.add(new_job)

    db.commit()

    return ("添加成功",)


