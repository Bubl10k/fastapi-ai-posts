from typing import Annotated

from fastapi import Depends

from app.schemas.user_schema import UserMe
from app.services.ai_service import AIService
from app.services.auth_service import AuthService, get_auth_service
from app.services.comment_service import CommentService, get_comment_service
from app.services.post_service import PostService, get_post_service
from app.services.user_service import UserService, get_user_service

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
PostServiceDependency = Annotated[PostService, Depends(get_post_service)]
CommentServiceDependency = Annotated[CommentService, Depends(get_comment_service)]
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
CurrentUserDependency = Annotated[UserMe, Depends(AuthService.get_current_user)]
AIServiceDependency = Annotated[AIService, Depends(AIService)]
