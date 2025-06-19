from ckanext.onboarding_baglan_adaskhan.model.dataset_review import DatasetReview
from ckan.model import User
from ckan.model.meta import Session
from sqlalchemy import desc

def get_last_reject_reviewer(package_id):
    review = (
        Session.query(DatasetReview)
        .filter_by(package_id=package_id, review_status="rejected")
        .order_by(desc(DatasetReview.timestamp))
        .first()
    )
    if review:
        return Session.query(User).get(review.user_id)
    return None
