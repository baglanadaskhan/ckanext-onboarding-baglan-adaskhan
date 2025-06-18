import ckan.logic as logic
from ckan.plugins import toolkit as tk

from .schema import dataset_review_schema


@tk.side_effect_free
def hello_world(context, data_dict):
    return {"message": "Hello World"}


@tk.chained_action
@tk.side_effect_free
def package_search(up_func, context, data_dict):
    result = up_func(context, data_dict)
    result["did_the_override_work"] = "Yes"
    return result


def _default_to_pending(context, data_dict):
    skip_default = context.get("skip_default", False)
    if not skip_default:
        data_dict["review_status"] = "pending"
        data_dict["private"] = True


@tk.chained_action
def package_create(up_func, context, data_dict):
    _default_to_pending(context, data_dict)
    result = up_func(context, data_dict)
    return result


@tk.chained_action
def package_update(up_func, context, data_dict):
    _default_to_pending(context, data_dict)
    result = up_func(context, data_dict)
    return result


def dataset_review(context, data_dict):
    logic.check_access("dataset_review", context, data_dict)

    review_status = data_dict.get("review_status")
    data_dict["review_status"] = review_status

    if review_status == "approved":
        data_dict["private"] = False

    package_patch_action = tk.get_action("package_patch")
    context["skip_default"] = True

    result = package_patch_action(context, data_dict)

    return result
