from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health():
    return {
        "status": "Healthy",
        "message": "HRMS API is running"
    }