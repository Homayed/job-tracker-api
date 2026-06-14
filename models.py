from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    name = Column(String)
    website = Column(String)
    location = Column(String)
    industry = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    job_title = Column(String)
    job_type = Column(String)
    location = Column(String)
    remote = Column(Boolean)

    salary_min = Column(Integer)
    salary_max = Column(Integer)
    currency = Column(String)

    status = Column(String)
    source = Column(String)
    job_url = Column(String)

    applied_date = Column(DateTime)
    deadline = Column(DateTime)
    priority = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(Integer, ForeignKey("job_applications.id"))

    interview_type = Column(String)
    scheduled_at = Column(DateTime)
    location_or_link = Column(String)
    interviewer_name = Column(String)
    status = Column(String)
    notes = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)


class ApplicationNote(Base):
    __tablename__ = "application_notes"

    id = Column(Integer, primary_key=True, index=True)

    application_id = Column(Integer, ForeignKey("job_applications.id"))

    note = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)