---
layout: page
title: Advanced and Parallel Python
subtitle: Why (and What) is Python?
---

### Why Python?

You might wonder why caring about accelerating your (already working) Python code is important. Let's have a look at a really simple example of PI approximation:

![PI approximation](img/pi.png)

We'll use a naive implementation, both in C and Python for comparison.

Here is relevant part of the C implementation, found in approx_pi.c:

~~~ {.c}
double approx_pi(int intervals)
{
     int i;
     double pi = 0.0;
     for (i = 0; i < intervals; i++) {
         pi += (4 - ((i % 2) * 8)) / (double)(2 * i + 1);
     }
     return pi;
}
~~~

And here is the equivalent Python implementation, found in approx_pi.py:

~~~ {.python}
def approx_pi(intervals):
    pi = 0.0
    for i in range(intervals):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi
~~~

Compiling and running the resulting binary would result in something like this:

~~~ {.input}
$ make approx_pi && ./approx_pi 100000000
~~~
~~~ {.output}
gcc -O2 approx_pi.c -o approx_pi
PI is approximately 3.1415926435893260, Error is 0.0000000100004671
Time = 0.4207670000000000 sec
~~~

Be aware that your measurements can be significatly different on different computers. Now for it's Python counterpart:

~~~ {.input}
$ python approx_pi.py 100000000
~~~
~~~ {.output}
PI is approximately 3.1415926435893260, Error is 0.0000000100004671
Time = 34.5257519999999971 sec
~~~

You will usually notice that the C version is 80 to 100 times faster than the Python code. You can imagine that when running long simulation, this can make a huge difference.

### What is Python?

Let's take a step back and awnser that question: What is Python?

It is self-described as "Python is a programming language that lets you work quickly and integrate systems more effectively", which is quite accurate. From a development standpoint, designing, writing and deploying Python code is usually faster than the equivalent C code. As we have seen, the only problem is that you have to make some kind of effort to speed it up.

The first thing to know is that when talking about Python, most people are really talking about [CPython](https://python.org). CPython is the reference implementation of the language but there are others. From the words of its authors, CPython is not always the fastest implementation. Let's try using one of them, [PyPy](http://pypy.org/), to see how they compare.

Using the same Python code above, we can run it using the PyPy interpreter:

~~~ {.input}
$ pypy-c ./approx_pi.py 100000000
~~~
~~~ {.output}
PI is approximately 3.1415926435893260, Error is 0.0000000100004671
Time = 0.7333470000000000 sec
~~~

That was fast. We are still about twice slower than C, but it's not bad, taking into account we did not have to change a single line of code. It is important to note that PyPy has it's [limits](http://pypy.org/compat.html):

1. It is only Python 2.7.10 compliant, not 3.x (yet).
2. It supports most of the standard library modules.
3. It doesn't support, out of the box, C Python extensions.
4. Since Numpy is a C extension, they maintain a [PyPy-compatible fork](https://bitbucket.org/pypy/numpy.git).

Let's return to a part the above statement: "integrate systems more effectively".

Python should really be seen as the glue keeping together multiple components (libraries). And since pure Python is usually pretty slow, compared to C, that means you want to integrate components written in C, and spend most of your computation time inside those libraries, not in your Python code.

Let's have a go at optimizing our code using a widely-used C-based library, Numpy. Here's a simple version that can be found in the approx_pi_numpy.py file:

~~~ {.python}
def approx_pi(intervals):
    pi1 = 4/numpy.arange(1, intervals*2, 4)
    pi2 = -4/numpy.arange(3, intervals*2, 4)
    return numpy.sum(pi1) + numpy.sum(pi2)
~~~

And now we run it:

~~~ {.input}
$ python approx_pi_numpy.py 100000000
~~~
~~~ {.output}
PI is approximately 3.1415926435844881, Error is 0.0000000100053050
Time = 1.2332240000000001 sec
~~~

While not as good as with the PyPy interpreter, it's still quite an improvement compared to our original version. The advantage of using Numpy is that you maintain full compatibility with the official Python release. This is something you want to take into account when deciding whether you should use the PyPy interpreter. It all depends on the libraries you are using and the level of compatibility vs. performance you want to achieve.
