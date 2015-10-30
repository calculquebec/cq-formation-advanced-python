/* approx_pi_swig.i */
/*  Example of wrapping approx_pi using SWIG. */
%module approx_pi_swig
%{
    /* the resulting C file should be built as a python extension */
    #define SWIG_FILE_WITH_INIT
    /*  Includes the header in the wrapper code */
    #include "approx_pi.h"
%}
/*  Parse the header file to generate wrappers */
%include "approx_pi.h"

