---
layout: page
title: Advanced and Parallel Python
subtitle: Compiling Python Code
---

While is might seem unintuitive to talk about compiling an interpreted language, it is often an easy and overlooked solution to speeding up Python programs. The advantage of being an interpreted language is that most Python compilers do [Just-In-Time compilation](https://en.wikipedia.org/wiki/Just-in-time_compilation), not unlike what [PyPy](http://pypy.org) is doing.

We'll first have a look at the Cython (not to be confused with CPython). It has both pre-compilation and just-in-time compilation modes. We will use the former for now as it will help us understand what it's doing and make better use of it.

It is important to note that Cython scripts use extensions to the language and as such, scripts must not end with the .py extension. The recommended extension is .pyx. Let's make a copy of our initial script:

~~~ {.input}
$ cp approx_pi.py approx_pi_cython.pyx
~~~

The relevant part of our file should look like this:

~~~ {.input}
$ cat approx_pi_cython.pyx
~~~
~~~ {.output}
...
def approx_pi(intervals):
    pi = 0.0
    for i in range(intervals):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi
...
~~~

To define compilation steps, we must create a compilation script, written in Python. A simple one, found in the setup_cython.py file, would look like this:

~~~ {.python}
from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules = cythonize("*.pyx"))
~~~

And to proceed with the compilation:

~~~ {.input}
$ python setup_cython.py build_ext --inplace
~~~

After some compilation steps involving your C compiler (GCC, clang, icc, ...), you will get, on Unix platforms, a shared library named approx_pi_cython.so. This is very differrent than what we did with PyPy in that this is not immediatly executable: it's only a library exposing functions so our main timing code, cannot be executed. To use our newly compiled function, we need to import it in a script or in a Python interpreter:

~~~ {.input}
$ ipython
~~~
~~~ {.output}
In [1]: from approx_pi_cython import approx_pi
In [2]: %timeit approx_pi(100000000)
1 loops, best of 3: 20.4 s per loop
~~~

As you can see, we are not even twice as fast as our original Python code under CPython. To see why, we have to look at the generated C code in approx_pi_cython.c:

~~~ {.c}
 PyObject *__pyx_v_pi = NULL;
[...]
  /* "approx_pi_cython.pyx":6
 *
 * def approx_pi(intervals):
 *     pi = 0.0             # <<<<<<<<<<<<<<
 *     for i in range(intervals):
 *         pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
 */
  __Pyx_INCREF(__pyx_float_0_0);
  __pyx_v_pi = __pyx_float_0_0;
~~~

This is only a small snippet of the entire code but it's enough to understand what's going on.
First, you'll notice you have a C comment with an arrow pointing to the line the next code refers to. This is helpful to know how a line or chunk of code has been translated to C.
Second, we notice that our pi variable is not a double native type, as we would expect, but a Python object. That means every interaction with that variable cannot be native C code and must go back inside the Python VM, as seen in this snippet:

~~~ {.c}
...
    __pyx_t_5 = PyNumber_Multiply(__pyx_int_8, __pyx_t_2); ...
...
~~~

So even for basic arithmetic operations like multiplications, Python is involved. Going back and forth between C/Python that way explains why we don't get really better performance.
But there is a way to help the Cython compiler and give it hint about data types. This is where we begin using language extensions, as in the approx_pi_cython2.pyx file:

~~~ {.python}
def approx_pi(int intervals):
    cdef double pi
    cdef int i
    pi = 0.0
    for i in range(intervals):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi
~~~

All we did was add types to the input parameter (int), as well the two local variable pi and i (cdef double). Let's compile and run it to compare:

~~~ {.input}
$ python setup_cython.py build_ext --inplace
...
$ ipython
~~~
~~~ {.output}
In [1]: from approx_pi_cython import approx_pi
In [2]: %timeit approx_pi(100000000)
1 loop, best of 3: 711 ms per loop
~~~

We are now on par with the PyPy interpreter. One could argue that using PyPy is easier than compiling with Cython and they would have a point: PyPy doesn't require a C compiler nor a setup script to work. However, Cython will integrate with other C extensions. Let's try to do better with Cython by looking again at the generated C code:

~~~ {.c}
...
  double __pyx_v_pi;
  int __pyx_v_i;
...
  __pyx_v_pi = 0.0;
...
    /* "approx_pi_cython2.pyx":6
 *     pi = 0.0
 *     for i in range(intervals):
 *         pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)             # <<<<<<<<<<<<<<
 *     return pi
 */
    __pyx_t_3 = (4 - (8 * __Pyx_mod_long(__pyx_v_i, 2)));
~~~

Everything looks almost right. Our variables are now native types (double and int). The only thing left is this call to __Pyx_mod_long instead of the (way faster) C modulo operator (%). This is done mainly because of different behaviour when using negative numbers. In C, -1%10 == -1 and in Python, -1%10 == 9. Since we know we won't have any negative numbers going from 0 to intervals-1, we can safely tell the Cython compiler to use the native modulo operator:

~~~ {.python}
#cython:cdivision=True
def approx_pi(int intervals):
    cdef double pi
    cdef int i
    pi = 0.0
    for i in range(intervals):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi
~~~

And we compile yet again our Cython code:

~~~ {.input}
$ python setup_cython.py build_ext --inplace
...
$ ipython
~~~
~~~ {.output}
In [1]: from approx_pi_cython import approx_pi
In [2]: %timeit approx_pi(100000000)
1 loop, best of 3: 414 ms per loop
~~~

We are now as fast as our first C code. I will let know have a look for yourself at the generated C code to confirm that the C modulo operator was indeed used.

A last note about Cython: we have learned how to compile our libraries but Cython also supports Just-In-Time compilation just by importing and running a statement before using our function:

~~~ {.input}
$ make clean && ipython
~~~
~~~ {.output}
In [1]: import pyximport; pyximport.install()
In [2]: from approx_pi_cython import approx_pi
In [3]: %timeit approx_pi(100000000)
1 loop, best of 3: 407 ms per loop
~~~
