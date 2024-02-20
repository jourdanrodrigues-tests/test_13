import json
from datetime import datetime, date
from typing import cast

from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def extract_response_data(response: Response) -> list | dict | None:
    """
    DRF serializer data outputs "OrderedDict" instead of a plain dict,
    which makes it not so readable when it differs.
    """
    return getattr(response, "data", None) and json.loads(JSONRenderer().render(response.data))


class TestCaseMixin:
    maxDiff = None

    @staticmethod
    def format_datetime(value: datetime | date | None) -> str | None:
        if isinstance(value, datetime):
            return value.isoformat().replace("00:00", "Z")
        if isinstance(value, date):
            return value.isoformat()
        return value

    def assertResponse(
        self: SimpleTestCase,
        response: Response,
        expected_status: int,
        expected_data: list | dict | None,
    ) -> None:
        self.assertListEqual(
            [response.status_code, extract_response_data(response)],
            [expected_status, expected_data],
        )

    def assertNotFoundResponse(self, response: Response, message: str | None = None) -> None:
        self.assertResponse(response, status.HTTP_404_NOT_FOUND, {"detail": message or "Not found."})

    def assertUnauthorizedResponse(self, response: Response, expected_data: dict | None = None) -> None:
        data = expected_data or {"detail": "Authentication credentials were not provided."}
        self.assertResponse(response, status.HTTP_401_UNAUTHORIZED, data)

    def assertBadRequestResponse(self, response: Response, expected_data: dict) -> None:
        self.assertResponse(response, status.HTTP_400_BAD_REQUEST, expected_data)

    def assertOkResponse(self, response: Response, expected_data: list | dict | None) -> None:
        self.assertResponse(response, status.HTTP_200_OK, expected_data)

    def assertCreatedResponse(self, response: Response, expected_data: dict) -> None:
        self.assertResponse(response, status.HTTP_201_CREATED, expected_data)

    def assertForbiddenResponse(self, response: Response, message: str | None = None) -> None:
        message = message or "You do not have permission to perform this action."
        self.assertResponse(response, status.HTTP_403_FORBIDDEN, {"detail": message})

    def assertNoContentResponse(self, response: Response) -> None:
        self.assertResponse(response, status.HTTP_204_NO_CONTENT, None)

    def assertFilteredResponse(self: SimpleTestCase, response: Response, expected_data: set, key: str = "id") -> None:
        data = cast(dict, extract_response_data(response))
        self.assertSetEqual({result[key] for result in data["results"]}, expected_data)
