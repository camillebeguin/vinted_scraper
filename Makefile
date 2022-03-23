install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
		
format:
	black src/*.py

lint:
	pylint --exit-zero --disable=R,C src/loader.py src/scraper.py src/preprocess.py