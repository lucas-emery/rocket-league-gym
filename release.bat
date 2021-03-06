rm -r dist
rm -r rlgym.egg-info
python setup.py sdist && twine upload dist/*