from flask import Blueprint
import ckan.lib.base as base
import ckan.model as model
import sqlalchemy

admin = Blueprint(u'onboarding_admin', __name__, url_prefix=u'/ckan-admin')


def _get_reviewers():
    q = model.Session.query(model.User).filter(
        model.User.plugin_extras.op("->>")("review_permission").cast(sqlalchemy.Boolean) == True,
        model.User.state == u'active')
    return q


def reviewers():
    data = dict(reviewers=[a.name for a in _get_reviewers()])
    return base.render(u'admin/reviewers.html', extra_vars=data)


admin.add_url_rule(
    u'/reviewers', view_func=reviewers, methods=['GET'], strict_slashes=False
)