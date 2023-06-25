from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.error = detail
        self.status_code = code


class InvalidRoomBookException(BaseCustomException):

    def __init__(self, detail):
        super().__init__(detail, status.HTTP_410_GONE)