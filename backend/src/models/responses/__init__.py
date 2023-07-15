# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    description: str = "Error description"
    content: str = "Details of the error message"
    status: int = 400


class SuccessResponse(BaseModel):
    content: str = "OK"
    status: int = 200
