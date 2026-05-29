.PHONY: run test build-exe build-deb build-all clean install

run:
	python3 -m mousart

test:
	python3 -m pytest tests/ -v

build-exe:
	bash scripts/build_exe.sh

build-deb:
	bash scripts/build_deb.sh

build-all: build-exe build-deb

clean:
	rm -rf build/ dist/ *.egg-info __pycache__ release/*.exe release/*.deb
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete

install:
	pip3 install -e .

install-deps:
	pip3 install PyQt6 pyserial pyinstaller

system-deps:
	sudo apt-get install -y socat python3-pyqt6 python3-serial
