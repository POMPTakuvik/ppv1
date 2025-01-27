/*
 * takuvik.h
 * Maxime Benoit-Gagne
 * August 22nd, 2012
 *
 * compiler:
 * $ gcc -v
 * Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1
 * Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)
 * Target: x86_64-apple-darwin12.6.0
 * Thread model: posix
 *
 * takuvik.h is a header for general functions in takuvik.c.
 */

#ifndef _takuvik_h
#define _takuvik_h

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#ifndef MAX
#define MAX(A,B)    ((A) > (B) ? (A) : (B))  /* Greater of (A,B) */ 
#endif

#ifndef MIN
#define MIN(A,B)    ((A) < (B) ? (A) : (B))  /* Lesser  of (A,B) */
#endif

/*
 * See the ISO C standard at
 * http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf at page 26.
 * 1E-5.
 */
#define MY_FLT_EPSILON 0.00001

/*
 * a1: An array (1d) of float.
 * a2: An array (1d) of float.
 * n : The length of a1 and a2.
 * Return
 *  different than 0 if a1 is different than a2 for indices 0 to n - 1.
 *  0 if a1 is equal to a2 for indices 0 to n - 1.
 *  The epsilon used is the ISO C standard float epsilon 1E-5.
 */
int array1dfcmp(float* a1, float* a2, int n);

/*
 * m : The length of the first dimension of a1 and a2.
 * n : The length of the second dimension of a1 and a2.
 * a1: An array (2d) of float.
 * a2: An array (2d) of float.
 * Return
 *  different than 0 if a1 is different than a2.
 *  0 if a1 is equal to a2.
 *  The epsilon used is the ISO C standard float epsilon 1E-5.
 */
int array2dfcmp(int m, int n, float a1[m][n], float a2[m][n]);

/*
 * f1: A float.
 * f2: A float.
 * Return
 * -1 if f1 < f2,
 *  1 if f1 > f2,
 *  0 if f1 = f2.
 * The epsilon used is the ISO C standard float epsilon 1E-5.
 */
int fcmp(float f1, float f2);

/*
 * f1: A float.
 * f2: A float.
 * Return 1 if f1 is greater or equal to f2.
 * The epsilon used is the ISO C standard float epsilon 1E-5.
 * Return 0 if not.
 */
int ge(float f1, float f2);

/*
 * IN
 * ni: The length of the first dimension of array2df_i_j and of the first 
 *     (and only) dimension of array1df_i.
 * nj: The length of the second dimension of array2df_i_j.
 * array2df_i_j: An array (2d) of floats.
 * j_target: An index of the second dimension of array2df_i_j.
 * OUT
 * array1df_i: An array (1d) of floats containing the column at index 
 *             j_target in array2df_i_j.
 *             Exit and print a comprehensive error message if j_target >= nj.
 * Return 0 after a normal execution.
 * Return -1 if not.
 */
int get_array1df_i_from_array2df_i_j(int ni,
				     int nj,
				     float array2df_i_j[ni][nj],
				     int j_target,
				     float array1df_i[ni]);

/*
 * IN
 * lon:
 *  Longitude. Between -180 and 180.
 *  Units: degrees East.
 * Return
 *  The time UTC of the local noon. Between 0 and 24h.
 *  Print a comprehensive error message and exit if lon < -180 or lon > 180.    
 */
float get_timeGMT_local_noon(float lon);

/*
 * f1: A float.
 * f2: A float.
 * Return 1 if f1 is greater than f2.
 * The epsilon used is the ISO C standard float epsilon 1E-5.
 * Return 0 if not.
 */
int gt(float f1, float f2);

/*
 * a1: An array (1d) of float.
 * n : The length of a1.
 * Return
 *  1 if a1[i] >= 0 for all i < n.
 *  0 if not.
 */
int is_array1df_valid(float* a1, int n);

/*
 * INOUT:
 * s:
 *  A string.
 * Add a forward slash at the end of s if there is not one already.
 */
int make_sure_last_character_is_slash(char* s);

/*
 * ar: Array of floats.
 * n:  Length of the array.
 * Return the mean.
 */
float mean(float ar[], int n);

/*
 * ptr_val: A non-empty array of n float numbers.
 * n      : The length of the array.
 * Sort the array and return the median.
 * In case of an even length, the average of the two middle numbers is returned.
 * The behavior is indefinite if the array is empty.
 * TODO:
 *  Implement the QuickSelect method to speed up.
 *  Reference: http://ndevilla.free.fr/median/median/index.html
 *             See the quickselect.c code snippet.
 */
float median_libc_qsort(float *ptr_val, int n);

#endif
