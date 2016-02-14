import sys
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size < 2:
    sys.exit(-1)

if rank == 0:
    matrix = np.reshape(np.arange(16), (4,4))
    comm.Send(matrix, dest=1, tag=54321)
    print("Process %d sent matrix="%rank)

if rank == 1:
    matrix = np.empty((4,4), dtype=int)
    comm.Recv(matrix, source=0, tag=MPI.ANY_TAG)
    print("Process %d received matrix="%rank)

if rank < 2:
    for row in matrix:
        print("%2d %2d %2d %2d"%tuple(row))


