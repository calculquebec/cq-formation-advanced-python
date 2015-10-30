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

