run:
	python src/main.py --settings cfg/settings.json

runbrick:
	python src/main.py --settings cfg/brickuber.json

runnotouch:
	python src/main.py --settings cfg/no-touch.json

runnoargs:
	python src/main.py

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

