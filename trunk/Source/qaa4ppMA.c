/* *
 *  @file qaa4ppMA.c
 *  @brief Quasi-Analytic Algorithm pour MODISA
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
 *  qaa_initMA( idx410, idx440, idx490, idx555, idx670);
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
 *  qaa_v5MA( NBANDS, wl, Rrs, rrs, u, buf, a, bb, flags );
 *  qaa_decompMA( NBANDS, wl, rrs, a, adg, aph, flags );
 *
 *  // write out results
 *
 *  @endcode
 */

#include <stdlib.h>
#include <math.h>
#include <stdarg.h>
#include <assert.h>
#include "qaa4ppMA.h"

static int idx410 = -1;
static int idx440 = -1;
static int idx490 = -1;
static int idx555 = -1;
static int idx670 = -1;
static int initialized  = 0;
static double acoefs[3];

/* *
 *  @brief determine if qaa algorithm properly initialized
 *  @returns 1 if qaa_initMA has been previously called; 0, otherwise
 */

int
qaa_is_initializedMA( void )
{
    return initialized;
}


int
qaa_initMA( int i410, int i440, int i490, int i555, int i670 )
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


int qaaf_v5MA( int nbands, float *wavel, float *Rrs, float *aw, float *bbw,
          float *rrs, float *u, float *a, float *bb, unsigned char *flags  )
{

    /*const float g0 = 0.08945;
      const float g1 = 0.1247;*/ /* Valeurs originales de SeaDAS */
    const float g0 = 0.0895;
    const float g1 = 0.1247; /* Valeurs de Simon Belanger */

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


#ifdef TEST_QAA

#include <stdio.h>

/*
 * to compile:
 * cc -o qaa -g -DTEST_QAA -I. qaa.c -lm
 * ./qaa
 */


/*
static void print_outMA( int n, float *fwl, float *Rrs, float *rrs, float *u,
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

    printf("a   : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", a[i]);
    printf("\n");

     printf("bb  : ");
    for ( i = 0; i < n; i++ )
	printf("%9.6f ", bb[i]);
    printf("\n");

}
*/



int qaaMA( float Rrs[NBANDS],float a[NBANDS],float bb[NBANDS] )
{
/*  if(argc != 7){
    printf("lancer avec en arguments les Rrs a  412, 443, 490, 510, 555, 670 :\n");
    printf(" qaaLOG 0.001753 0.002657 0.004348 0.005212 0.007641 0.003950\n");
    exit(-1);
  }*/
    /* the 5th position here will be changed for 640nm later down in code */


    /*    412       443       490       510       555       670 */

    float fwl[NBANDS] ={ 412,      443,      488,      531,      555,       667 };
    float aw[NBANDS] = AW_MODISA;
    float bbw[NBANDS] = BBW_MODISA;
    int   i;
    float rrs[NBANDS];
    float u[NBANDS];
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

    qaa_initMA( idx410, idx440, idx490, idx555, idx670 );
/*     qaa_set_param( QAA_APH_CHECK, 0 );*/

/*    printf("QAA v5\n" );
    for ( j = 0; j < NUM_SPECTRA; j++ ) {*/

    flags  = 0;
    nbands = NBANDS;
    /* 412 to 670 
    for ( i = 0; i < nbands; i++ )
        Rrs[i] = Rrs_insitu[j][i];*/


    qaaf_v5MA( nbands, fwl, Rrs, aw, bbw, rrs, u, a, bb, &flags );
    
    return 0;
}
#endif

