import ckan.model as model
import click
from sqlalchemy import Boolean, or_


@click.group(short_help="Dataset review management commands.")
def reviewers():
    pass


@reviewers.command()
def list():
    q = model.Session.query(model.User).filter(
        or_(
            model.User.plugin_extras.op("->>")("review_permission").cast(Boolean)
            == True,
            model.User.sysadmin,
        ),
        model.User.state == "active",
    )

    reviewers = q.all()
    for reviewer in reviewers:
        click.secho(reviewer.name)