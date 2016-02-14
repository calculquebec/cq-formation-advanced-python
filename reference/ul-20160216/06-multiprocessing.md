---
layout: page
title: Advanced and Parallel Python
subtitle: Using Multiple Cores
---

The reference Python implementation, CPython, only support the execution of one thread at a time. On modern hardware, we can leverage the power of two, four or even more cores, on one machime, using the multiprocessing module. Be aware that there is also a threading module, which lets you use a shared-memory model, but won't let you take full advantage of the underlying hardware. See [GIL description](https://wiki.python.org/moin/GlobalInterpreterLock) for more information.

When using the multiprocessing module, we use a distributed memory model. That is, a variable, in two different processes, will each have their own values. Communication and synchronisation must then be explicit. As with anything Python, the multiprocessing module makes this simple.

We'll start back with the first (non-optimized) example for PI approximation:

~~~ {.input}
$ cp approx_pi.py approx_pi_multiprocessing.py
~~~
~~~ {.python}
import sys
import math
import time

def approx_pi(intervals):
    pi = 0.0
    for i in range(intervals):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "usage: {0} <intervals>".format(sys.argv[0])
        sys.exit(1)

    t1 = time.clock()
    pi = approx_pi(int(sys.argv[1]))
    t2 = time.clock()
    print("PI is approximately %.16f, Error is %.16f"%(pi, abs(pi - math.pi)))
    print("Time = %.16f sec\n"%(t2 - t1))
~~~

To put this into context, let's measure the run time again:

~~~ {.input}
$ python approx_pi_multiprocessing.py 100000000
~~~
~~~ {.output}
PI is approximately 3.1415926435893260, Error is 0.0000000100004671
Time = 34.1915959999999970 sec
~~~

When parallelizing, the first thing to decide is how to distribute our data. We want to try and balance the workload fairly amongst all processes. In this case, this is easy as each process will need to loop (about) the same number of time.

Having a look back a our code:

~~~ {.python}
def approx_pi(intervals):
    pi = 0.0
    for i in range(intervals):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi
~~~

We take as an input a number of intervals to compute and loop from 0 to intervals-1. One approach could be to accept two parameters: start (inclusive) and end (exclusive). Now our function would look like this:

~~~ {.python}
def approx_pi(start, end):
    pi = 0.0
    for i in range(start, end):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi
~~~

This single call will need to be replaced:

~~~ {.python}
    pi = approx_pi(int(sys.argv[1]))
~~~

Now let's see how we can prepare those intervals. We'll assume 4 processes for now.

~~~ {.python}
    n = int(sys.argv[1])
    chunk_size = n/4
    intervals = map(lambda p: [p*chunk_size, p*chunk_size+chunk_size], range(4))
    intervals[-1][1] = max(intervals[-1][1], n)
~~~

The last line is to make sure that if the number of iterations is ot entirely divisible by the number of processes, we do them in the last process instead. If we output those intervals, for 4 processes and 100 million iterations, we get the following:

~~~ {.python}
    print "Intervals: ",intervals
~~~
~~~ {.output}
Intervals:  [[0, 25000000], [25000000, 50000000], [50000000, 75000000], [75000000, 100000000]]
~~~

Once we have our input data split up correctly, we can try to apply our new function, without any parallelization:

~~~ {.python}
    pi = sum(map(approx_pi, intervals))
~~~

This will apply the approx_pi on each interval, suming the partial sums at the end. This kind of operation is called a reduction and is a fundamental concept in parallel computing. Running it again should yield the right result, in about the same run time as before:

~~~ {.input}
$ python approx_pi_multiprocessing.py 100000000
~~~
~~~ {.output}
PI is approximately 3.1415926435898172, Error is 0.0000000099999760
Time = 32.7979009999999960 sec
~~~

The last missing piece is the actual parallel processing, for which we'll use the Pool.map parallel implementation of the map algorithm:

~~~ {.python}
...
from multiprocessing import Pool
...
    p = Pool(4)
    pi = sum(p.map(approx_pi, intervals))
~~~

And let's run it:

~~~ {.input}
$ python approx_pi_multiprocessing.py 100000000
~~~
~~~ {.output}
PI is approximately 3.1415926435898172, Error is 0.0000000099999760
Time = 0.0305790000000000 sec
~~~

You'll notice that the answer is right, the error margin is also good, but that the timing code is way off. It took about 10 seconds to run but we display only 0.03 sec. This is because we use the time.clock function, which is dependent on the current process (start at 0 when the process is launched) and it is confused when starting other processes. Although a little less precise, we'll change the time.clock function calls to time.time, which doesn't have this limitation:

~~~ {.python}
    t1 = time.time()
    
    n = int(sys.argv[1])
    chunk_size = n/4
    intervals = map(lambda p: [p*chunk_size, p*chunk_size+chunk_size], range(4))
    intervals[-1][1] = max(intervals[-1][1], n)

    p = Pool(4)
    pi = sum(p.map(approx_pi, intervals))

    t2 = time.time()
~~~

Which yields the following run tim:

~~~ {.input}
$ python approx_pi_multiprocessing.py 100000000
~~~
~~~ {.output}
PI is approximately 3.1415926435898172, Error is 0.0000000099999760
Time = 8.9762020111083984 sec
~~~

Which is pretty close to a 4 times speedup.
