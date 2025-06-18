import ckan.authz as authz
from ckanext.onboarding_baglan_adaskhan.authz import user_has_review_permission
from ckan.common import _
from ckan.logic.auth.update import package_update as core_package_update
import ckan.logic as logic


def package_update(context, data_dict):
    dataset_id = data_dict.get("id")
    skip_default = context.get("skip_default", False)

    dataset = logic.get_action("package_show")(context, {"id": dataset_id})
    current_review_status = dataset.get("review_status")

    if current_review_status == "pending" and not skip_default:
        return {"success": False, "msg": "Dataset is currently in review and cannot be updated."}

    if skip_default:
        return {"success": True}

    return core_package_update(context, data_dict)


def dataset_review(context, data_dict):
    user = context['user']
    user_id = authz.get_user_id_for_username(user, allow_none=True)

    if user and user_has_review_permission(user_id):
        return {'success': True}

    return {'success': False, 'msg': _('User %s not authorized to review datasets') % user}
