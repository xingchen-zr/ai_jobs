#创建MySql表
from sqlalchemy.orm import Mapped,mapped_column,relationship
from typing_extensions import Annotated
from datetime import datetime
import sqlalchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()

#限制条件
primary_cx = Annotated[int,mapped_column(primary_key=True,autoincrement=True)]
str_cx = Annotated[str,mapped_column(sqlalchemy.String(128),nullable=False)]
date__cx = Annotated[datetime,mapped_column(sqlalchemy.DateTime,default = datetime.now)]
int_cx = Annotated[int,mapped_column(sqlalchemy.Integer)]


class JobContent(Base):

      """['job_id', 'title', 'company_name', 'company_industry', 'company_size',
        'city', 'district', 'job_category', 'salary_min_k', 'salary_max_k',
        'salary_raw', 'experience_years_min', 'experience_years_max',
        'education', 'skills', 'responsibilities', 'requirements',
        'nice_to_haves', 'benefits', 'employment_type', 'headcount', 'source',
        'source_url', 'published_at', 'is_active'],dtype='str"""

      __tablename__ = "job_content"

      id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
      job_id: Mapped[str] = mapped_column(sqlalchemy.String(128), nullable=False, unique=True)

      title: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False)
      company_name: Mapped[str] = mapped_column(sqlalchemy.String(255), nullable=False)
      city: Mapped[str] = mapped_column(sqlalchemy.String(64), nullable=False)

      salary_min_k: Mapped[int] = mapped_column(sqlalchemy.Integer, nullable=False, default=0)
      salary_max_k: Mapped[int] = mapped_column(sqlalchemy.Integer, nullable=False, default=0)

      education: Mapped[str] = mapped_column(sqlalchemy.String(32), nullable=True)
      skills: Mapped[str] = mapped_column(sqlalchemy.Text, nullable=True)

