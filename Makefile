install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
		
format:
	black src/*.py

lint:
	pylint -j 3 --disable=C0116,C0114 src/loader.py src/preprocess.py src/scraper.py