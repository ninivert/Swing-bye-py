.PHONY: build-cython build-cython-physicssolver build-cython-orbitsolver

build-cython: build-cython-orbitsolver build-cython-physicssolver

build-cython-experimental:
	cd swingbye/experimental; python setup.py build_ext --inplace;

build-cython-orbitsolver:
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

build-cython-physicssolver:
	mkdir -p tmp/physics

	cython -3 -o tmp/physics/physicssolver.c swingbye/physics/physicssolver.pyx
	gcc \
		-shared \
		-pthread \
		-fPIC -fwrapv -fno-strict-aliasing \
		-O2 -Wall \
		-I/usr/include/python3.9 \
		-I`python -c "import numpy; print(numpy.get_include())"` \
		-o swingbye/physics/physicssolver.so \
		tmp/physics/physicssolver.c

	rm -r tmp
