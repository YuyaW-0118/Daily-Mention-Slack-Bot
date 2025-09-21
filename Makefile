.PHONY: venv deps build plan apply

venv:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip

deps:
	. .venv/bin/activate && pip install -r requirements.txt -t build/python

build:
	rm -rf build && mkdir -p build/python
	. .venv/bin/activate && pip install -r requirements.txt -t build/python
	cp -r lambda/* build/
	rsync -a build/python/ build/ && rm -rf build/python
	cd build && zip -r package.zip .

plan:
	cd terraform && terraform init && terraform plan

apply:
	cd terraform && terraform apply -auto-approve
