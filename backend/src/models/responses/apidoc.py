# Copyright (c) 2023 Zoltan Fabian
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from sanic_ext.extensions.openapi.definitions import (
    Response as ResponseDoc,
)
from . import SuccessResponse, ErrorResponse

SuccessDoc = ResponseDoc(
    {"application/json": SuccessResponse().model_json_schema()},
    description="Operation successful",
    status=200,
)

Error400Doc = ResponseDoc(
    {"application/json": ErrorResponse.model_json_schema()},
    description="Operation failed",
    status=400,
)
