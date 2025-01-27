/*
 * See comments in the header light.h.
 */

/* ============================== INCLUDES ============================== */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "light.h"
#include "sza.h"


/* ====================== CONSTANTS TO MODIFY ====================== */
#define DEBUG_0 0
#define DEBUG_1 1
#define DEBUG DEBUG_0


/* ====================== CONSTANTS ====================== */

#define ITIME_TOMORROW_MIDNIGHT 8


/* ====================== PROTOTYPES ====================== */

extern void ed0moins(int, double rtime, double lat, double lon,
                             double o3, double tcl, double cf,
                             float Ed_pixel[NBWL],
                             float ed_lut[NBWL][NTHETAS][NO3][NTAUCLD][NALB],
                             double thetas);
extern void read_ed0moins_lut_(const char *filename, double ptr[NBWL][NTHETAS][NO3][NTAUCLD][NALB]);
                            
void test_get_array2d_itime_ivis_ed0minus_in(float array2d_itime_ivis_ed0minus[NTIMES][NVIS]);
void test_get_array4d_itaucld_io3_ithetas_iwl_ed0minus(float array4d_itaucld_io3_ithetas_iwl_ed0minus[NTAUCLD][NO3][NTHETAS][NBWL]);

/* ============== GLOBAL VARIABLES (ONLY ARRAYS OF CONSTANTS) ============== */

/*
 * Array of dimension 9.
 * The first dimension is the hours UTC from 0 to 24 by step of 3 h.
 * The values are the hours UTC.
 * The units are hours UTC.
 */
float _ARRAY1D_ITIME_HOUR[NTIMES]={0., 3., 6., 9., 12., 15., 18., 21., 0.};

/* ====================== FUNCTIONS ====================== */

int get_array2d_itime_ivis_ed0minus(float lat,
				    float lon,
				    int doy,
				    float array1d_itime_cf[NTIMES],
				    float array1d_itime_o3[NTIMES],
				    float array1d_itime_taucld[NTIMES],
				    float downward_irradiance_table_as_input[NBWL][NTHETAS][NO3][NTAUCLD][NALB], //array input
				    float array2d_itime_ivis_ed0minus[NTIMES][NVIS]){ // array output
  
  float array1d_iwl_Ed0minus[NBWL]; // output de la fonction ed0moins
  float cf;
  float ed0minus;
  float hour;
  int itime;
  int ivis;
  int iwl;
  float lambda;
  float o3;
  float phi;
  int ret;
  float thetas;
  float taucld;
  int tmpdoy;
  
  /////////// Initialize variables with foo values. ///////////
  for(itime = 0; itime < NTIMES; itime++){
    for(ivis = 0; ivis < NVIS; ivis++){
      array2d_itime_ivis_ed0minus[itime][ivis] = -999.;
    }
  }

  /////////// test if the inputs are valid ///////////
  ret = 0;
  for(itime = 0; itime < NTIMES; itime++){
    cf = array1d_itime_cf[itime];
    o3 = array1d_itime_o3[itime];
    taucld = array1d_itime_taucld[itime];
    if(cf < 0 || o3 < 0 || taucld < 0){
      ret = -1;
    }
  }

  /////////// if the inputs are valid ///////////
  if(!ret){

    /////////// Compute ed0minus ///////////
    /* Loop on time steps of 3 hours. */
    for(itime = 0; itime < NTIMES; itime++){
      ///// Initialize variables with foo values. /////
      for(iwl = 0; iwl < NBWL; iwl++){
	      array1d_iwl_Ed0minus[iwl] = -999.;
      }
      /////////// compute hour ///////////
      hour = _ARRAY1D_ITIME_HOUR[itime];
    
      /////////// compute atmospheric products ///////////
      cf = array1d_itime_cf[itime];
      o3 = array1d_itime_o3[itime];
      taucld = array1d_itime_taucld[itime];
      
      /////////// compute doy ///////////
      if(itime == ITIME_TOMORROW_MIDNIGHT){
        tmpdoy = doy + 1;
       }else{
	      tmpdoy = doy;
      }

  double thetas = sun_zenithal_angle_approximation(tmpdoy, hour, lat, lon);
  

  // Test sunpos
  

  ed0moins(tmpdoy, hour, lat, lon, o3, taucld, cf, array1d_iwl_Ed0minus, downward_irradiance_table_as_input, thetas);
  

      /////////// compute ed0minus(lambda_61, t) ///////////
      for(ivis = 0; ivis < NVIS; ivis++){
	      array2d_itime_ivis_ed0minus[itime][ivis]
	        = array1d_iwl_Ed0minus[I400_FROM_290 + ivis];
      }
    }
    /* Loop on time steps of 3 hours. */
  }

  return ret;
  
}
/* ------------------------------------------------------------------ */

int get_downward_irradiance_table(char* filename,
						 float downward_irriadiance_table_as_output[NBWL][NTHETAS][NO3][NTAUCLD][NALB]){

  read_ed0moins_lut_(filename, downward_irriadiance_table_as_output);
 
  return 0;
}
