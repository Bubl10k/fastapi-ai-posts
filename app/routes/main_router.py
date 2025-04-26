from fastapi import APIRouter

from app.routes.auth_router import router as auth_router
from app.routes.comment_response_router import router as comment_response_router
from app.routes.comment_router import router as comment_router
from app.routes.post_router import router as post_router
from app.routes.user_router import router as user_router

__all__ = ["router"]

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(post_router)
router.include_router(comment_router)
router.include_router(comment_response_router)
