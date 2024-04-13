from setuptools import find_namespace_packages
from packaging.version import parse
from itertools import chain
import json


exports = {}
exec(open('rlgym/rocket_league/version.py').read(), exports)
version = exports['__version__']

exports = {}
exec(open('rlgym/api/version.py').read(), exports)
api_version = exports['__version__']

with open('rlgym/rocket_league/README.md', 'r') as readme_file:
    long_description = readme_file.read()

packages = [pkg for pkg in find_namespace_packages() if pkg.startswith("rlgym.rocket_league")]

requires = [
    'rlgym-api >={},<{}'.format(api_version, parse(api_version).major + 1),
    'numpy >=1.19,<2',
]

extras = {
    'sim': [
        'rocketsim >=2',
    ],
    'rlviser': [
        'rlviser-py ==0.6.*',
    ],
    'game': [
        'pywin32 >=228',
        'pywinauto >=0.6.8,<0.7',
        'psutil >=5.8,<6',
    ]
}

extras['all'] = list(chain(*extras.values()))
extras['rlviser'].extend(extras['sim'])


setup = dict(
    name='rlgym-rocket-league',
    packages=packages,
    version=version,
    description='A python API that can be used to treat the game Rocket League as an Openai Gym-like environment for '
                'Reinforcement Learning projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requires,
    extras_require=extras,
    package_data={
        'rlgym.rocket_league': [
            'README.md',
            'game/plugin/*',
            'sim/collision_meshes/**/*',
        ]
    }
)

with open('setup.json', 'w') as setup_json:
    setup_json.write(json.dumps(setup))
