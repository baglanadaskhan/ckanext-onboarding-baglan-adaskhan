import logging
from flask import Blueprint
from ckan.common import request, asbool, current_user, _
import ckan.lib.base as base
import ckan.logic as logic
from ckan.lib.helpers import helper_functions as h

log = logging.getLogger(__name__)
user = Blueprint(u'onboarding_user', __name__, url_prefix=u'/user')


def reviewers():
    username = request.form.get(u'username')
    status = asbool(request.form.get(u'status'))
    try:
        context = {
            u'user': current_user.name,
            u'auth_user_obj': current_user,
        }

        data_dict = {u'id': username, u'plugin_extras': { "review_permission": status }} # <===== ONLY THIS LINE CHANGED
        user = logic.get_action(u'user_patch')(context, data_dict)
    except logic.NotAuthorized:
        return base.abort(
            403,
            _(u'Not authorized to promote user to reviewer')
        )
    except logic.NotFound:
        h.flash_error(_(u'User not found'))
        return h.redirect_to(u'onboarding_admin.reviewers')
    except logic.ValidationError as e:
        h.flash_error((e.message or e.error_summary or e.error_dict))
        return h.redirect_to(u'onboarding_admin.reviewers')

    if status:
        h.flash_success(
            _(u'Promoted {} to reviewer'.format(user[u'display_name']))
        )
    else:
        h.flash_success(
            _(
                u'Revoked reviewer permission from {}'.format(
                    user[u'display_name']
                )
            )
        )
    return h.redirect_to(u'onboarding_admin.reviewers')


user.add_url_rule(rule=u'/reviewers', view_func=reviewers, methods=['POST'])
