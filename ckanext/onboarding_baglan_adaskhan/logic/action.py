import ckan.logic as logic
from ckan.plugins import toolkit as tk

from ckanext.onboarding_baglan_adaskhan.model.dataset_review import DatasetReview
from ckanext.onboarding_baglan_adaskhan.lib.queries import get_last_reject_reviewer
from ckanext.onboarding_baglan_adaskhan.mailer import notify_reviewer_pending
from ckanext.onboarding_baglan_adaskhan.mailer import dataset_review_mail
import logging
log = logging.getLogger(__name__)


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


def dataset_review(context, data_dict):
    logic.check_access("dataset_review", context, data_dict)

    review_status = data_dict.get("review_status")
    data_dict["review_status"] = review_status

    if review_status == "approved":
        data_dict["private"] = False

    package_patch_action = tk.get_action("package_patch")
    context["skip_default"] = True

    result = package_patch_action(context, data_dict)

    dataset_id = data_dict.get("id")
    username = context.get("user")
    dataset_review_mail(username, review_status, dataset_id)
    return result




def _track_dataset_review(context, data_dict):
    model = context["model"]
    user_obj = context.get('auth_user_obj')
    review_status = data_dict.get("review_status")

    log.debug(">>> TRACKING dataset review:")
    log.debug(f"package_id = {data_dict.get('id')}")
    log.debug(f"review_status = {review_status}")
    log.debug(f"user = {user_obj}")

    if not user_obj:
        log.error("auth_user_obj is missing in context!")
        return

    dataset_review_obj = DatasetReview(
        package_id=data_dict.get("id"),
        review_status=review_status,
        user_id=user_obj.id
    )

    model.Session.add(dataset_review_obj)
    model.repo.commit()
    log.debug(">>> dataset_review successfully committed.")


@tk.chained_action
def package_create(up_func, context, data_dict):
    _default_to_pending(context, data_dict)
    result = up_func(context, data_dict)
    _track_dataset_review(context, result)
    return result


@tk.chained_action
def package_update(up_func, context, data_dict):
    old_pkg = logic.get_action("package_show")(context, {"id": data_dict["id"]})

    old_private = old_pkg.get("private", True)
    new_private = data_dict.get("private", old_private)

    context["skip_default"] = True

    if old_private and not new_private:
        data_dict["review_status"] = "pending"
        data_dict["private"] = True

    result = up_func(context, data_dict)

    dataset = tk.get_action("package_show")(context, data_dict)
    status = dataset.get("review_status", "pending")

    log.debug(f"Sending notify email to {old_pkg.get('review_status')} for dataset {status}")

    if old_pkg.get("review_status") == "rejected" and status == "pending":
        last_reviewer = get_last_reject_reviewer(data_dict["id"])
        log.debug(f"Sending notify email to {last_reviewer.email} for dataset {result['name']}")
        if last_reviewer and last_reviewer.email:
            notify_reviewer_pending(
                reviewer=last_reviewer,
                dataset=result
            )

    if data_dict.get("review_status"):
        _track_dataset_review(context, result)

    return result
