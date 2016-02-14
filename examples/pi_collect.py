import sys
import math
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

while True:
    if rank == 0:
        sys.stdout.write("Enter the number of intervals (0 quits) : ")
        n = int(input())
        if n > 0:
            print("-> %d iterations"%n)
        else:
            print("done");
        t1 = MPI.Wtime()
    else:
        n = None

    n = comm.bcast(n, root=0)
    if n == 0:
        break

    sum = 0.0
    i = n - 1 - rank
    while i >= 0:
        sum += (4.0 - 8.0 * (i % 2)) / (2.0 * i + 1)
        i -= size

    pi = comm.reduce(sum, op=MPI.SUM, root=0)

    if rank == 0:
        t2 = MPI.Wtime()
        print("PI is approximately %.16f, Error is %.16f"%(pi, abs(pi - math.pi)))
        print("Time = %.16f sec\n"%(t2 - t1))


