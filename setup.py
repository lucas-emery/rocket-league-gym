import json
from setuptools import setup


with open('setup.json', 'r') as setup_json:
    config = json.loads(setup_json.read())

base_config = dict(
    author='Lucas Emery, Matthew Allen and Rolv-Arild Braaten',
    author_email='contact@rlgym.org',
    url='https://rlgym.org',
    project_urls={
        'Source Code': 'https://github.com/lucas-emery/rocket-league-gym'
    },
    python_requires='>=3.7',
    license='Apache 2.0',
    license_file='LICENSE',
    keywords=['rocket-league', 'gym', 'reinforcement-learning', 'rlgym'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent",
    ]
)

setup(**{**base_config, **config})
