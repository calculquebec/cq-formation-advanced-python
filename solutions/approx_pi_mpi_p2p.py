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
