import datetime
import logging

import ckan.model as model
import ckan.model.meta as meta
import ckan.model.types as _types
from sqlalchemy import Column, ForeignKey, Table, types
from sqlalchemy.orm import Mapped, relationship

log = logging.getLogger(__name__)

dataset_review_table = Table(
    "dataset_review",
    meta.metadata,
    Column("id", types.UnicodeText, primary_key=True, default=_types.make_uuid),
    Column("package_id", types.UnicodeText, ForeignKey("package.id")),
    Column("review_status", types.UnicodeText),
    Column("user_id", types.UnicodeText, ForeignKey("user.id")),
    Column("timestamp", types.DateTime, default=datetime.datetime.utcnow),
)


class DatasetReview:
    id: Mapped[str]
    package_id: Mapped[str]
    review_status: Mapped[str]
    user_id: Mapped[str]
    timestamp: Mapped[datetime.datetime]

    def __init__(self, package_id, review_status, user_id):
        self.package_id = package_id
        self.review_status = review_status
        self.user_id = user_id

    @classmethod
    def list(cls, package_id=None):
        q = (
            meta.Session.query(
                *DatasetReview.__table__.columns,
                model.Package.title.label("dataset_title"),
                model.User.name.label("username")
            )
            .join(DatasetReview.package)
            .join(DatasetReview.user)
        )
        if package_id:
            q = q.filter(DatasetReview.package_id == package_id)
        return q


meta.registry.map_imperatively(
    DatasetReview,
    dataset_review_table,
    properties={
        "package": relationship(model.Package),
        "user": relationship(model.User),
    },
)