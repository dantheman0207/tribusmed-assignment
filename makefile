demo: install run

install:
	source tribusmed/bin/activate; pip install -r requirements.txt

run:
	source tribusmed/bin/activate; python manipulator.py