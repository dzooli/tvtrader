from dataclasses import dataclass


@dataclass
class ErrorResponse:
    description: str = "Error description"
    content: str = "Details of the error message"
    status: int = 400


# class SuccessResponse(BaseModel):
#     status: int = Field(description="Response code", default=200)
#     content: str = Field(description="Response message of the call")


@dataclass
class SuccessResponse:
    content: str
    status: int = 200
