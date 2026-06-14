from datetime import datetime

from pydantic import BaseModel, ConfigDict


# -------------------------
# User Schemas
# -------------------------

class UserCreate(BaseModel):
    name: str
    email: str
    hashed_password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Company Schemas
# -------------------------

class CompanyCreate(BaseModel):
    name: str
    website: str
    location: str
    industry: str


class CompanyResponse(BaseModel):
    id: int
    name: str
    website: str
    location: str
    industry: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Job Application Schemas
# -------------------------

class JobApplicationCreate(BaseModel):
    user_id: int
    company_id: int
    job_title: str
    job_type: str
    location: str
    remote: bool
    salary_min: int
    salary_max: int
    currency: str
    status: str
    source: str
    job_url: str
    applied_date: datetime
    deadline: datetime
    priority: str


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    company_id: int
    job_title: str
    job_type: str
    location: str
    remote: bool
    salary_min: int
    salary_max: int
    currency: str
    status: str
    source: str
    job_url: str
    applied_date: datetime
    deadline: datetime
    priority: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Interview Schemas
# -------------------------

class InterviewCreate(BaseModel):
    application_id: int
    interview_type: str
    scheduled_at: datetime
    location_or_link: str
    interviewer_name: str
    status: str
    notes: str


class InterviewResponse(BaseModel):
    id: int
    application_id: int
    interview_type: str
    scheduled_at: datetime
    location_or_link: str
    interviewer_name: str
    status: str
    notes: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Application Note Schemas
# -------------------------

class ApplicationNoteCreate(BaseModel):
    application_id: int
    note: str


class ApplicationNoteResponse(BaseModel):
    id: int
    application_id: int
    note: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)