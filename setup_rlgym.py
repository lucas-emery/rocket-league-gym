from itertools import chain
import json


exports = {}
exec(open('rlgym/version/version.py').read(), exports)
version = exports['__version__']

exports = {}
exec(open('rlgym/api/version.py').read(), exports)
api_version = exports['__version__']

exports = {}
exec(open('rlgym/rocket_league/version.py').read(), exports)
rl_version = exports['__version__']


with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

requires = [
    'rlgym-api =={}'.format(api_version),
]

extras = {
    'rl': ['rlgym-rocket-league[all] =={}'.format(rl_version)],
    'rl-sim': ['rlgym-rocket-league[sim] =={}'.format(rl_version)],
    'rl-rlviser': ['rlgym-rocket-league[rlviser] =={}'.format(rl_version)],
}

extras['all'] = list(chain(extras['rl']))


setup = dict(
    name='rlgym',
    packages=['rlgym.version'],
    version=version,
    description='A python API with zero dependencies to create fully customizable environments for '
                'Reinforcement Learning projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requires,
    extras_require=extras
)

with open('setup.json', 'w') as setup_json:
    setup_json.write(json.dumps(setup))
