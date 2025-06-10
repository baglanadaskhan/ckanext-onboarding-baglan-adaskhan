from flask import Blueprint


onboarding_baglan_adaskhan = Blueprint(
    "onboarding_baglan_adaskhan", __name__)


def page():
    return "Hello, onboarding_baglan_adaskhan!"


onboarding_baglan_adaskhan.add_url_rule(
    "/onboarding_baglan_adaskhan/page", view_func=page)


def get_blueprints():
    return [onboarding_baglan_adaskhan]
