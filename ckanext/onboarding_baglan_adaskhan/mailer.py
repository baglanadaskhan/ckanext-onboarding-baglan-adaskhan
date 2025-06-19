import ckan.lib.mailer as mailer
from ckan.common import config
from ckan.lib.base import render
import ckan.model as model


def dataset_review_mail(username, review_status, dataset_id):
    user = model.User.get(username)
    to_email = user.email

    dataset = model.Package.get(dataset_id)
    dataset_title = dataset.title

    site_title = config.get("ckan.site_title")
    site_url = config.get("ckan.frontend_portal_url")
    subject = render("emails/dataset_review_subject.txt")
    body_vars = {"dataset_title": dataset_title, "review_status": review_status}
    body = render("emails/dataset_review.html", body_vars)

    mailer._mail_recipient(
        username,
        to_email,
        site_title,
        site_url,
        subject,
        body
    )


def notify_reviewer_pending(reviewer, dataset):
    subject = "Dataset submitted again for review"
    body = render(
        "emails/review_back_to_pending.html",
        {
            "dataset_title": dataset["title"],
            "dataset_url": f"{config.get('ckan.site_url')}/dataset/{dataset['name']}"
        }
    )

    mailer.mail_recipient(
        reviewer.name,
        reviewer.email,
        subject,
        body
    )
