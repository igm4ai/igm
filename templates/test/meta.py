from igm.conf import igm_setup
from inquirer import inquire_func
from utils import trepr

igm_setup(
    name='test',
    version='0.0.1',
    description='Just a test template for IGM.',
    inquire=inquire_func,
    extras={
        'trepr': trepr
    }
)
