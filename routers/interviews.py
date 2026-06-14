from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import User, JobApplication, Interview
from schemas import InterviewCreate, InterviewResponse


router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"]
)


@router.post("/", response_model=InterviewResponse)
def add_interview(
    interview: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(JobApplication).filter(
        JobApplication.id == interview.application_id,
        JobApplication.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(status_code=404, detail="application not found")

    new_interview = Interview(
        application_id=interview.application_id,
        interview_type=interview.interview_type,
        scheduled_at=interview.scheduled_at,
        location_or_link=interview.location_or_link,
        interviewer_name=interview.interviewer_name,
        status=interview.status,
        notes=interview.notes
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return new_interview


@router.get("/", response_model=List[InterviewResponse])
def get_interviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interviews = db.query(Interview).join(
        JobApplication,
        Interview.application_id == JobApplication.id
    ).filter(
        JobApplication.user_id == current_user.id
    ).all()

    return interviews


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview_by_id(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interview = db.query(Interview).join(
        JobApplication,
        Interview.application_id == JobApplication.id
    ).filter(
        Interview.id == interview_id,
        JobApplication.user_id == current_user.id
    ).first()

    if interview is None:
        raise HTTPException(status_code=404, detail="interview not found")

    return interview


@router.put("/{interview_id}", response_model=InterviewResponse)
def update_interview(
    interview_id: int,
    interview: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_interview = db.query(Interview).join(
        JobApplication,
        Interview.application_id == JobApplication.id
    ).filter(
        Interview.id == interview_id,
        JobApplication.user_id == current_user.id
    ).first()

    if existing_interview is None:
        raise HTTPException(status_code=404, detail="interview not found")

    application = db.query(JobApplication).filter(
        JobApplication.id == interview.application_id,
        JobApplication.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(status_code=404, detail="application not found")

    existing_interview.application_id = interview.application_id
    existing_interview.interview_type = interview.interview_type
    existing_interview.scheduled_at = interview.scheduled_at
    existing_interview.location_or_link = interview.location_or_link
    existing_interview.interviewer_name = interview.interviewer_name
    existing_interview.status = interview.status
    existing_interview.notes = interview.notes

    db.commit()
    db.refresh(existing_interview)

    return existing_interview


@router.delete("/{interview_id}")
def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interview = db.query(Interview).join(
        JobApplication,
        Interview.application_id == JobApplication.id
    ).filter(
        Interview.id == interview_id,
        JobApplication.user_id == current_user.id
    ).first()

    if interview is None:
        raise HTTPException(status_code=404, detail="interview not found")

    db.delete(interview)
    db.commit()

    return {
        "message": "Interview deleted successfully"
    }