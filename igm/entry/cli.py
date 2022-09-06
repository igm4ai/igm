from .dispatch import igm
from .new import _new_cli
from .show import _show_cli

_DECORATORS = [  # all the sub commands here, using decorator pattern
    _show_cli,
    _new_cli,
]

cli_entry = igm
for deco in _DECORATORS:
    cli_entry = deco(cli_entry)
