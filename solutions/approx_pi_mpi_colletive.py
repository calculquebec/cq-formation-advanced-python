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
    
    intervals = None
    if rank == 0:
        n = int(sys.argv[1])
        chunk_size = n/size
        intervals = map(lambda p: [p*chunk_size, p*chunk_size+chunk_size], range(size))
        intervals[-1][1] = max(intervals[-1][1], n)

    myInterval = comm.scatter(intervals, root=0)
    partial_pi = approx_pi(myInterval)
    partial_sums = comm.gather(partial_pi, root=0)

    if rank == 0:
        pi = sum(partial_sums)
        t2 = time.time()
        print("PI is approximately %.16f, Error is %.16f"%(pi, abs(pi - math.pi)))
        print("Time = %.16f sec\n"%(t2 - t1))
