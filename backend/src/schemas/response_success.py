from email import message
from sanic_openapi import doc


class SuccessResponseSchema:
    status = doc.Integer(description="Respoonse code")
    message = doc.String(description="Response message of the call")
