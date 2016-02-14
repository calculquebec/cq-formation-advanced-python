#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

double approx_pi(int);

int main(int argc, char *argv[])
{
    clock_t t1 = clock();
    int n = atoi(argv[1]);
    double pi = approx_pi(n);
    clock_t t2 = clock();
    printf("PI is approximately %.16f, Error is %.16f\n",
	   pi, fabs(pi - M_PI));
    printf("Time = %.16f sec\n", (double)(t2 - t1)/CLOCKS_PER_SEC);
    return 0;
}

double approx_pi(int intervals)
{
     double pi = 0.0;
     int i;
     for (i = 0; i < intervals; i++) {
         // Note: using "float" instead of "double" is a little faster here
         pi += (4 - ((i % 2) * 8)) / (double)(2 * i + 1);
     }
     return pi;
}
