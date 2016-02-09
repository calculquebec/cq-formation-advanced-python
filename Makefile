all: approx_pi

approx_pi:
	gcc -O2 approx_pi.c -o approx_pi

cython: approx_pi_cython1.pyx approx_pi_cython2.pyx approx_pi_cython3.pyx
	python setup_cython.py build_ext --inplace

clean:
	rm -rf __pycache__ approx_pi build approx_pi_cython*.c *.so
