
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
		
format:
	black src/*.py

lint:
	pylint --disable=R,C src/*.py