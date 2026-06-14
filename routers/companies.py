from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import User, Company, JobApplication
from schemas import CompanyCreate, CompanyResponse


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.post("/", response_model=CompanyResponse)
def add_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_company = Company(
        user_id=current_user.id,
        name=company.name,
        website=company.website,
        location=company.location,
        industry=company.industry
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company


@router.get("/", response_model=List[CompanyResponse])
def get_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    companies = db.query(Company).filter(
        Company.user_id == current_user.id
    ).all()

    return companies


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company_by_id(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()

    if company is None:
        raise HTTPException(status_code=404, detail="company not found")

    return company


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()

    if existing_company is None:
        raise HTTPException(status_code=404, detail="company not found")

    existing_company.name = company.name
    existing_company.website = company.website
    existing_company.location = company.location
    existing_company.industry = company.industry

    db.commit()
    db.refresh(existing_company)

    return existing_company


@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()

    if company is None:
        raise HTTPException(status_code=404, detail="company not found")

    existing_application = db.query(JobApplication).filter(
        JobApplication.company_id == company_id,
        JobApplication.user_id == current_user.id
    ).first()

    if existing_application is not None:
        raise HTTPException(
            status_code=400,
            detail="cannot delete company because it has job applications"
        )

    db.delete(company)
    db.commit()

    return {
        "message": "Company deleted successfully"
    }