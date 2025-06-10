"""Tests for validators.py."""

import pytest

import ckan.plugins.toolkit as tk

from ckanext.onboarding_baglan_adaskhan.logic import validators


def test_onboarding_baglan_adaskhan_reauired_with_valid_value():
    assert validators.onboarding_baglan_adaskhan_required("value") == "value"


def test_onboarding_baglan_adaskhan_reauired_with_invalid_value():
    with pytest.raises(tk.Invalid):
        validators.onboarding_baglan_adaskhan_required(None)
