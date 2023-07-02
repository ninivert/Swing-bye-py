.PHONY: build-cphysics

all: install-pybind-smart_holder build-cphysics

build-cphysics:
	cd swingbye/cphysics; \
	python setup.py build_ext --build-lib ../

install-pybind-smart_holder:
	pip uninstall pybind11
	git clone --branch smart_holder https://github.com/pybind/pybind11.git
	cd pybind11; \
	python setup.py install
	rm pybind11 -rf
