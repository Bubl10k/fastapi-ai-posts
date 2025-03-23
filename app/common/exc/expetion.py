from fastapi import HTTPException


class PostValidationError(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(
            status_code=400,
            detail=f"Post validation error: {message}",
        )
