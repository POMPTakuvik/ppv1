/*
 *  qaa4ppSW.h
 *
 *      Compute IOPs from rrs using Quasi-Analytic Algorithm
 *
 *  Naval Research Laboratory
 *  Stennis Space Center, MS
 */
// Pour SeaWiFS

#ifndef _QAASW_H
#define _QAASW_H
#include "qaa.h"
int qaaSW( float Rrs[NBANDS],float a[NBANDS],float bb[NBANDS] );
#endif

