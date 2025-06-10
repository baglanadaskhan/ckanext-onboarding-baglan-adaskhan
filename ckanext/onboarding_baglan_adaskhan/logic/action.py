import ckan.plugins.toolkit as tk
import ckanext.onboarding_baglan_adaskhan.logic.schema as schema


@tk.side_effect_free
def onboarding_baglan_adaskhan_get_sum(context, data_dict):
    tk.check_access(
        "onboarding_baglan_adaskhan_get_sum", context, data_dict)
    data, errors = tk.navl_validate(
        data_dict, schema.onboarding_baglan_adaskhan_get_sum(), context)

    if errors:
        raise tk.ValidationError(errors)

    return {
        "left": data["left"],
        "right": data["right"],
        "sum": data["left"] + data["right"]
    }


def get_actions():
    return {
        'onboarding_baglan_adaskhan_get_sum': onboarding_baglan_adaskhan_get_sum,
    }
