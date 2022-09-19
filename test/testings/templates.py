from .env import _has_github, GITHUB_HOST

# template-simple
TEMPLATE_SIMPLE = 'templates/simple'
TEMPLATE_SIMPLE_FILE = 'templates/simple/meta.py'
TEMPLATE_SIMPLE_VERSION = '0.0.1'
if _has_github():
    TEMPLATE_SIMPLE_REPO_GIT = f'git+https://{GITHUB_HOST}/igm4ai/template-simple.git'
else:
    TEMPLATE_SIMPLE_REPO_GIT = f'git+https://gitee.com/igm4ai/template-simple.git'

# template-linear
TEMPLATE_LINEAR = 'templates/linear-regression'
TEMPLATE_LINEAR_FILE = 'templates/linear-regression/meta.py'
TEMPLATE_LINEAR_VERSION = '0.0.1'

# template-test
TEMPLATE_TEST = 'templates/test'
TEMPLATE_TEST_FILE = 'templates/test/meta.py'
TEMPLATE_TEST_VERSION = '0.0.1'
