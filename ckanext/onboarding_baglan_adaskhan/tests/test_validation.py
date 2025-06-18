import pytest
from ckan.logic import get_validator

pytestmark = [
    pytest.mark.usefixtures("with_plugins"),
    pytest.mark.ckan_config(
        "ckan.plugins",
        " ".join(
            [
                "onboarding_baglan_adaskhan",
            ]
        ),
    ),
]


class TestReviewStatusValidator(object):
    def test_invalid_values(self):
        validator = get_validator("review_status_validator")
        error_msg_1 = "Review status must be 'pending'"
        error_msg_2 = "Review status must be either 'approved' or 'rejected'"
        cases = [
            {
                "skip_default": None,
                "value": None,
                "error": error_msg_1
            },
            {
                "skip_default": None,
                "value": "approved",
                "error": error_msg_1
            },
            {
                "skip_default": False,
                "value": "rejected",
                "error": error_msg_1
            },
            {
                "skip_default": True,
                "value": "invalid",
                "error": error_msg_2
            },
        ]

        for case in cases:
            errors = {"review_status": []}
            validator(
                "review_status",
                {"review_status": case["value"]},
                errors,
                {"skip_default": case["skip_default"]},
            )
            assert errors["review_status"][0] == case["error"]

    def test_valid_values(self):
        validator = get_validator("review_status_validator")
        cases = [
            {
                "skip_default": True,
                "value": "approved",
            },
            {
                "skip_default": True,
                "value": "rejected",
            },
        ]

        for case in cases:
            errors = {"review_status": []}
            validator(
                "review_status",
                {"review_status": case["value"]},
                errors,
                {"skip_default": case["skip_default"]},
            )
            assert len(errors["review_status"]) == 0