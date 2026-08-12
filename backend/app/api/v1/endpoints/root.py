from fastapi import APIRouter

router = APIRouter()
@router.get("/")
def root():
    return {
        "application": "HRMS",
        "version": "1.0.0"
    }