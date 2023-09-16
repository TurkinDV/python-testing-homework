import json
from typing import Iterator
from urllib.parse import urljoin

import factory
import httpretty
import pytest

from server.apps.identity.intrastructure.services.placeholder import (
    UserResponse,
)
from server.common.django.types import Settings


class UserResponseFactory(factory.Factory):
    """User response factory for create lead."""

    id = factory.Sequence(int)

    class Meta(object):
        model = UserResponse


@pytest.fixture()
def create_lead_api_user_response() -> UserResponseFactory:
    """Generate random user response data."""
    return UserResponseFactory.create()


@pytest.fixture()
def mock_api_create_lead(
    create_lead_api_user_response: UserResponse,
    settings: Settings,
) -> Iterator[UserResponse]:
    """Mock external `/users` calls."""
    with httpretty.httprettized():
        httpretty.register_uri(
            method=httpretty.POST,
            body=json.dumps(create_lead_api_user_response.model_dump()),
            uri=urljoin(settings.PLACEHOLDER_API_URL, 'users'),
        )
        yield create_lead_api_user_response
        assert httpretty.has_request()
