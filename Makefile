.PHONY: build run build-exe build-deb build-all clean install

build:
	@echo "Nothing to build (pure Python project)"

run:
	python3 -m mousart

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
	python3 -m pip install --no-deps --no-build-isolation --prefix=$(DESTDIR)/usr . 2>/dev/null || \
	python3 -c "import sysconfig; print(sysconfig.get_path('purelib'))" && \
	cp -r mousart $(DESTDIR)/usr/lib/python3/dist-packages/mousart 2>/dev/null || true

install-deps:
	pip3 install PyQt6 pyserial pyinstaller

system-deps:
	sudo apt-get install -y socat python3-pyqt6 python3-serial
