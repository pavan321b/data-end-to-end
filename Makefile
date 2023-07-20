install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C,W1203,E1101,W1514,W0621 *.py

run:
	python api.py

test:
	pytest test_api.py -W 'ignore::DeprecationWarning'
all: install format lint test run