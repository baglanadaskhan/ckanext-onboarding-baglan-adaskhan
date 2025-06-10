import ckan.plugins.toolkit as tk


def onboarding_baglan_adaskhan_required(value):
    if not value or value is tk.missing:
        raise tk.Invalid(tk._("Required"))
    return value


def get_validators():
    return {
        "onboarding_baglan_adaskhan_required": onboarding_baglan_adaskhan_required,
    }
