---
layout: page
title: Advanced and Parallel Python
subtitle: Scaling Beyond One Machine
---

The technique used with the multiprocessing Python module is a fast way to achieve good scaling. Although it is based on a distributed-memory (processes) pattern, it doesn't provide scaling beyond one physical machine. For that, you need something that provides transparent network communication between processes. There are a multitude of solutions for this kind of pattern when using Python but we'll stick with an old, but proven, method called MPI.

### MPI

MPI stands for _Message Passing Interface_. As its name implies, it is a library for passing messages around between processes. A message can be anything from a simple digit to a giant Numpy matix. It is important to note that it is built to handle message passing between processes that may or may not be on the same machine. It means this method can scale to hundreds or thousands of computing cores. 

### How Does It Work?

Since it is an interface, many libraries can implement it. We are going to focus on [OpenMPI](https://www.open-mpi.org/) since it is open source and is widely available on many clusters.

Usually, when you run a Python program, you will use something like this:

~~~ {.input}
$ python my_program.py --argument1 ...
~~~

Similarly, when you run an MPI-enabled program, you will use a launcher to start multiple instances (processes) of your program:

~~~ {.input}
$ mpirun python my_program.py --argument1 ...
~~~

The default configuration on most machines, when using OpenMPI, is to use the same number of processes that there are cores available. It is possible to specify exactly the number of processes you want, for example if you are memory constrained. This would launch your program using 2 processes:

~~~ {.input}
$ mpirun -n 2 python my_program.py --argument1 ...
~~~

If you try to run a non-MPI-enabled program using the mpirun launcher, you will have 2 instances doing exactly the same thing, not communicating with each other. When doing parallel computation, you want to split your input data, like in the multiprocessing example, and distribute it amongst all participant processes.

### MPI-enabled Python Program

The most basic MPI-enabled program would look like this:

~~~ {.python}
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print "I am rank", rank, "of", size
~~~

We first import the MPI library from the mpi4py package. The _comm_ variable stands for communicator, which is a fundamental part of the MPI programming paradigm: all communication between processes or groups of processes are sent using a communicator. You can see it as a pool of processes participating in a meeting. One communicator, called world, always exist and includes all processes.

The other interesting concept is the rank. Each process is assigned a unique number, ranging from 0 to _n_-1, where n is the total number of processes. This unique number is called a rank and is used to communicate with one process in particular.

> ## Smiling Processes {.challenge}
>
> Do the following:
>
> 1. Run the exercices/smiley.py python script using mpirun and 4 processes.
> 2. Make each process print a different smiley face.
>
> A possible solution can be found in the solutions/smiley.py file.

Let's try our first run of our MPI program:

~~~ {.input}
$ mpirun -np 4 python mpi.py
~~~
~~~ {.output}
I am rank 3 of 4
I am rank 0 of 4
I am rank 1 of 4
I am rank 2 of 4
~~~

As expected, we have 4 ranks, numbered 0 to 3. The interesting thing to notice is that the output is not sequential. This is the first thing to remember: those processes are really independent processes. They do their own thing, whenever they are ready, unless we synchronize them in some way, either explicitly or by adding communication between them.

The most important aspect of MPI programming is, as it was with the multiprocessing module, is to take care to split our processing equitably between processes. Since we will start with our multiprocessing solution from the last topic, we will use the same interval-splitting and go straight to communication.

Let's have a look back at our previous (simplified) multiprocessing solution:

~~~ {.python}
import sys
import math
import time

from multiprocessing import Pool

def approx_pi(intervals):
    pi = 0.0
    for i in range(intervals[0], intervals[1]):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi

n = int(sys.argv[1])
chunk_size = n/4
intervals = map(lambda p: [p*chunk_size, p*chunk_size+chunk_size], range(4))
intervals[-1][1] = max(intervals[-1][1], n)

p = Pool(4)
pi = sum(p.map(approx_pi, intervals))
~~~

### Communication

In MPI, there are two communication patterns:

1. Point to Point: used for exchanging data between two processes.
2. Collective Operations: used for exchanging data between any number of processes, in one operation.

We will re-implement the previous example, in turn, using both communication patterns.

#### Point to Point

This mode of communication implies that one process can talk to only one other process at a time. One approach we could use in our implementation is to elect a process as our master process, and make it compute our intervals and send it to each other processes, one at a time. We will use our rank 0 for this task.

> ## Rank 0 {.callout}
> 
> In most MPI program, rank 0 is doing more things like initialization or data distribution. Keep in mind that this is a design decision and that rank 0 is exactly the same as other processes. It just happens that rank 0 will always exist (since it's the first process) so people tend to choose that one for this coordinating role.

The first thing we will add is the MPI library import:

~~~ {.python}
from mpi4py import MPI
~~~

In our previous example, we had split our inputs into 4 intervals, assuming 4 processes. We want to become more generic here and plan for any number of processes:

~~~ {.python}
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    n = int(sys.argv[1])
    chunk_size = n/size
    intervals = map(lambda p: [p*chunk_size, p*chunk_size+chunk_size], range(size))
    intervals[-1][1] = max(intervals[-1][1], n)
~~~

Notice that we compute our chunk_size by dividing it by the number of ranks (processes) instead of 4.

We then go on with the intervals distribution to all ranks, using point to point communication:

~~~ {.python}
    if rank == 0:
        myInterval = intervals[0]
        for otherRank in range(1, size):
            comm.send(intervals[otherRank], dest=otherRank)
    else:
        myInterval = comm.recv(source=0)
~~~

At this point, each process has a myInterval variable defined as their own share of the data to process. myInterval on rank 0 would be [0, 25000000], on rank 1 [25000000, 50000000], and so on. Remember that we are still using processes, with a distributed memory model. That means every process has its own independent variable myInterval, with different values.

Notice the two point to point communication functions used:

1. comm.send: it is used to send, synchronously, data to a specific rank. Here we send the sub-list intervals[otherRank] to the rank otherRank.
2. comm.recv: it is used to receive, synchronously, data from a specific rank. Here we want to receive data from rank 0 (source=0).

Note that those are blocking operations: it means if rank 0 forgets to send data to a rank, this rank will be blocked on the comm.recv call forever.

Once everyone has its share of the input data to process, here their own interval, we can process it using the approx_pi function, without modifying it:

~~~ {.python}
    partial_pi = approx_pi(myInterval)
~~~

Once we have the partial sums, we need to get the result back to rank 0, and sum them all:

~~~ {.python}
    if rank == 0:
        pi = partial_pi
        for otherRank in range(1, size):
            pi += comm.recv(source=otherRank)
    else:
        comm.send(partial_pi, dest=0)
~~~

One last thing to note: you usually want to output results, either on the terminal on to a file, only from one rank. So we will add the following to make sure only rank 0 prints the result:

~~~ {.python}
    if rank == 0:
        t2 = time.time()
        print("PI is approximately %.16f, Error is %.16f"%(pi, abs(pi - math.pi)))
        print("Time = %.16f sec\n"%(t2 - t1))
~~~

Also remember that only rank 0 has done this summing so only rank 0 known the final pi value. Let's recap everything at the same place:

~~~ {.python}
from mpi4py import MPI

import sys
import math
import time

def approx_pi(intervals):
    pi = 0.0
    for i in range(intervals[0], intervals[1]):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "usage: {0} <intervals>".format(sys.argv[0])
        sys.exit(1)

    t1 = time.time()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    n = int(sys.argv[1])
    chunk_size = n/size
    intervals = map(lambda p: [p*chunk_size, p*chunk_size+chunk_size], range(size))
    intervals[-1][1] = max(intervals[-1][1], n)

    if rank == 0:
        myInterval = intervals[0]
        for otherRank in range(1, size):
            comm.send(intervals[otherRank], dest=otherRank)
    else:
        myInterval = comm.recv(source=0)

    partial_pi = approx_pi(myInterval)
    print "Rank", rank, "partial pi:", partial_pi

    if rank == 0:
        pi = partial_pi
        for otherRank in range(1, size):
            pi += comm.recv(source=otherRank)
    else:
        comm.send(partial_pi, dest=0)

    if rank == 0:
        t2 = time.time()
        print("PI is approximately %.16f, Error is %.16f"%(pi, abs(pi - math.pi)))
        print("Time = %.16f sec\n"%(t2 - t1))
~~~

~~~ {.input}
$ mpirun -np 4 python approx_pi_mpi.py 100000000
~~~
~~~ {.output}
Rank 3 partial pi: 3.33333333333e-09
Rank 0 partial pi: 3.14159261359
Rank 1 partial pi: 2.00000000006e-08
Rank 2 partial pi: 6.66666666771e-09
PI is approximately 3.1415926435898172, Error is 0.0000000099999760
Time = 9.0873570442199707 sec
~~~

We get about the same run time as with our multiprocessing example, which is good. The code is arguably more complex, but keep in mind that now, we can scale beyond one single machine without changing a single line of code, which can be really useful, or even mandatory, to solve difficult problems.

#### Collective Operations

Collective operations imply that multiple processes coordinate for communicating. There are a handful of patterns that can be used:

* Broadcasting: used for sending the same data from one process to one or more processes.
* Scattering: used for sending chunks of data to multiple processes.
* Gathering: used for collecting chunks of data from multiple processes to one process.

Our interval distribution sure looks like scattering so we'll try to simplify our code a little using this collective operation. This is the sending part of our previous example:

~~~ {.python}
    if rank == 0:
        myInterval = intervals[0]
        for otherRank in range(1, size):
            comm.send(intervals[otherRank], dest=otherRank)
    else:
        myInterval = comm.recv(source=0)
~~~

It could be rewritten using a scatter collective operation like this:

~~~ {.python}
    myInterval = comm.scatter(intervals, root=0)
~~~

The _intervals_ list must have the same number of elements as there are processes in the communicator used, which is the case here.

At the end, the reverse operation looks like a gathering. We want to get all data back to rank 0 so it can sum the partial sums. This is the code we had previously:

~~~ {.python}
    if rank == 0:
        pi = partial_pi
        for otherRank in range(1, size):
            pi += comm.recv(source=otherRank)
    else:
        comm.send(partial_pi, dest=0)
~~~

Which can be replaced with the following:

~~~ {.python}
    partial_sums = comm.gather(partial_pi, root=0)
    if rank == 0:
        pi = sum(partial_sums)
~~~

Note that partial_sums will be a list of all partial_pi on rank 0 and None on all other ranks.

#### Reduction

As we have seen previously, certain operations, like summing values from all processes, are called reductions. What we have done so far is called a manual reduction and might not be the most effective way to do it. Imagine having 10s of millions of elements to sum: would it be wise to send every single value to one single rank, and sum them while other processes just sit there and wait? Reduction, as implemented in most MPI libraries, have (hidden) strategies for such cases.

Let's have a look at the way we do it now:

~~~ {.python}
    partial_sums = comm.gather(partial_pi, root=0)

    if rank == 0:
        pi = sum(partial_sums)
~~~

This could be done efficiently, on many processes, using a reduction operation:

~~~ {.python}
    pi = comm.reduce(partial_pi, op=MPI.SUM, root=0)
~~~

This statement basically means: sum all partial_pi variables and make the result available on rank 0. Running it yields the same result, in about the same run time.

~~~ {.input}
$ mpirun -np 4 python approx_pi_mpi.py 100000000
~~~
~~~ {.output}
PI is approximately 3.1415926435898172, Error is 0.0000000099999760
Time = 8.9309309005737305 sec
~~~

Note that, currently, the mpi4py implementation of the reduction operations are done naively and would do exactly what we did previously: gather everything on one rank and sum there. The advantage of using the reduction operation today is that the code is shorter, clearer, and that you will benefit from it once it is implemented in mpi4py without changing anything.

> ## Dot-product {.challenge}
>
> Implement a MPI dot product.
>
> 1. Rank 0 must initialize the two input vectors a and b where a = [1..n] and b = [n..1]
> 2. Use the scatter algorithm to split the data between processes.
> 3. Use the reduce algorithm to compute the final result.
>
> __Alternative__: In point 3, use the gather algorithm and let rank 0 compute the final result.
>
> A possible solution can be found in the solutions/dot_product.py file.
