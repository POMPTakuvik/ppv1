/* ================================================================== 
  test_subroutine_Ed0moins_at_pixel.c
  
  Created by Maxime Benoit-Gagne on 2017-05-19.
  Takuvik - Canada.
  
  compiler:
  $ gcc -v
  Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1
  Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)
  Target: x86_64-apple-darwin12.6.0
  Thread model: posix
  
  usage:
  ./test_subroutine_Ed0moins_at_pixel.c
  
  description: Test from the trace of the second test in 
  get_array1d_idepth_pp.c.
  
  uses: 
  
  keywords: example
  ================================================================== */

#include <stdio.h>
#include <stdlib.h>

#include "takuvik.h"

#define ID400 22 /* emplacement de lambda 400 dans les longeurs d'onde 290-700*/

/*
 * LUT provided by Simon Belanger (UQAR) on 2011.
 * Dimensions: Wavelength(83) * TauCld(8) * Ozone(8) * Thetas(19)
 * In row-major order.
 * (See https://en.wikipedia.org/wiki/Row-_and_column-major_order)
 */
#define LUT "../Inputs/Ed0moins_LUT.dat"
/*
 * Number of wavelengths from 290 to 700 nm by step of 5 nm.
 */
#define NBWL 83
/*
 * 8 values for total ozone column from 200 to 550, in Dobson units (DU) at
 * every 50 DU.
 */
#define NO3 8
/*
 * 8 values of optical thickness from 0 to 64,
 * i.e. 0, 1, 2,4, 8, 16, 32 and 64.
 */
#define NTAUCLD 8
/*
 * 19 different values for sun's zenith angle from 0 to 90 degrees at every
 * 5 degrees.
 */
#define NTHETAS 19

/* ====================== EXTERNAL FUNCTIONS ====================== */

/* Function of : subroutine_Ed0moins_at_pixel.f */
extern void ed0moins_(int *jday,
		      float *rtime,
		      float *lat,
		      float *lon,
		      float *o3,
		      float *tcl,
		      float *cf,
		      float Ed_pixel[NBWL],
		      float *ed_lut,
		      float *thetas);
extern void read_ed0moins_lut_(int* lutname_length,
			       char *lut_fic,
			       float *ed_lut);

/* ================================= MAIN ================================= */

int main(int argc, char *argv[]){
  
  char errmsg[] = "Bad number of arguments.\n"
  "Usage:\n"
  "./test_subroutine_Ed0moins_at_pixel.c\n";
  
  /////////// Declaration of the variables. ///////////
  int doy;
  float hour;
  float lat;
  float lon;
  float o3;
  float taucld;
  float cf;
  /*
   * Array of dimensions NBWL = 83.
   * The first dimension are the wavelengths from 290 to 700 by step 5 nm.
   * The values are the downward irradiance just below the water surface.
   * The units are umol photons*m^-2*s^-1*nm^-1. 
   */
  float array1d_iwl_Ed0minus[NBWL];
  float* ptr_array4d_itaucl_io3_ithetas_iwl_ed0minus;
  /*
   * Solar zenith angle.
   * Units: Degrees.
   */
  float thetas;
  int iwl;
  int lutname_length = 500;
  float ed0moins_ref = 0.680771052;
  float ed0moins;
  
  /////////// Verification of the arguments. ///////////
  if(argc != 1){
    printf("%s", errmsg);
    return -1;
  }

  /////////// Test. ///////////
  doy = 233;
  hour = 0.;
  lat = 68.767860;
  lon = -104.884529;
  o3 = 276.799988;
  taucld = 5.520000;
  cf = 0.582200;
  ///// Initialize variables with foo values. /////
  for(iwl = 0; iwl < NBWL; iwl++){
    array1d_iwl_Ed0minus[iwl] = -999.;
  }  
  // Memory allocation.
  ptr_array4d_itaucl_io3_ithetas_iwl_ed0minus
    = (float*) malloc(sizeof(float) * NTAUCLD * NO3 * NTHETAS * NBWL);
  // read LUT
  read_ed0moins_lut_(&lutname_length,
		     LUT,
		     ptr_array4d_itaucl_io3_ithetas_iwl_ed0minus);
  thetas = 73.731125;

  /////////// compute ed0minus(lambda_83) ///////////
  ed0moins_(&doy,
	    &hour,
	    &lat,
	    &lon,
	    &o3,
	    &taucld,
	    &cf,
	    array1d_iwl_Ed0minus,
	    ptr_array4d_itaucl_io3_ithetas_iwl_ed0minus,
	    &thetas);

  /////////// compare ///////////
  ed0moins = array1d_iwl_Ed0minus[1 + ID400];
  //printf("ed0moins: %f\n", ed0moins);
  if(fcmp(ed0moins, ed0moins_ref) == 0){
    printf("PASS\n");
  }else{
    printf("FAIL\n");
  }
  
  /////////// Return. ///////////
  return 0;
}
