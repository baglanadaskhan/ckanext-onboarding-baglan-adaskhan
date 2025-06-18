import ckan.model as model
from sqlalchemy import Boolean, or_
from ckan.plugins import toolkit
from ckanext.onboarding_baglan_adaskhan.authz import user_has_review_permission


def user_is_reviewer(user_id):
    return user_has_review_permission(user_id)


def dataset_review_status(dataset_id):
    try:
        context = {"ignore_auth": True}
        data_dict = {"id": dataset_id}
        dataset = toolkit.get_action("package_show")(context, data_dict)
        status = dataset.get("review_status", "pending")
        return status if status else "pending"
    except toolkit.ObjectNotFound:
        return None


def get_helpers():
    return {
        "user_is_reviewer": user_is_reviewer,
        "dataset_review_status": dataset_review_status
    }
