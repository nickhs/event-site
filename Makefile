deps:
	sudo pip install -r requirements.txt

bootstrap:
	foreman run python bootstrap.py

run:
	foreman start --procfile=Procfile.dev

setup: deps bootstrap run

.PHONY: deps bootstrap run setup
