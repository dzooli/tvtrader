from sanic_openapi import doc


class ErrorResponseSchema:
    description = doc.String(description="Error description")
    status = doc.Integer(description="Status code")
    message = doc.String(description="Details of the error message")


class SuccessResponseSchema:
    status = doc.Integer(description="Response code")
    message = doc.String(description="Response message of the call")
