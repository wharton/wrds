clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

test: clean-pyc
	python setup.py test

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

lint:
	flake8 wrds

push:
	git push origin master
	git push github master

publish_to_warehouse:
	python -m twine upload dist/*

buld_dist:
	python setup.py sdist bdist_wheel

publish_to_anaconda:
	echo "Not implemented"

