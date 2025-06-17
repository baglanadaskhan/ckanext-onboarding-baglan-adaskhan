from flask import Blueprint
import ckan.lib.base as base
import logging

log = logging.getLogger(__name__)

home = Blueprint("onboarding_home", __name__)


def about():
    log.debug("/about is being overriden")
    return base.render(u'home/about.html', extra_vars={})

def my_new_route():
    return base.render(u'home/about.html', extra_vars={})

home.add_url_rule("/about", view_func=about)
home.add_url_rule("/my-new-route", view_func=my_new_route)
