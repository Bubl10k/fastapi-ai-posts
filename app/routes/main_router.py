from fastapi import APIRouter

from app.routes.user_router import router as user_router 

__all__ = ["router"]


router = APIRouter(prefix="/api")

router.include_router(user_router)
