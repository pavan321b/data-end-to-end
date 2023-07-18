install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C,W1203,E1101,W1514 *.py

run:
	python api.py -> results.log
all: install format lint run