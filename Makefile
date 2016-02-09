all: approx_pi

approx_pi:
	gcc -O2 approx_pi.c -o approx_pi

clean:
	rm -rf __pycache__ approx_pi build approx_pi_cython*.c *.so
