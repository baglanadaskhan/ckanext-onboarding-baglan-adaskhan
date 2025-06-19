import ckan.logic as logic

from ckan.common import _


def review_status_validator(
    key,
    data,
    errors,
    context,
):
    value = data.get(key)
    skip_default = context.get("skip_default", False)

    if not skip_default and value != "pending":
        errors[key].append(
            _("Review status must be 'pending'")
        )

    # if skip_default and value not in ["approved", "rejected"]:
    #     errors[key].append(
    #         _("Review status must be either 'approved' or 'rejected'")
    #     )

    return

def review_status_flow_validator(key, data, errors, context):
    value = data.get(key)
    dataset_id = data.get(('id',))
    package_show_action = logic.get_action("package_show")
    dataset = package_show_action(context, {"id": dataset_id})
    current_review_status = dataset.get("review_status")

    if current_review_status == "pending":
        return

    if value == "pending":
        errors[key].append(
            _("Update the dataset to put in pending status")
        )
        return

    errors[key].append(
        _("Only pending datasets can be approved or rejected")
    )
