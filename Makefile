.PHONY: build-cphysics

build-cphysics:
	cd swingbye/cphysics; \
	python setup.py build_ext --build-lib ../
