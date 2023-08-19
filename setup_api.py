from setuptools import find_namespace_packages
import json


exports = {}
exec(open('rlgym/api/version.py').read(), exports)
version = exports['__version__']

with open('rlgym/api/README.md', 'r') as readme_file:
    long_description = readme_file.read()

packages = [pkg for pkg in find_namespace_packages() if pkg.startswith("rlgym.api")]


setup = dict(
    name='rlgym-api',
    packages=packages,
    version=version,
    description='A python API with zero dependencies to create fully customizable environments for '
                'Reinforcement Learning projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data={
        'rlgym.api': [
            'README.md'
        ]
    }
)

with open('setup.json', 'w') as setup_json:
    setup_json.write(json.dumps(setup))
