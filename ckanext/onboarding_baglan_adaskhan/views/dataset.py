import ckan.lib.base as base
import ckan.logic as logic
from ckan.common import _, current_user, request
from ckan.lib.helpers import helper_functions as h
from flask import Blueprint
import logging

log = logging.getLogger(__name__)

dataset = Blueprint("onboarding_dataset", __name__, url_prefix="/dataset")


def review():
    id = request.form.get("id")
    review_status = request.form.get("review_status")

    url = h.url_for("dataset.read", package_type="dataset", id=id)

    try:
        context = {
            "user": current_user.name,
            "auth_user_obj": current_user,
        }

        data_dict = {"id": id, "review_status": review_status}
        logic.get_action("dataset_review")(context, data_dict)
    except logic.NotAuthorized:
        return base.abort(403, _("Not authorized to review datasets"))
    except logic.NotFound:
        h.flash_error(_("Dataset not found"))
        return h.redirect_to("dataset.index")
    except logic.ValidationError as e:
        h.flash_error((e.message or e.error_summary or e.error_dict))
        return h.redirect_to(url)

    if review_status == "approved":
        h.flash_success(_("Successfully approved dataset"))
    else:
        h.flash_success(_("Succesfully rejected dataset"))
    return h.redirect_to(url)


dataset.add_url_rule(rule="/review", view_func=review, methods=["POST"])