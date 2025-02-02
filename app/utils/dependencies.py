from typing import Annotated

from fastapi import Depends

from app.services.post_service import PostService, get_post_service
from app.services.user_service import UserService, get_user_service


UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
PostServiceDependency = Annotated[PostService, Depends(get_post_service)]
