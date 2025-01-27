/* *
 *  @file qaa4ppSW.c
 *  @brief Quasi-Analytic Algorithm for SeaWiFS
 *  @author Paul Martinolich
 *  @author Naval Research Laboratory, Stennis Space Center, MS
 *
 *  This code implements version 5 of the QAA algorithm which
 *  was based on the original algorithm  Lee, at al (2002)
 *  "Deriving inherent optical properties from water color:  A
 *  multi-band quasi-analytical algorithm for optically deep water"
 *  <em>Applied Optics, (41) 27, 5755-5772</em>, 2002
 *
 *  The version 4 update was presented as Appendix A in the paper
 *  Lee, et al (2007) "Euphotic zone depth:  Its derivation and
 *  implication to ocean-color remote sensing" <em>Journal of
 *  Geophysical Research, Vol 112</em>, C03009, doi:10,1029/2006JC003802.
 *
 *  The 5th version was provided by Dr. Lee.
 *
 *  Additional routines are used to initialize indices and other parameters
 *  with the goal to make the code generic for use in SeaWiFS/MODIS processing
 *  as well as hyperspectral data from an ASD or PHILLS.
 *
 *  Likewise, the code duplicates routines for float or double type
 *  variables.  The 'float' routines have an 'f' after the 'qaa'
 *  prefix.
 *
 *  The following code example shows a example of running the QAA
 *  algorithm on SeaWiFS data (with notes on how to run it for other
 *  sensor and using the 670nm path or chl path).
 *
 *  @code
 *  #include "qaa.h"
 *  #define NBANDS 7
 *  // inputs
 *  int   idx410  = 0;
 *  int   idx440  = 1;
 *  int   idx490  = 2;
 *  int   idx555  = 3;
 *  int   idx670  = 4;
 *
 *  // SeaWiFS wavelengths (nm)
 *  double wl[NBANDS] = { 412, 443, 490, 555, 670 };
 *
 *  // SeaWiFS band-averaged pure water absorption
 *  double aw[NBANDS] = { 0.004641, 0.007095, 0.0015267, 0.032599, 0.4456 };
 *
 *  // SeaWiFS band-averaged pure water backscattering coefficient
 *  double bbw[NBANDS] = { 0.003272, 0.002421, 0.001568, 0.0009394, 0.0004261 };
 *
 *  double Rrs[NBANDS];
 *
 *  // temporary space
 *
 *  double u[NBANDS], buf[4*NBANDS];
 *
 *  // outputs
 *
 *  double rrs[NBANDS];
 *  double a[NBANDS], bb[NBANDS], adg[NBANDS], aph[NBANDS];
 *
 *  // read input Rrs
 *
 *  qaa_init( idx410, idx440, idx490, idx555, idx670);
 *
 *  // set the S parameter (default is 0.015)
 *  qaa_set_param( QAA_S_PARAM, 0.011 );
 *
 *  // set the 640 coefficients which differ based on sensor
 *  // qaa_set_param( QAA_COEFS_PARAM, -1.192, -1.230, -0.362 ); // MODIS
 *  // qaa_set_param( QAA_COEFS_PARAM, -1.226, -1.214, -0.350 ); // SeaWiFS (default)
 *  // qaa_set_param( QAA_COEFS_PARAM, -1.295, -1.158, -0.284 ); // MERIS
 *
 *  // run QAA using chl reference and decompose a into adg and aph components
 *  qaa_v5( NBANDS, wl, Rrs, rrs, u, buf, a, bb, flags );
 *  qaa_decomp( NBANDS, wl, rrs, a, adg, aph, flags );
 *
 *  // write out results
 *
 *  @endcode
 */

#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <assert.h>
#include "qaa4ppSW.h"

static int idx410 = -1;
static int idx440 = -1;
static int idx490 = -1;
static int idx555 = -1;
static int idx670 = -1;
static int initialized  = 0;
static int aph_check = 1;
static double S = 0.015;
/*static double chl = -1;*/
static double acoefs[3];

/* *
 *  @brief determine if qaa algorithm properly initialized
 *  @returns 1 if qaa_init has been previously called; 0, otherwise
 */

int
qaa_is_initialized( void )
{
    return initialized;
}

/* *
 *  @brief initalize Quasi-Analytical Algorithm v4
 *  @param[in] i410   0-relative index in spectrum of 410 nm
 *  @param[in] i440   0-relative index in spectrum of 440 nm
 *  @param[in] i490   0-relative index in spectrum of 490 nm
 *  @param[in] i555   0-relative index in spectrum of 555 nm
 *  @param[in] i670   0-relative index in spectrum of 670 nm
 *
 *  This routine should be called to initialize various parameters that may
 *  be adjusted in the QAA algorithm or that must be known apriori.  For example,
 *  the user must supply the indices for various required band numbers and
 *  whether to perform the iteration in the QAA-555 algorithm (normally yes).
 */

int
qaa_init( int i410, int i440, int i490, int i555, int i670 )
{
    idx410 = i410;
    idx440 = i440;
    idx490 = i490;
    idx555 = i555;
    idx670 = i670;

//  SeaWiFS coefficients

    acoefs[0] = -1.146;
    acoefs[1] = -1.366;
    acoefs[2] = -0.469;

    initialized = 1;

    return 0;
}

/**
 *  @brief set a parameter for Quasi-Analytical Algorithm
 *  @param[in] param  name of parameter
 *  @param[in] value  value
 *
 *  This routine should be called to initialize various parameters that may
 *  be adjusted in the QAA algorithm or that must be known apriori.  For example,
 *  the user must supply the indices for various required band numbers.  Optionally,
 *  the user may define there own values for some parameters, like S.
 *
 *  Presently the only parameter the user may set is the S value.
 

int
qaa_set_param( int param, ... )
{
    va_list  ap;
    va_start( ap, param );
    switch (param) {
    case QAA_S_PARAM:
        S = va_arg(ap,double);
        break;
    case QAA_CHL_PARAM:
        chl = va_arg(ap,double);
        break;
    case QAA_COEFS_PARAM:
        acoefs[0] = va_arg(ap,double);
        acoefs[1] = va_arg(ap,double);
        acoefs[2] = va_arg(ap,double);
        break;
    case QAA_APH_CHECK:
        aph_check = va_arg(ap,int);
        break;
    }
    va_end(ap);
    return 0;
}*/

/**
 *  @brief Quasi-Analytical Algorithm v4
 *  @param[in]   nbands   number of bands in spectrum
 *  @param[in]   wavel    wavelength of spectrum (nbands)
 *  @param[in]   Rrs      above-water remote sensing reflectance (nbands)
 *  @param[in]   aw       pure-water absorption (nbands)
 *  @param[in]   bbw      pure-water back scattering (nbands)
 *  @param[out]  rrs      below-water remote sensing reflectance (nbands)
 *  @param[out]  u        ratio (nbands)
 *  @param[out]  a        total absorption (nbands)
 *  @param[out]  bb       backscattering (nbands)
 *  @param[in|out] flags  flags to indicate quality (will be modified)
 *
 *  This implements version 4 of the Quasi-Analytical Algorithm.
 */

int
qaa_v5( int nbands, double *wavel, double *Rrs, double *aw, double *bbw,
         double *rrs, double *u, double *a, double *bb, unsigned char *flags  )
{

    const double g0 = 0.08945;
    const double g1 = 0.1247;

    int     i;

    double  rat, a555;
    double  bbp555;
    double  Y;
    double  rho, numer, denom;

    assert( idx440 >= 0 );
    assert( idx490 >= 0 );
    assert( idx555 >= 0 );
    assert( nbands >= 0 );

    /* pre-test 670 */
    if ( (Rrs[idx670] > 20.0*pow(Rrs[idx555],1.5)) ||
         (Rrs[idx670] < 0.9*pow(Rrs[idx555],1.7)) ) {
        Rrs[idx670] = 1.27*pow(Rrs[idx555],1.47) + 0.00018*pow(Rrs[idx490]/Rrs[idx555],-3.19);
        *flags |= 0x02;
    }

    /* Step 0 */
    for ( i = 0; i < nbands; i++ ) {
        rrs[i] = Rrs[i] / (0.52 + 1.7 * Rrs[i] );
        if ( Rrs[i] < 0.0 )
            *flags |= 0x01;
    }

    /* Step 1 */
    for ( i = 0; i < nbands; i++ )
        u[i]   = (sqrt(g0*g0 + 4.0*g1*rrs[i]) - g0) / (2.0 * g1);

    /* Step 2 */
    numer = Rrs[idx440] + Rrs[idx490];
    denom = Rrs[idx555] + 5*Rrs[idx670]*(Rrs[idx670]/Rrs[idx490]);
    rho   = log10( numer / denom );
    rho   = acoefs[0] + acoefs[1]*rho + acoefs[2]*rho*rho;
    a555  = aw[idx555] + pow(10.0,rho);

    /* Step 3 */
    bbp555 = ((u[idx555] * a555) / (1.0 - u[idx555])) - bbw[idx555];

    /* Step 4 */
    rat    = rrs[idx440] / rrs[idx555];
    Y = 2.0 * (1.0 - 1.2 * exp( -0.9*rat) );

    /* Step 5 */
    for ( i = 0; i < nbands; i++ ) {
        bb[i] = bbp555 * pow((wavel[idx555]/wavel[i]),Y) + bbw[i];
        if ( bb[i] < 0.0 )
            *flags |= 0x04;
    }

    /* Step 6 */
    for ( i = 0; i < nbands; i++ ) {
        a[i] = ((1.0 - u[i]) * bb[i]) / u[i];
        if ( a[i] < 0.0 )
            *flags |= 0x08;
    }

    return 0;
}

/**
 *  @brief Quasi-Analytical Algorithm v4
 *  @see qaa_v5()
 */

int
qaaf_v5( int nbands, float *wavel, float *Rrs, float *aw, float *bbw,
          float *rrs, float *u, float *a, float *bb, unsigned char *flags  )
{

    /*const float g0 = 0.08945;
      const float g1 = 0.1247;*/ /* Valeurs originales de SeaDAS */
    const float g0 = 0.0895;
    const float g1 = 0.1247; /* Valeurs de Simon Belanger */
    /*const float g0 = 0.089;
      const float g1 = 0.125; */ /* Valeurs de David Dessailly */
    float   rho, numer, denom;

    float   rat, a555;
    float   bbp555;
    float   Y;

    int     i;

    assert( idx440 >= 0 );
    assert( idx490 >= 0 );
    assert( idx555 >= 0 );
    assert( idx670 >= 0 );
    assert( nbands >= 0 );

    /* pre-test 670 */
    /*if ( (Rrs[idx670] > 20.0*powf(Rrs[idx555],1.5)) ||
         (Rrs[idx670] < 0.9*powf(Rrs[idx555],1.7)) ) {
        Rrs[idx670] = 1.27*powf(Rrs[idx555],1.47) + 0.00018*powf(Rrs[idx490]/Rrs[idx555],-3.19);
        *flags |= 0x02;
	}*/

    /* Step 0 */
    for ( i = 0; i < nbands; i++ ) {
        rrs[i] = Rrs[i] / (0.52 + 1.7 * Rrs[i] );
        if ( Rrs[i] < 0.0 )
            *flags |= 0x01;
    }

    /* Step 1 */
    for ( i = 0; i < nbands; i++ )
        u[i]   = (sqrt(g0*g0 + 4.0*g1*rrs[i]) - g0) / (2.0 * g1);

    /* Step 2 */
    numer = Rrs[idx440] + Rrs[idx490];
    denom = Rrs[idx555] + 5*Rrs[idx670]*(Rrs[idx670]/Rrs[idx490]);
    rho   = log10f( numer / denom );
    rho   = acoefs[0] + acoefs[1]*rho + acoefs[2]*rho*rho;
    a555  = aw[idx555] + powf(10.0,rho);

    /* Step 3 */
    bbp555 = ((u[idx555] * a555) / (1.0 - u[idx555])) - bbw[idx555];

    /* Step 4 */
    rat   = rrs[idx440] / rrs[idx555];
    Y = 2.0 * (1.0 - 1.2 * expf( -0.9*rat) );

    /* Step 5 */
    for ( i = 0; i < nbands; i++ ) {
        bb[i] = bbp555 * pow((wavel[idx555]/wavel[i]),Y) + bbw[i];
        if ( bb[i] < 0.0 )
            *flags |= 0x04;
    }

    /* Step 6 */
    for ( i = 0; i < nbands; i++ ) {
        a[i] = ((1.0 - u[i]) * bb[i]) / u[i];
        if ( a[i] < 0.0 )
            *flags |= 0x08;
    }

    return 0;
}

/**
 *  @brief Quasi-Analytical Algorithm - decomposition of total absorption
 *  @param[in]   nbands   number of bands in spectrum
 *  @param[in]   wavel    wavelength of spectrum (nbands)
 *  @param[in]   rrs      below-water remote sensing reflectance (nbands)
 *  @param[in]   a        total absorption (nbands)
 *  @param[in]   aw       pure-water absorption (nbands)
 *  @param[out]  adg      gelbstuff absorption (nbands)
 *  @param[out]  aph      phytoplankton absorption (nbands)
 *  @param[in|out] flags  flags to indicate quality (will be modified)
 *
 *  This implements Table 3 of the Quasi-Analytical Algorithm.
 *  It decomposes the total absorption into phytoplankton absorption and
 *  gelbstuff absorption.
 *
 *  This implementation adds a consistency check based on the
 *  phytoplankton absorption at 443nm to improve the decomposition
 *  of total absorption.
 */

int
qaa_decomp( int nbands, double *wavel, double *rrs, double *a, double *aw,
            double *adg, double *aph, unsigned char *flags )
{
    int     i;
    double  symbol, x1, x2;
    double  zeta, denom, dif1, dif2;
    double  rat, ag440;
    double  Sr;

    assert( idx410 >= 0 );
    assert( idx440 >= 0 );
    assert( idx555 >= 0 );
    assert( nbands >= 0 );

    /* step 7 */
    rat    = rrs[idx440] / rrs[idx555];
    symbol = 0.74 + ( 0.2 / ( 0.8 + rat ) );

    /* step 8 */
    Sr = S + 0.002 / ( 0.6 + rat );
    zeta = exp( Sr * (wavel[idx440] - wavel[idx410]) );

    /* step 9 */
    denom = zeta - symbol;
    dif1  = a[idx410]  - symbol * a[idx440];
    dif2  = aw[idx410] - symbol * aw[idx440];
    ag440 = (dif1 - dif2) / denom;

    for ( i = 0; i < nbands; i++ ) {
        adg[i] = ag440 * exp( Sr * (wavel[idx440] - wavel[i]));
	aph[i] = a[i] - adg[i] - aw[i];
    }

    /* check aph443 range */

    if ( aph_check ) {
	x1 = aph[idx440] / a[idx440];
	if ( x1 < 0.15 || x1 > 0.6 ) {

	    *flags |= 0x10;
	    x2 = -0.8 + 1.4 * (a[idx440] - aw[idx440])/(a[idx410] - aw[idx410]);
	    if ( x2 < 0.15 ) {
		x2 = 0.15;
		*flags |= 0x20;
	    }
	    if ( x2 > 0.6 ) {
		x2 = 0.6;
		*flags |= 0x40;
	    }

	    aph[idx440] = a[idx440] * x2;
	    ag440 = a[idx440] - aph[idx440] - aw[idx440];

	    for ( i = 0; i < nbands; i++ ) {
	       adg[i] = ag440 * exp( Sr * (wavel[idx440] - wavel[i]));
	       aph[i] = a[i] - adg[i] - aw[i];
	    }

        }
    }
    return 0;
}

/**
 *  @brief Quasi-Analytical Algorithm - decomposition of total absorption
 *  @see qaa_decomp()
 */

int
qaaf_decomp( int nbands, float *wavel, float *rrs, float *a, float *aw,
             float *adg, float *aph, unsigned char *flags )
{
    int    i;
    float  symbol, x1, x2;
    float  zeta, denom, dif1, dif2;
    float  rat, ag440;
    float  Sr;

    assert( idx410 >= 0 );
    assert( idx440 >= 0 );
    assert( idx555 >= 0 );
    assert( nbands >= 0 );

    /* step 7 */
    rat = rrs[idx440] / rrs[idx555];
    symbol = 0.74 + ( 0.2 / ( 0.8 + rat ) );

    /* step 8 */
    Sr = S + 0.002 / ( 0.6 + rat );
    zeta = expf( Sr * (wavel[idx440] - wavel[idx410]) );

    /* step 9 */
    denom  = zeta - symbol;
    dif1  = a[idx410]  - symbol * a[idx440];
    dif2  = aw[idx410] - symbol * aw[idx440];
    ag440 = (dif1 - dif2) / denom;

    for ( i = 0; i < nbands; i++ ) {
        adg[i] = ag440 * expf( Sr * (wavel[idx440] - wavel[i]));
	aph[i] = a[i] - adg[i] - aw[i];
    }

    /* check aph443 range */

    if ( aph_check ) {

        x1 = aph[idx440] / a[idx440];
        if ( x1 < 0.15 || x1 > 0.6 ) {

            *flags |= 0x10;

            x2 = -0.8 + 1.4 * (a[idx440] - aw[idx440])/(a[idx410] - aw[idx410]);
            if ( x2 < 0.15 ) {
                x2 = 0.15;
                *flags |= 0x20;
            }
            if ( x2 > 0.6 ) {
                x2 = 0.6;
                *flags |= 0x40;
            }

            aph[idx440] = a[idx440] * x2;
            ag440 = a[idx440] - aph[idx440] - aw[idx440];

            for ( i = 0; i < nbands; i++ ) {
                adg[i] = ag440 * expf( Sr * (wavel[idx440] - wavel[i]));
                aph[i] = a[i] - adg[i] - aw[i];
            }

        }

    }

    return 0;
}

#ifdef TEST_QAA

#include <stdio.h>

/*
 * to compile:
 * cc -o qaa -g -DTEST_QAA -I. qaa.c -lm
 * ./qaa
 */


/*
static void print_out( int n, float *fwl, float *Rrs, float *rrs, float *u,
           float *a, float *aph, float *adg, float *aw, float *bb, float *bbw )
{

    int i;

    printf("lamda ");
    for ( i = 0; i < n; i++ )
	printf("%9.0f ", fwl[i]);
    printf("\n");

    printf("Rrs : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", Rrs[i]);
    printf("\n");

    printf("rrs : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", rrs[i]);
    printf("\n");

    printf("u   : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", u[i]);
    printf("\n");

    printf("a   : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", a[i]);
    printf("\n");

    printf("aph : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", aph[i]);
    printf("\n");

    printf("adg : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", adg[i]);
    printf("\n");

    printf("aw  : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", aw[i]);
    printf("\n");

    printf("bb  : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", bb[i]);
    printf("\n");

    printf("bbw : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", bbw[i]);
    printf("\n");

}
*/



int qaaSW( float Rrs[NBANDS],float a[NBANDS],float bb[NBANDS] )
{
/*  if(argc != 7){
    printf("lancer avec en arguments les Rrs a  412, 443, 490, 510, 555, 670 :\n");
    printf(" qaaLOG 0.001753 0.002657 0.004348 0.005212 0.007641 0.003950\n");
    exit(-1);
  }*/
    /* the 5th position here will be changed for 640nm later down in code */


    /*    412       443       490       510       555       670 */

    float fwl[NBANDS] ={ 412,      443,      490,      510,      555,       670 };
    float aw[NBANDS] = AW_SEAWIFS;
    float bbw[NBANDS] = BBW_SEAWIFS;
    float aph[NBANDS];
    int   i;
    float rrs[NBANDS];
    float u[NBANDS];
/*    float aph[NBANDS];*/
    float adg[NBANDS];
    unsigned char flags;

    int   idx410 = 0;
    int   idx440 = 1;
    int   idx490 = 2;
    int   idx555 = 4;
    int   idx670 = 5;
    int   nbands;

    // Ping's bbw using 0.0038 * pow((400.0/lambda),4.32);
    for ( i = 0; i< NBANDS; i++ )
        bbw[i] = 0.0038 * pow(400.0/fwl[i],4.32);

    qaa_init( idx410, idx440, idx490, idx555, idx670 );
/*     qaa_set_param( QAA_APH_CHECK, 0 );*/

/*    printf("QAA v5\n" );
    for ( j = 0; j < NUM_SPECTRA; j++ ) {*/

    flags  = 0;
    nbands = NBANDS;
    /* 412 to 670 
    for ( i = 0; i < nbands; i++ )
        Rrs[i] = Rrs_insitu[j][i];*/


    qaaf_v5( nbands, fwl, Rrs, aw, bbw, rrs, u, a, bb, &flags );
    qaaf_decomp( nbands, fwl, rrs, a, aw, adg, aph, &flags );
    
/*    for ( i = 0; i < 6; i++ )
      printf("%.6f ",a[i]);
    for ( i = 0; i < 6; i++ )
      printf("%.6f ",bb[i]);
    printf("\n");*/
    
  /*for ( i = 0; i < 6; i++ )
	    if ( a[i] < aw[i] )
		flags |= 0x08;

	for ( i = 0; i < 6; i++ )
	    if ( bb[i] < bbw[i] )
		flags |= 0x80;

 	print_out( nbands, fwl, Rrs, rrs, u, a, aph, adg, aw, bb, bbw );

	if ( flags & 0x10 )
	    printf("original aph/a ratio was out of range (0.15 to 0.6)\n");
	if ( flags & 0x20 )
	    printf("    and was forced to minimum (0.15)\n");
	if ( flags & 0x40 )
	    printf("    and was forced to maximum (0.6)\n");
	printf("\n");*/
    /*}*/

    return 0;
}
#endif

