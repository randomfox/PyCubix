run:
	python src/main.py --settings cfg/settings.json --colors cfg/colors.json

runbrick:
	python src/main.py --settings cfg/brickuber.json --colors cfg/colors.json

runnotouch:
	python src/main.py --settings cfg/no-touch.json --colors cfg/colors.json

runnoargs:
	python src/main.py

freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt

install:
	pip install -r requirements.txt
