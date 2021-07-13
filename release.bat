rm -r dist rlgym.egg-info
python setup.py sdist && twine upload dist/*
rm -r dist rlgym.egg-info
