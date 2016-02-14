import sys
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size < 2:
    sys.exit(-1)

if rank == 0:
    
    A = np.array([1.0, 2.0])
    B = np.empty(2)

    # Send and Receive
    comm.Send(A, dest=1, tag=10)
    comm.Recv(B, source=1, tag=20)
    print("Process %d sent     A=[%f, %f]"%(rank, A[0], A[1]))
    print("Process %d received B=[%f, %f]"%(rank, B[0], B[1]))

if rank == 1:

    A = np.empty(2)
    B = np.array([3.0, 4.0])

    # Send and Receive
    comm.Recv(A, source=0, tag=10)
    comm.Send(B, dest=0, tag=20)
    print("Process %d sent     B=[%f, %f]"%(rank, B[0], B[1]))
    print("Process %d received A=[%f, %f]"%(rank, A[0], A[1]))


