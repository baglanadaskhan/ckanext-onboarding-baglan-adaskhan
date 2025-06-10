import click


@click.group(short_help="onboarding_baglan_adaskhan CLI.")
def onboarding_baglan_adaskhan():
    """onboarding_baglan_adaskhan CLI.
    """
    pass


@onboarding_baglan_adaskhan.command()
@click.argument("name", default="onboarding_baglan_adaskhan")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [onboarding_baglan_adaskhan]
