from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from dependencies import get_current_user
from ai_service import analyze_job_description

router = APIRouter(
    prefix="/applications",
    tags=["AI"],
)


@router.post(
    "/{application_id}/ai-analysis",
    response_model=schemas.AIJobAnalysisResponse,
)
def analyze_application_with_ai(
    application_id: int,
    request: schemas.AIJobAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id,
        models.JobApplication.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    company_name = "Unknown company"

    if getattr(application, "company", None):
        company_name = application.company.name

    job_title = (
        getattr(application, "job_title", None)
        or getattr(application, "title", None)
        or getattr(application, "position", None)
        or "Unknown job title"
    )

    analysis = analyze_job_description(
        job_title=job_title,
        company_name=company_name,
        status=application.status,
        job_description=request.job_description,
    )

    return analysis