from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import User, Company, JobApplication, Interview, ApplicationNote
from schemas import JobApplicationCreate, JobApplicationResponse


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("/", response_model=JobApplicationResponse)
def add_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.query(Company).filter(
        Company.id == application.company_id,
        Company.user_id == current_user.id
    ).first()

    if company is None:
        raise HTTPException(status_code=404, detail="company not found")

    new_application = JobApplication(
        user_id=current_user.id,
        company_id=application.company_id,
        job_title=application.job_title,
        job_type=application.job_type,
        location=application.location,
        remote=application.remote,
        salary_min=application.salary_min,
        salary_max=application.salary_max,
        currency=application.currency,
        status=application.status,
        source=application.source,
        job_url=application.job_url,
        applied_date=application.applied_date,
        deadline=application.deadline,
        priority=application.priority
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


@router.get("/")
def get_applications(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    remote: Optional[bool] = None,
    company_id: Optional[int] = None,
    job_type: Optional[str] = None,
    source: Optional[str] = None,
    location: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(JobApplication).filter(
        JobApplication.user_id == current_user.id
    )

    if status is not None:
        query = query.filter(JobApplication.status == status)

    if priority is not None:
        query = query.filter(JobApplication.priority == priority)

    if remote is not None:
        query = query.filter(JobApplication.remote == remote)

    if company_id is not None:
        query = query.filter(JobApplication.company_id == company_id)

    if job_type is not None:
        query = query.filter(JobApplication.job_type == job_type)

    if source is not None:
        query = query.filter(JobApplication.source == source)

    if location is not None:
        query = query.filter(JobApplication.location.ilike(f"%{location}%"))

    if search is not None:
        query = query.filter(
            or_(
                JobApplication.job_title.ilike(f"%{search}%"),
                JobApplication.location.ilike(f"%{search}%"),
                JobApplication.status.ilike(f"%{search}%"),
                JobApplication.priority.ilike(f"%{search}%"),
                JobApplication.source.ilike(f"%{search}%"),
                JobApplication.job_type.ilike(f"%{search}%")
            )
        )

    applications = query.offset(skip).limit(limit).all()

    return {
        "message": "Applications fetched successfully",
        "count": len(applications),
        "applications": applications
    }


@router.get("/summary")
def get_application_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    applications = db.query(JobApplication).filter(
        JobApplication.user_id == current_user.id
    ).all()

    total_applications = len(applications)
    applied_count = 0
    interview_count = 0
    rejected_count = 0
    remote_count = 0
    high_priority_count = 0

    for application in applications:

        if application.status == "applied":
            applied_count += 1

        if application.status == "interview":
            interview_count += 1

        if application.status == "rejected":
            rejected_count += 1

        if application.remote is True:
            remote_count += 1

        if application.priority == "high":
            high_priority_count += 1

    return {
        "message": "Application summary fetched successfully",
        "total_applications": total_applications,
        "applied_count": applied_count,
        "interview_count": interview_count,
        "rejected_count": rejected_count,
        "remote_count": remote_count,
        "high_priority_count": high_priority_count
    }


@router.get("/{application_id}", response_model=JobApplicationResponse)
def get_application_by_id(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(JobApplication).filter(
        JobApplication.id == application_id,
        JobApplication.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(status_code=404, detail="application not found")

    return application


@router.put("/{application_id}", response_model=JobApplicationResponse)
def update_application(
    application_id: int,
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_application = db.query(JobApplication).filter(
        JobApplication.id == application_id,
        JobApplication.user_id == current_user.id
    ).first()

    if existing_application is None:
        raise HTTPException(status_code=404, detail="application not found")

    company = db.query(Company).filter(
        Company.id == application.company_id,
        Company.user_id == current_user.id
    ).first()

    if company is None:
        raise HTTPException(status_code=404, detail="company not found")

    existing_application.company_id = application.company_id
    existing_application.job_title = application.job_title
    existing_application.job_type = application.job_type
    existing_application.location = application.location
    existing_application.remote = application.remote
    existing_application.salary_min = application.salary_min
    existing_application.salary_max = application.salary_max
    existing_application.currency = application.currency
    existing_application.status = application.status
    existing_application.source = application.source
    existing_application.job_url = application.job_url
    existing_application.applied_date = application.applied_date
    existing_application.deadline = application.deadline
    existing_application.priority = application.priority
    existing_application.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(existing_application)

    return existing_application


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(JobApplication).filter(
        JobApplication.id == application_id,
        JobApplication.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(status_code=404, detail="application not found")

    db.query(Interview).filter(
        Interview.application_id == application_id
    ).delete()

    db.query(ApplicationNote).filter(
        ApplicationNote.application_id == application_id
    ).delete()

    db.delete(application)
    db.commit()

    return {
        "message": "Application deleted successfully"
    }