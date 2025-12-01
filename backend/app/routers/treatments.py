from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.crud.treatment_type import crud_treatment_type
from app.schemas.treatment_type import TreatmentTypeCreate, TreatmentTypeRead, TreatmentTypeUpdate
from app.utils.exceptions import not_found

router = APIRouter(prefix="/treatments", tags=["treatments"])


@router.get("/", response_model=list[TreatmentTypeRead])
def list_treatments(db: Session = Depends(get_db)):
    return db.query(crud_treatment_type.model).filter(crud_treatment_type.model.is_active == True).all()  # noqa: E712


@router.post("/", response_model=TreatmentTypeRead)
def create_treatment(data: TreatmentTypeCreate, db: Session = Depends(get_db), _: None = Depends(get_current_admin)):
    return crud_treatment_type.create(db, data)


@router.put("/{treatment_id}", response_model=TreatmentTypeRead)
def update_treatment(treatment_id: int, data: TreatmentTypeUpdate, db: Session = Depends(get_db), _: None = Depends(get_current_admin)):
    obj = crud_treatment_type.get(db, treatment_id)
    if not obj:
        raise not_found("TreatmentType")
    return crud_treatment_type.update(db, obj, data)


@router.patch("/{treatment_id}/activate", response_model=TreatmentTypeRead)
def activate_treatment(treatment_id: int, db: Session = Depends(get_db), _: None = Depends(get_current_admin)):
    obj = crud_treatment_type.get(db, treatment_id)
    if not obj:
        raise not_found("TreatmentType")
    return crud_treatment_type.update(db, obj, {"is_active": True})


@router.patch("/{treatment_id}/deactivate", response_model=TreatmentTypeRead)
def deactivate_treatment(treatment_id: int, db: Session = Depends(get_db), _: None = Depends(get_current_admin)):
    obj = crud_treatment_type.get(db, treatment_id)
    if not obj:
        raise not_found("TreatmentType")
    return crud_treatment_type.update(db, obj, {"is_active": False})
