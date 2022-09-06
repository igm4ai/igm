import click

from .base import CONTEXT_SETTINGS
from ..conf import load_igm_setup


def _show_cli(cli: click.Group):
    @cli.command('show', help='Show meta information of IGM Template.',
                 context_settings=CONTEXT_SETTINGS)
    @click.option('--silent', is_flag=True, default=False,
                  help='Do not show the process of template loading.', show_default=True)
    @click.argument('template', type=str)
    def _show(template: str, silent: bool):
        with load_igm_setup(template, silent=silent) as t:
            click.secho(f'Template: ', nl=False)
            click.secho(t.name, fg='cyan', underline=True)

            click.secho(f'Version: ', nl=False)
            click.secho(t.version, fg='cyan', underline=True)

            if t.description:
                click.secho(f'Description: ', nl=False)
                click.secho(t.description, underline=True)

    return cli
