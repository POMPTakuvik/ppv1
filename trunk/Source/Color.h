/* ==================================================================
 Color.h
 
 author: Maxime Benoit-Gagne - Takuvik - Canada.
 date of creation: January 20, 2016.
 
 compiler:
 $ gcc -v
Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1
Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)
Target: x86_64-apple-darwin12.6.0
Thread model: posix
 
 description: Color.h is a header for general functions in Color.c.
 
 uses: 
 
 keywords: ...
 
 ================================================================== */

#ifndef _Color_h
#define _Color_h

/* ====================== CONSTANTS ====================== */
/*
 * Number of limits of the time intervals:		   
 * 0 to 24h by step of 3h.                                 
 */
#define NTIMES 9

/*
 * Number of bands in the visible spectrum for SeaWiFS and MODIS.
 */
#define NBANDS 6

/* ====================== PROTOTYPES ====================== */

/*
 * IN
 * time:
 *  Time. Between 0 and 24.
 *  Units: h.
 * Return the index of the time in the array of the hours from 0 to 24 by step 
 * of 3 h.
 */
int get_itime(float time);

#endif
