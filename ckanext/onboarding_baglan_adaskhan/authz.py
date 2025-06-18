import ckan.model as model
from sqlalchemy import Boolean, or_

def user_has_review_permission(user_id):
    q = model.Session.query(model.User).filter(
        or_(model.User.id == user_id, model.User.name == user_id),
        or_(model.User.plugin_extras.op("->>")("review_permission").cast(Boolean) == True, model.User.sysadmin),
        model.User.state == u'active')
    return q.first()
