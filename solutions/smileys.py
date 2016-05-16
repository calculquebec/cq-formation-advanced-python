from mpi4py import MPI
import numpy

smileys = [ ":-|", ":-)", ":-D", ":-P" ]

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = None
if rank == 0:
    data = numpy.arange(8.)
    print "data:", data

myData = numpy.empty(8//4)

comm.Scatter(data, myData, root=0)

print "rank ", rank, "data:", myData
