from flask import Blueprint
import ckan.lib.base as base
import logging
from ckan.lib.dictization import table_dictize
from ckan.plugins.toolkit import get_action, request as toolkit_request
from ckanext.onboarding_baglan_adaskhan.model.dataset_review import DatasetReview
from ckan.common import g


log = logging.getLogger(__name__)

home = Blueprint("onboarding_home", __name__)


def about():
    log.debug("/about is being overriden")
    return base.render(u'home/about.html', extra_vars={})

def dataset_reviews():
    dataset_reviews_q = DatasetReview.list()
    dataset_reviews_list = dataset_reviews_q.all()

    log.debug(f"dataset_reviews_list {dataset_reviews_list}")

    user = g.user
    context = {"user": user}
    log.debug(f"context {context}")
    search_result = get_action("package_search")(context)
    log.debug(f"search_result {search_result}")
    allowed_dataset_ids = set(pkg["id"] for pkg in search_result["results"])
    log.debug(f"allowed_dataset_ids {allowed_dataset_ids}")

    visible_reviews = []
    for r in dataset_reviews_list:
        log.debug(f"package_id {r._mapping['package_id']}")

        if r._mapping["package_id"] in allowed_dataset_ids:
            visible_reviews.append(r)

    dataset_reviews_dict_list = [table_dictize(r, {}) for r in visible_reviews]

    return base.render(
        "dataset_reviews.html",
        extra_vars={"dataset_reviews": dataset_reviews_dict_list},
    )

home.add_url_rule("/about", view_func=about)
home.add_url_rule("/dataset_reviews", view_func=dataset_reviews)
