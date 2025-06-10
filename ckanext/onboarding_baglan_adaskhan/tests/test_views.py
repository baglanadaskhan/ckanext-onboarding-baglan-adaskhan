"""Tests for views.py."""

import pytest

import ckanext.onboarding_baglan_adaskhan.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "onboarding_baglan_adaskhan")
@pytest.mark.usefixtures("with_plugins")
def test_onboarding_baglan_adaskhan_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("onboarding_baglan_adaskhan.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, onboarding_baglan_adaskhan!"
