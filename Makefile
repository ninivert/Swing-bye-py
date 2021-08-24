.PHONY: build-cython

build-cython:
	mkdir -p tmp/physics
	cython -3 -o tmp/physics/orbitsolver.c swingbye/physics/orbitsolver.pyx
	gcc \
		-shared \
		-pthread \
		-fPIC -fwrapv -fno-strict-aliasing \
		-O2 -Wall \
		-I/usr/include/python3.9 \
		-I`python -c "import numpy; print(numpy.get_include())"` \
		-o swingbye/physics/orbitsolver.so \
		tmp/physics/orbitsolver.c
	rm -r tmp
