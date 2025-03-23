from fastapi import HTTPException


class ValidationError(HTTPException):
    def __init__(self, message) -> None:
        super().__init__(
            status_code=400,
            detail=f"Validation error: {message}",
        )
