from dataclasses import dataclass

@dataclass
class JobPosition:
    job_id: str
    title: str
    company_name: str
    city: str
    salary_min_k: int
    salary_max_k: int
    education: str
    skills: list[str]




































