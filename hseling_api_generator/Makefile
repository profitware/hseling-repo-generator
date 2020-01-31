all: run

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

venv:
	virtualenv --python=python3 venv && venv/bin/pip install ../hseling_lib_generator && venv/bin/pip install .

run: venv
	FLASK_APP=hseling_api_generator venv/bin/flask run

test: venv
	HSELING_API_GENERATOR_SETTINGS=../settings.cfg venv/bin/python -m unittest discover -s tests

sdist: venv test
	venv/bin/python setup.py sdist
