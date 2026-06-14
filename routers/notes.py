from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from models import User, JobApplication, ApplicationNote
from schemas import ApplicationNoteCreate, ApplicationNoteResponse


router = APIRouter(
    prefix="/application-notes",
    tags=["Application Notes"]
)


@router.post("/", response_model=ApplicationNoteResponse)
def add_application_note(
    note: ApplicationNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(JobApplication).filter(
        JobApplication.id == note.application_id,
        JobApplication.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(status_code=404, detail="application not found")

    new_note = ApplicationNote(
        application_id=note.application_id,
        note=note.note
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@router.get("/", response_model=List[ApplicationNoteResponse])
def get_application_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notes = db.query(ApplicationNote).join(
        JobApplication,
        ApplicationNote.application_id == JobApplication.id
    ).filter(
        JobApplication.user_id == current_user.id
    ).all()

    return notes


@router.get("/{note_id}", response_model=ApplicationNoteResponse)
def get_application_note_by_id(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(ApplicationNote).join(
        JobApplication,
        ApplicationNote.application_id == JobApplication.id
    ).filter(
        ApplicationNote.id == note_id,
        JobApplication.user_id == current_user.id
    ).first()

    if note is None:
        raise HTTPException(status_code=404, detail="note not found")

    return note


@router.put("/{note_id}", response_model=ApplicationNoteResponse)
def update_application_note(
    note_id: int,
    note: ApplicationNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_note = db.query(ApplicationNote).join(
        JobApplication,
        ApplicationNote.application_id == JobApplication.id
    ).filter(
        ApplicationNote.id == note_id,
        JobApplication.user_id == current_user.id
    ).first()

    if existing_note is None:
        raise HTTPException(status_code=404, detail="note not found")

    application = db.query(JobApplication).filter(
        JobApplication.id == note.application_id,
        JobApplication.user_id == current_user.id
    ).first()

    if application is None:
        raise HTTPException(status_code=404, detail="application not found")

    existing_note.application_id = note.application_id
    existing_note.note = note.note

    db.commit()
    db.refresh(existing_note)

    return existing_note


@router.delete("/{note_id}")
def delete_application_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(ApplicationNote).join(
        JobApplication,
        ApplicationNote.application_id == JobApplication.id
    ).filter(
        ApplicationNote.id == note_id,
        JobApplication.user_id == current_user.id
    ).first()

    if note is None:
        raise HTTPException(status_code=404, detail="note not found")

    db.delete(note)
    db.commit()

    return {
        "message": "Application note deleted successfully"
    }