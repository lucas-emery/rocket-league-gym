rm -r dist *.egg-info
python setup.py sdist && twine upload dist/*
rm -r dist *.egg-info setup.json
