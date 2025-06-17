import ckan.model as model
from sqlalchemy import Boolean, or_


def user_is_reviewer(user_id):
    q = model.Session.query(model.User).filter(
        or_(model.User.id == user_id, model.User.name == user_id),
        or_(model.User.plugin_extras.op("->>")("review_permission").cast(Boolean) == True, model.User.sysadmin),
        model.User.state == u'active')

    result = q.first()
    return result


def dataset_review_status(dataset_id):
    # Can be "pending", "approved" or "rejected"
    return "approved"


def get_helpers():
    return {
        "user_is_reviewer": user_is_reviewer,
        "dataset_review_status": dataset_review_status
    }
