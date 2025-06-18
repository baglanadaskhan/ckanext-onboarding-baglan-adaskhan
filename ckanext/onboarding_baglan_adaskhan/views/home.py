from flask import Blueprint
import ckan.lib.base as base
import logging
from ckan.lib.dictization import table_dictize
from ckanext.onboarding_baglan_adaskhan.model.dataset_review import DatasetReview


log = logging.getLogger(__name__)

home = Blueprint("onboarding_home", __name__)


def about():
    log.debug("/about is being overriden")
    return base.render(u'home/about.html', extra_vars={})

def dataset_reviews():
    dataset_reviews_q = DatasetReview.list()
    dataset_reviews_list = dataset_reviews_q.all()
    dataset_reviews_dict_list = [table_dictize(r, {}) for r in dataset_reviews_list]
    return base.render(
        "dataset_reviews.html",
        extra_vars={"dataset_reviews": dataset_reviews_dict_list},
    )

home.add_url_rule("/about", view_func=about)
home.add_url_rule("/dataset_reviews", view_func=dataset_reviews)
