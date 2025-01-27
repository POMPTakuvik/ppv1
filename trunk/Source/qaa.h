/*
 *  qaa.h
 *
 *      Compute IOPs from rrs using Quasi-Analytic Algorithm
 *
 *  Naval Research Laboratory
 *  Stennis Space Center, MS
 */

#ifndef _QAA_H
#define _QAA_H

#include "Color.h"
#include "params.h"

#define NUM_SPECTRA 23
enum {
     QAA_S_PARAM     = 1,
     QAA_CHL_PARAM   = 2,
     QAA_COEFS_PARAM = 3,
     QAA_APH_CHECK   = 8
};
#endif

