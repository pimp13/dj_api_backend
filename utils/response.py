from typing import Any, Optional

from rest_framework import status
from rest_framework.response import Response


class BaseResponse:
    def __init__(
            self,
            ok: bool,
            message: str,
            data: Optional[Any] = None,
            status_code: int = status.HTTP_200_OK,
    ):
        self.ok = ok
        self.message = message
        self.data = data
        self.status_code = status_code

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "message": self.message,
            "data": self.data,
        }

    def to_response(self) -> Response:
        return Response(self.to_dict(), status=self.status_code)


class SuccessResponse(BaseResponse):
    def __init__(
            self,
            ok: bool = True,
            message: str = "Success",
            data: Optional[Any] = None,
            status_code: int = status.HTTP_200_OK,
    ):
        super().__init__(ok, message, data, status_code)


class ErrorResponse(BaseResponse):
    def __init__(
            self,
            ok: bool = False,
            message: str = "Error",
            data: Optional[Any] = None,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(ok, message, data, status_code)
