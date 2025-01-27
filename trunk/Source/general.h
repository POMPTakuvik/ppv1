/*
 * general.h
 * Maxime Benoit-Gagne
 * November 25, 2014
 *
 * general.h is a header for general functions in general.c.
 */

#ifndef _general_h
#define _general_h

#include <stdlib.h>

/*
 * IN
 * array1d_i_val1:
 *  Array of one dimension = n.
 *  The first dimension is i.
 *  The values are val.
 * array1d_i_val2:
 *  Array of one dimension = n.
 *  The first dimension is i.
 *  The values are val.
 * n:
 *  The length of array1d_i_val1 and array1d_i_val2.
 * Return
 * 0 if all elements are equal.
 * 1 if not.
 * The result is unspecified if both arrays have different lengths.
 *
 */
int compare_arrays_i(const int* array1d_i_val1,
                     const int* array1d_i_val2,
                     int n);

#endif
