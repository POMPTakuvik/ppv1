/* =========================================================================
 get_array1d_idepth_pp.c
 
 author: Maxime Benoit-Gagne
 - Takuvik - Canada.
 
 compiler:
 $ gcc -v
 Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1
 Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)
 Target: x86_64-apple-darwin12.6.0
 Thread model: posix
 
 usage:
 ./get_array1d_idepth_pp
 
 description:
 Test function get_array1d_idepth_pp in get_array1d_idepth_pp.c.
 
 uses: TODO
 
 keywords: test
 
 ============================================================================ */

/* ============================== INCLUDES ============================== */

#include <assert.h>
#include <limits.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "Color.h"
#include "DepthAPI.h"
#include "general.h"
#include "light.h"
#include "qaa4ppMA.h"
#include "qaa4ppSW.h"
#include "rscalc.h"
#include "takuvik.h"
#include "sza.h"

/* ====================== CONSTANTS TO MODIFY ====================== */
/* Print ? */
#define DEBUG_0 0
/* Print a minimal output. */
#define DEBUG_1 1
/* Print a maximal output. */
#define DEBUG_2 2
/* Type of the wished output. */
#define DEBUG DEBUG_0

/* ====================== CONSTANTS ====================== */

/* Coefficient A_phi(lambda) derive empiriquement pour la loi de puissance
 * servant a calculer a_phi(lambda), le coefficient d'absorption du
 * phytoplancton selon Matsuoka et al. 2007 tableau 2.
 */
#define A_PHI_443 0.0288
/*
 * The value of the option chl to use the chlorophyll-a concentration 
 * vertical profile in the water column.
 */
#define CHL_COLUMN 1
/*
 * The value of the option chl to use the surface chlorophyll-a concentration.
 */
#define CHL_SURFACE 0
/*
 * Difference between two depths.
 * Units: m.
 */
#define DEPTH_STEP 1.
/* Coefficient E_phi(lambda) derive empiriquement pour la loi de puissance
 * servant a calculer a_phi(lambda), le coefficient d'absorption du
 * phytoplancton selon Matsuoka et al. 2007 tableau 2.
 */
#define E_PHI_443 0.82
#define KD700_PURE_WATER 0.624 /* Kd(700)=0.62 from Morel for pure water */
/* Index of the 555 nm band in SeaWiFS and MODIS. */
#define I555 4
#define ID400 22 /* emplacement de lambda 400 dans les longeurs d'onde 290-700*/
/* emplacement de lambda 490 dans les longueurs d'onde de SeaWiFS */
#define I490SW 2
/* emplacement de lambda 490 dans les longueurs d'onde 400-700 */
#define I490_FROM400 18
#define INTERVALLE_TEMPS_ISCCP 3.
#define ITIME_TOMORROW_MIDNIGHT 8
/*
 * Depth to which the primary productivity is computed if the bathymetry
 * allows it.
 * Units: m.
 */
#define MAX_DEPTH 100.
#define MODISA 'A'
/*
 * Number of geometric depths.
 * The geometric depths are from 0 to 100 by step 1.
 * Units: m.
 */
#define NBDEPTHS 101
#define NBTHETAS 3
#define SEAWIFS 'S'

/* =================  TYPEDEF AND STRUCT  ============================ */
/*
 * shallow if depth < max_depth,
 * deep if not.
 */
typedef enum {deep, shallow} deep_or_shallow_type;

/*
 * Pixel with information about the water.
 */
typedef struct PixelWater{
  /*
   * Latitude.
   * The units are degrees North.
   */
  float lat;
  /*
   * Longitude.
   * From -180 to 180.
   * The units are degrees East.
   */
  float lon;
  int year;
  int month;
  /* Day of month. */
  int day;
  /* Day of year. */
  int doy;
  /*
   * Bathymetry.
   * The units are m.
   */
  float depth;
  /*
   * S for SeaWiFS and A for MODIS-AQUA.
   */
  char rrs_type;
  /*
   * Array of dimension NBANDS = 6.
   * The first dimension are the wavelengths of the bands of the satellite.
   * The values are the remote-sensing reflectances.
   * The units are sr^-1.
   */
  float* ptr_array1d_iband_Rrs;
  /*
   * Array of dimension NBDEPTHS = 101.
   * The first dimension is the index of the geometric depths.
   * The geometric depths are from 0 to 100 by step 1. Units: m.
   * The values are the chlorophyll-a concentration.
   * The units are mg Chl-a m^-3.
   */
  float* ptr_array1d_idepth_chl;
  /*
   * Array of dimension NBDEPTHS - 1 = 100.
   * The first dimension is the index of the geometric depths.
   * The geometric depths are from 0 to 100 by step 1. Units: m.
   * The values are the primary productivities.
   * Units: mgC.m^-2.d^-1.
   */
  float* ptr_array1d_idepth_pp;
} PixelWater;

/* ====================== EXTERNAL FUNCTIONS ====================== */
/* Function of : subroutine_Ed0moins_at_pixel.f */
// extern void sunpos_(int *jday,
// 		    float *rtime,
// 		    float *lat,
// 		    float *lon,
// 		    float *thetas,
// 		    float *azim);

/* ====================== PROTOTYPES ====================== */

void calc_aphy(float aphy443[NBDEPTHS],
               int idepth_max,
               float vis_aphy[NBDEPTHS][NVIS]);
void calc_aphy443(float array1d_idepth_chl[NBDEPTHS],
                  int idepth_max,
                  float aphy443[NBDEPTHS]);
void calc_array1d_iprof_PUR(float array2d_idepth_ivis_E0[NBDEPTHS][NVIS],
                            float vis_aphy[NBDEPTHS][NVIS],
                            float aphy443[NBDEPTHS],
                            int idepth_max,
                            float array1d_iprof_PUR[NBDEPTHS]);
void calc_Ek(float Ek[NBDEPTHS],
             float meanPUR[NBDEPTHS],
             int idepth_max);
void calc_kdsimon(float a[NVIS],
                  float bb[NVIS],
                  float Kd[NVIS],
                  float thetas);
void calc_meanPUR(float PUR[NBDEPTHS][NTIMES],
                  float meanPUR[NBDEPTHS],
                  float photoperiode,
                  int idepth_max);
float calc_PP_down_to_depth(float array1d_idepth_chl[NBDEPTHS],
                            float array2d_idepth_itime_pur[NBDEPTHS][NTIMES],
                            float array1d_idepth_ek[NBDEPTHS],
                            float array1d_idepth_depthphy[NBDEPTHS],
                            int array1d_itime_idepth_max[NTIMES],
                            float array1d_idepth_pp[NBDEPTHS - 1]);
void calc_PUR(float array2d_iprof_h_PUR[NBDEPTHS][NTIMES],
              float array2d_idepth_ivis_E0[NBDEPTHS][NVIS],
              int h,
              float vis_aphy[NBDEPTHS][NVIS],
              float aphy443[NBDEPTHS],
              int idepth_max);
void calc_Z(int nb_depths, float depth_step, float Z[NBDEPTHS]);

void get_array1d_iband_atotal_lee2002(PixelWater p,
				      float array1d_iband_atotal[NBANDS]);
void get_array1d_iband_bbtotal_lee2002(PixelWater p,
				       float array1d_iband_bbtotal[NBANDS]);
void get_array1d_ivis_bbtotal_lee2002(PixelWater p,
				      float array1d_ivis_bbtotal_lee2002[NVIS]);
void get_array1d_ivis_value(float array2d_idepth_ivis_value[NBDEPTHS][NVIS],
			    int idepth,
			    float array1d_ivis_value[NVIS]);
void get_array1d_idepth_bbp555(float array1d_idepth_chl[NBDEPTHS],
                               int idepth_max,
                               float array1d_idepth_bbp555[NBDEPTHS]);
void get_array1d_idepth_bbtotal555(float array1d_ivis_bbw[NVIS],
                                   float array1d_idepth_bbp555[NBDEPTHS],
                                   int idepth_max,
                                   float array1d_idepth_bbtotal555[NBDEPTHS]);
void get_array1d_idepth_gamma(float array1d_idepth_bbtotal555[NBDEPTHS],
                              int idepth_max,
                              float array1d_idepth_gamma[NBDEPTHS]);
void get_array1d_idepth_PAR(float array2d_idepth_ivis_Ed[NBDEPTHS][NVIS],
                            int idepth_max,
                            float array1d_idepth_PAR[NBDEPTHS]);
void get_array1d_idepth_PAR_local_noon(int idepth_max,
                                       float array2d_idepth_ivis_Ed
                                       [NBDEPTHS][NVIS],
                                       float array1d_idepth_PAR_local_noon
                                       [NBDEPTHS]);
void get_array1d_idepth_pp(float array2d_itime_ivis_Ed0minus
                           [NTIMES][NVIS],
                           float lat,
                           float lon,
                           int year,
                           int month,
                           int day,
                           int doy,
                           float depth,
                           char rrs_type,
                           float array1d_iband_Rrs
                           [NBANDS],
                           float array1d_idepth_chl
                           [NBDEPTHS],
                           float array1d_idepth_pp
                           [NBDEPTHS - 1]);
void get_array1d_idepth_pp_from_atm(float lat,
				    float lon,
				    int year,
				    int month,
				    int day,
				    int doy,
				    float depth,
				    char rrs_type,
				    float array1d_iband_Rrs[NBANDS],
				    float array1d_idepth_chl[NBDEPTHS],
				    float array1d_itime_cf[NTIMES],
				    float array1d_itime_o3[NTIMES],
				    float array1d_itime_taucld[NTIMES],
				    float downward_irradiance_table[NBWL][NTHETAS][NO3][NTAUCLD][NALB],
				    float array1d_idepth_pp[NBDEPTHS - 1]);
void get_array1d_idepth_pp_from_PixelWater_and_light(float array2d_itime_ivis_Ed0minus
                                                     [NTIMES][NVIS],
                                                     PixelWater p);
void get_array1d_idepth_ppin(float array2d_idepth_itime_pp
                             [NBDEPTHS - 1][NTIMES - 1],
                             float array1d_idepth_pp[NBDEPTHS - 1]);
void get_array1d_iband_aCDOM(float array1d_iband_atotal[NBANDS],
                             float array1d_iband_aw[NBANDS],
                             float array2d_idepth_iband_aphy[NBDEPTHS][NBANDS],
                             float array1d_iband_aCDOM[NBANDS]);
void get_array1d_ivis_atotal_lee2002(PixelWater p,
				     float array1d_ivis_atotal_lee2002[NVIS]);
void get_array1d_ivis_Ed(float array2d_idepth_ivis_Ed[NBDEPTHS][NVIS],
                         int idepth,
                         float array1d_ivis_Ed[NVIS]);
void get_array1d_ivis_from_iband(float array1d_iband_val[NBANDS],
				 char rrs_type,
				 float array1d_ivis_val[NVIS]);
void get_array2d_idepth_ivis_atotal(float array1d_ivis_atotal_lee2002[NVIS],
				    float array2d_idepth_ivis_aphy
				    [NBDEPTHS][NVIS],
				    int idepth_max,
				    float array2d_idepth_ivis_atotal
				    [NBDEPTHS][NVIS]);
void get_array2d_idepth_iband_atotal_lee2002(float array1d_iband_atotal[NBANDS],
					     float array2d_idepth_ivis_aphy[NBDEPTHS][NVIS],
					     char sat,
					     int idepth_max,
					     float *ptr_array1d_iband_band,
					     float array2d_idepth_iband_atotal[NBDEPTHS][NBANDS]);
void get_array2d_idepth_iband_val(float array2d_idepth_ivis_val[NBDEPTHS][NVIS],
                                  char sat,
                                  int idepth_max,
                                  float array2d_idepth_iband_val[NBDEPTHS][NBANDS]);
void get_array2d_idepth_itime_pp(float array1d_idepth_chl[NBDEPTHS],
                                 float array2d_idepth_itime_pur
                                 [NBDEPTHS][NTIMES],
                                 float array1d_idepth_ek[NBDEPTHS],
                                 float array1d_idepth_depthphy[NBDEPTHS],
                                 int array1d_itime_idepth_max[NTIMES],
                                 float array2d_idepth_itime_pp
                                 [NBDEPTHS - 1][NTIMES - 1]);
void get_array2d_idepth_ivis_atotal(float array1d_ivis_atotal_lee2002[NVIS],
				    float array2d_idepth_ivis_aphy
				    [NBDEPTHS][NVIS],
				    int idepth_max,
				    float array2d_idepth_ivis_atotal
				    [NBDEPTHS][NVIS]);
void get_array2d_idepth_ivis_bbtotal(PixelWater p,
				     float array1d_idepth_chl[NBDEPTHS],
				     int idepth_max,
				     float array2d_idepth_ivis_bbtotal
				     [NBDEPTHS][NVIS]);
void get_array2d_idepth_ivis_bbtotalin(float array1d_ivis_bbtotal_lee2002[NVIS],
				      float array2d_idepth_ivis_bbtotal_wang2005
				       [NBDEPTHS][NVIS],
				       int idepth_max,
				       float array2d_idepth_ivis_bbtotal
				       [NBDEPTHS][NVIS]);
void get_array2d_idepth_ivis_bbtotal_wang2005(float array1d_idepth_bbp555
					      [NBDEPTHS],
					      float array1d_idepth_gamma
					      [NBDEPTHS],
					      float array1d_ivis_bbw[NVIS],
					      int idepth_max,
					      float array2d_idepth_ivis_bbtotal
					      [NBDEPTHS][NVIS]);
void get_array2d_idepth_ivis_E0(float array2d_idepth_ivis_Ed[NBDEPTHS][NVIS],
				float array2d_idepth_ivis_Kd[NBDEPTHS][NVIS],
                                float array2d_idepth_ivis_atotal
                                [NBDEPTHS][NVIS],
                                float array2d_idepth_ivis_bbtotal
                                [NBDEPTHS][NVIS],
                                int idepth_max,
                                float array2d_idepth_ivis_E0[NBDEPTHS][NVIS]);
void get_array2d_idepth_ivis_Ed(float array2d_idepth_ivis_Kd[NBDEPTHS][NVIS],
                                float array1d_idepth_Z[NBDEPTHS],
                                float array1d_iwl_Ed0minus[NBWL],
                                int idepth_max,
                                float array2d_idepth_ivis_Ed[NBDEPTHS][NVIS]);
void get_array2d_idepth_ivis_Kd(float array2d_idepth_ivis_atotal
                                [NBDEPTHS][NVIS],
                                float array2d_idepth_ivis_bbtotal
                                [NBDEPTHS][NVIS],
                                float thetas,
                                int idepth_max,
                                float array2d_idepth_ivis_Kd[NBDEPTHS][NVIS]);
float getBelangerTmp(float chl, float pur, float ek);
int get_idepth_max(float depth,
                   float max_depth,
                   float depth_step);
int get_ivis(int iband, char sat);
float get_one_cell_from_double_integral(float lower_bound_first_integral,
                                        float upper_bound_first_integral,
                                        float lower_bound_second_integral_left,
                                        float upper_bound_second_integral_left,
                                        float lower_bound_second_integral_right,
                                        float upper_bound_second_integral_right,
                                        float topleft,
                                        float bottomleft,
                                        float topright,
                                        float bottomright);
float get_PAR(float array1d_ivis_Ed[NVIS]);
float get_pp(float array1d_idepth_pp[NBDEPTHS - 1]);
void fill_array2d_idepth_itime_PAR(float array1d_idepth_PAR[NBDEPTHS],
                                   int itime,
                                   float array2d_idepth_itime_PAR
                                   [NBDEPTHS][NTIMES]);
float interp_line(float x1, float x2, float x, float y1, float y2);
void print_aphy443(float aphy443[NBDEPTHS]);
void print_array1d_iband_3col(char* name_col1,
                              char* name_col2,
                              char* name_col3,
                              float array1d_iband_valcol1[NBANDS],
                              float array1d_iband_valcol2[NBANDS],
                              float array1d_iband_valcol3[NBANDS]);
void print_array1d_itime_ivalue(int array1d_itime_ivalue[NTIMES],
                                char* value_name);
void print_array1d_ivis_value(float array1d_ivis_value[NVIS],
			      char* value_name);
void print_array1d_idepth_chl(float array1d_idepth_chl[NBDEPTHS]);
void print_array1d_idepth_pp(float array1d_idepth_pp[NBDEPTHS - 1]);
void print_array2d_idepth_iband_value(float array2d_idepth_iband_value[NBDEPTHS][NBANDS],
                                      char* value_name);
void print_array2d_idepth_itime_value(float array2d_idepth_itime_value
                                      [NBDEPTHS][NTIMES],
                                      char* value_name);
void print_array2d_idepthminus1_itime_value(float array2d_idepth_itime_value[NBDEPTHS - 1][NTIMES - 1],
                                      char* value_name);
void print_array2d_idepth_ivis_value(float array2d_idepth_ivis_value
                                     [NBDEPTHS][NVIS],
                                     char* value_name);
void print_chl_bbp555_bbtotal_gamma(float array1d_idepth_chl[NBDEPTHS],
                                    float array1d_idepth_bbp555[NBDEPTHS],
                                    float array1d_idepth_bbtotal555[NBDEPTHS],
                                    float array1d_idepth_gamma[NBDEPTHS]);
void print_idepth_max(int idepth_max);
void print_iop_6bands(float array1d_iband_Rrs[NBANDS],
                      float array1d_iband_a[NBANDS],
                      float array1d_iband_bb[NBANDS]);
void print_meanpur_ek(float meanPUR[NBDEPTHS], float Ek[NBDEPTHS]);
void print_pp(float pp);
void print_pp_at_depth_and_time(int idepth,
                                int itime,
                                float depthtopleft,
                                float depthtopright,
                                float depthbottomleft,
                                float depthbottomright,
                                float hourleft,
                                float hourright,
                                float chlbottom,
                                float chltop,
                                float purtopleft,
                                float purtopright,
                                float purbottomleft,
                                float purbottomright,
                                float ektop,
                                float ekbottom,
                                float topleft,
                                float topright,
                                float bottomleft,
                                float bottomright,
                                float pp_one_cell);
void print_pur(int k, float PUR[NBDEPTHS][NTIMES]);
void print_thetas(int julien, float hh, float xlat, float xlon, float thetas);
void print_Z(float Z[NBDEPTHS]);
void read_Ed_pixel(float array2d_k_ivis_Ed0moins[NTIMES][NVIS],
                   int k,
                   float Ed_pixel[NBWL]);
void test_get_array1d_idepth_pp(float array1d_idepth_pp[NBDEPTHS - 1],
				int chl);
void test_get_array1d_idepth_pp_from_atm(float array1d_idepth_pp[NBDEPTHS - 1],
					 int chl);

/* ============== GLOBAL VARIABLES ============== */
/*
 * Array of dimension NBANDS = 6.
 * The first dimension are the wavelengths of the bands of the satellite.
 * The values are the band of MODIS-AQUA.
 * The units are nm.
 */
float ARRAY1D_IBAND_BANDMODISA[NBANDS] = {412., 443., 488., 531., 555., 667.};
/*
 * Array of dimension NBANDS = 6.
 * The first dimension are the wavelengths of the bands of the satellite.
 * The values are the band of SeaWiFS.
 * The units are nm.
 */
float ARRAY1D_IBAND_BANDSEAWIFS[NBANDS] = {412., 443., 490., 510., 555., 670.};
/*
 * Array of dimension 9.
 * The first dimension is the hours UTC from 0 to 24 by step of 3 h.
 * The values are the hours UTC.
 * The units are hours UTC.
 */
float ARRAY1D_ITIME_HOUR[NTIMES]={0., 3., 6., 9., 12., 15., 18., 21., 0.};
/*
 * Array of dimension 61.
 * The first dimension is the index of the wavelength.
 * The values are the wavelengths from 400 to 700 by step 5.
 * The units are nm.
 */
float LW[NVIS];

/* ====================== FUNCTIONS ====================== */

/*
 * IN
 * aphy443:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension are the geometrical depths. Units: m.
 *  The values are the phytoplankton absorption coefficient at 443 nm.
 *  The units are m^-1.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * vis_aphy:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the phytoplankton absorption coefficient (a_phy)
 *  The units are m^-1.
 * Compute the phytoplankton absorption coefficient (a_phy) from the
 * chlorophyll-a concentration (Matsuoka et al. 2007).
 */
void calc_aphy(float aphy443[NBDEPTHS],
               int idepth_max,
               float vis_aphy[NBDEPTHS][NVIS]){
  float A[NVIS] = {0.0209, 0.0232, 0.0252, 0.0266, 0.0275, 0.0281, 0.0291, 0.0304, 0.0306, 0.0291, 0.0271, 0.0257, 0.0253, 0.0249, 0.0242, 0.0228, 0.0241, 0.0202, 0.0189, 0.0172, 0.0156, 0.0141, 0.0126, 0.0113, 0.0103, 0.0093, 0.0085, 0.0077, 0.0070, 0.0064, 0.0057, 0.0049, 0.0043, 0.0039, 0.0036, 0.0036, 0.0035, 0.0036, 0.0037, 0.0036, 0.0034, 0.0033, 0.0035, 0.0038, 0.0041, 0.0042, 0.0045, 0.0048, 0.0050, 0.0052, 0.0054, 0.0058, 0.0072, 0.0100, 0.0127, 0.0140, 0.0128, 0.0093, 0.0054, 0.0029, 0.0018};
  float B[NVIS] = {0.881, 0.898, 0.902, 0.891, 0.881, 0.878, 0.866, 0.863, 0.860, 0.857, 0.856, 0.855, 0.858, 0.854, 0.854, 0.847, 0.843, 0.845, 0.853, 0.858, 0.866, 0.874, 0.877, 0.877, 0.888, 0.894, 0.909, 0.924, 0.950, 0.965, 0.975, 0.970, 0.972, 0.947, 0.932, 0.946, 0.894, 0.904, 0.903, 0.890, 0.880, 0.867, 0.891, 0.895, 0.912, 0.907, 0.909, 0.898, 0.898, 0.870, 0.883, 0.903, 0.920, 0.930, 0.922, 0.921, 0.932, 0.951, 0.956, 0.969, 0.993};
  int i;
  int idepth;
  float one_aphy443;
  for(idepth = 0; idepth < idepth_max; idepth++){
    one_aphy443 = aphy443[idepth];
    for(i = 0; i < NVIS; i++){
      vis_aphy[idepth][i]
      = A[i]
      * (float) pow((double) one_aphy443 / A_PHI_443, B[i] / E_PHI_443);
    }
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_chl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * aphy443:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The values are the phytoplankton absorption coefficient (a_phy) at
 *  443 nm.
 *  The units are m^-1.
 */
void calc_aphy443(float array1d_idepth_chl[NBDEPTHS],
                  int idepth_max,
                  float aphy443[NBDEPTHS]){
  int idepth;
  for(idepth = 0; idepth < idepth_max; idepth++){
    aphy443[idepth]
    = A_PHI_443 * (float)pow((double)array1d_idepth_chl[idepth], E_PHI_443);
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_ivis_E0
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 6.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the scalar irradiances.
 *  The units are umol photons.m^-2.s^-1.nm^-1.
 * vis_aphy:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the phytoplankton absorption coefficient (a_phy)
 *  The units are m^-1.
 * aphy443:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The values are the phytoplankton absorption coefficient at 443 nm.
 *  The units are m^-1.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array1d_iprof_PUR:
 *  The values are the photosynthetically usable radiation (PUR) for a pixel
 *  on a given day.
 *  The units are uEinstein*m^-2*s^-1.
 * Compute the PUR (equation 6).
 * Integration with the method of the trapezes.
 */
void calc_array1d_iprof_PUR(float array2d_idepth_ivis_E0[NBDEPTHS][NVIS],
                            float vis_aphy[NBDEPTHS][NVIS],
                            float aphy443[NBDEPTHS],
                            int idepth_max,
                            float array1d_iprof_PUR[NBDEPTHS]){
  int iprof;
  int ivis;
  float a1;
  float a2;
  for(iprof = 0; iprof < idepth_max; iprof++){
    array1d_iprof_PUR[iprof] = 0.;
    for(ivis = 0; ivis < (NVIS - 1); ivis++){
      a1 =
      vis_aphy[iprof][ivis] / aphy443[iprof] * array2d_idepth_ivis_E0[iprof][ivis];
      a2 =
      vis_aphy[iprof][ivis + 1] / aphy443[iprof] * array2d_idepth_ivis_E0[iprof][ivis + 1];
      array1d_iprof_PUR[iprof] +=
      ( (LW[ivis + 1] - LW[ivis]) * (a1 + a2) / 2.);
    }
  }
}
/* ------------------------------------------------------------------ */

/* --------------------------------------------------------------
 Calcul de Ek (equation 8 & 9)
 */
void calc_Ek(float Ek[NBDEPTHS], float meanPUR[NBDEPTHS], int idepth_max){
  int i;
  double Ek_max=80., B;
  
  B = exp( 1.089 - 2.12*log10(Ek_max));
  for(i=0; i<idepth_max; i++){
    Ek[i] = (float)( Ek_max / (1+2*exp(-B * meanPUR[i])) );
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * a:
 *  Array of dimensions NVIS = 101.
 *  The first dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the total absorption coefficients (a or a_t).
 *  The units are m^-1.
 * bb:
 *  Array of dimensions  NVIS = 101.
 *  The first dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the total backscattering coefficients (bb or bb_t).
 *  The units are m^-1.
 * thetas:
 *  Solar zenith angle.
 *  Units: Degrees.
 * OUT
 * Kd:
 *  Array of dimensions NVIS = 61.
 *  The first dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the diffuse attenuation coefficients.
 *  The units are m^-1.
 */
void calc_kdsimon(float a[NVIS],
                  float bb[NVIS],
                  float Kd[NVIS],
                  float thetas)
{
	short i, j,ithetas;
	//float m[4][NBTHETAS] = { {1.044, 1.108, 1.32}, {4.173, 4.245, 4.120}, {0.530, 0.526, 0.504}, {11.157, 10.942, 10.304}};
	// m3(10) de Simon
	float m[4][NBTHETAS] = { {1.044, 1.108, 1.32}, {4.173, 4.245, 4.120}, {0.530, 0.526, 0.504}, {11.157, 10.942, 10.304}};
	float thetas_lut[3] = {10.,30.,60.};
	float f,minter[4];
	
	if (thetas <= thetas_lut[0])
	{
    for(i=0; i<NVIS; i++)
    {
      Kd[i] = m[0][0]*a[i] + m[1][0]*(1.-m[2][0]*(float)exp( (double)-m[3][0]*a[i]) )*bb[i];
    }
	}
  
	if (thetas >= thetas_lut[2])
	{
		for(i=0; i<NVIS; i++)
		{
			Kd[i] = m[0][2]*a[i] + m[1][2]*(1.-m[2][2]*(float)exp( (double)-m[3][2]*a[i]) )*bb[i];
		}
	}
  
	if(thetas > 10. && thetas<60)
	{
		/* Interpolation des coefficients */
		for (j=0; j<=1; j++)
		{
			if(thetas >= thetas_lut[j] && thetas < thetas_lut[j+1])
			{ithetas=j;}
		}
		f = (thetas - thetas_lut[ithetas]) / (thetas_lut[ithetas+1] - thetas_lut[ithetas]);
    
		for(j=0; j<=3; j++)
		{
			minter[j] = (1.-f)*m[j][ithetas] + f * m[j][ithetas+1];
		}
    
		for (i=0; i<NVIS; i++)
		{
			Kd[i] = minter[0]*a[i] + minter[1]*(1.-minter[2]*(float)exp( (double)-minter[3]*a[i]) )*bb[i];
		}
	}
}
/* ------------------------------------------------------------------ */

/* --------------------------------------------------------------
 Calcul du PUR moyen (equation 10)
 integration par la methode des trapezes
 */
void calc_meanPUR(float PUR[NBDEPTHS][NTIMES],
                  float meanPUR[NBDEPTHS],
                  float photoperiode,
                  int idepth_max){
  int i, j;
  
  for(i=0; i<idepth_max; i++){
    meanPUR[i] = 0.;
    for(j=0; j<NTIMES-1; j++){
      meanPUR[i]
      += ( INTERVALLE_TEMPS_ISCCP * 3600. * (PUR[i][j+1] + PUR[i][j]) / 2. );
    }
    meanPUR[i] /= photoperiode;
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_chl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometrical depths.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 * array2d_idepth_itime_pur:
 *  Array of dimensions NBDEPTHS * 9.
 *  The first dimension is the index of the geometrical depths.
 *  The second dimension is the index of the hours.
 *  The values are the photosynthetically usable radiation (PUR) for a pixel
 *  on a given day.
 *  The units are uEinstein*m^-2*s^-1.
 * array1d_idepth_ek:
 *  Array of dimension NBDEPTHS.
 *  The first dimension is the index of the geometrical depths.
 *  The values are the saturation irradiances.
 *  The units are uEinstein*m^-2*s^-1.
 * array1d_itime_idepth_max:
 *  Array of dimensions 101.
 *  The first dimension is the index of the geometrical depths.
 *  The values are the geometrical depths.
 *  The units are m.
 * array1d_itime_idepthphy_max:
 *  Array of dimension NTIMES = 9.
 *  The first dimension is the is the hours from 0 to 24 by step of 3 h.
 *  The values are the indices of the depth unto which the primary
 *  productivity will be computed (exclusive).
 * OUT
 * array1d_idepth_pp:
 *  Array of dimension NBDEPTHS - 1 = 100.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the primary productivities.
 *  Units: mgC.m^-2.d^-1.
 * Return new primary productivity estimate from surface to 100 m.
 * Use equation 5.
 * The units are mgC.m^-2.d^-1.
 */
float calc_PP_down_to_depth(float array1d_idepth_chl[NBDEPTHS],
                            float array2d_idepth_itime_pur[NBDEPTHS][NTIMES],
                            float array1d_idepth_ek[NBDEPTHS],
                            float array1d_idepth_depthphy[NBDEPTHS],
                            int array1d_itime_idepth_max[NTIMES],
                            float array1d_idepth_pp[NBDEPTHS - 1]){
  /////////// Declaration of the variables. ///////////
  /*
   * Array of dimensions (NBDEPTHS - 1) * (NTIMES - 1) = 100 * 8.
   * The first dimension are the geometrical depths.
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   * The second dimension is the hours from 0 to 21 by step of 3 h.
   * The values are the primary productivity.
   * The units are mgC.m^-2.d^-1.
   */
  float array2d_idepth_itime_pp[NBDEPTHS - 1][NTIMES - 1];
  /*
   * The index of the geometrical depths.
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth;
  /*
   * Index of the time UTC from 0 to 24 by step 3.
   * Units: h.
   */
  int itime;
  /*
   * Primary productivity.
   * Units: mgC.m^-2.d^-1.
   */
  float pp;
  /////////// Initialize variables with foo values. ///////////
  pp = -999.;
  for(idepth = 0; idepth <  NBDEPTHS - 1; idepth++){
    for(itime = 0; itime < NTIMES - 1; itime++){
      array2d_idepth_itime_pp[idepth][itime] = -999.;
    }
  }
  /////////// Compute primary productivity for each depth and each time. /////
  get_array2d_idepth_itime_pp(array1d_idepth_chl,
                              array2d_idepth_itime_pur,
                              array1d_idepth_ek,
                              array1d_idepth_depthphy,
                              array1d_itime_idepth_max,
                              array2d_idepth_itime_pp);
  /////////// Compute primary productivity for each depth. ///////////
  get_array1d_idepth_ppin(array2d_idepth_itime_pp,
                          array1d_idepth_pp);
  
  /////////// Compute primary productivity. ///////////
  pp = get_pp(array1d_idepth_pp);
  
  /////////// Print. ///////////
  if(DEBUG >= DEBUG_1){
    print_array2d_idepthminus1_itime_value(array2d_idepth_itime_pp,
                                    "Primary productivity (mgC.m^-2.d^-1)");
  }
  
  /////////// Return. ///////////
  return pp;
}
/* ------------------------------------------------------------------ */

/*
 * OUT
 * array2d_iprof_h_PUR:
 *  Array of dimensions 12 * 9.
 *  The first dimension is the optical depths:
 *  {1.,.9, .8, .7, .6, .5, .4, .3, .2, .1, .01, .001}.
 *  The second dimension is the hours from 0 to 24 by step of 3 h.
 * IN
 * array2d_idepth_ivis_E0
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 6.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the scalar irradiances.
 *  The units are umol photons.m^-2.s^-1.nm^-1.
 * h:
 *  The index of the hour for the hours from 0 to 24 by step of 3 h.
 * vis_aphy:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the phytoplankton absorption coefficient (a_phy)
 *  The units are m^-1.
 * aphy443:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The values are the phytoplankton absorption coefficient at 443 nm.
 *  The units are m^-1.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * Compute the PUR for a specific time and write it in a 2d array of the PUR
 * for each depth and each time.
 */
void calc_PUR(float array2d_iprof_h_PUR[NBDEPTHS][NTIMES],
              float array2d_idepth_ivis_E0[NBDEPTHS][NVIS],
              int h,
              float vis_aphy[NBDEPTHS][NVIS],
              float aphy443[NBDEPTHS],
              int idepth_max){
  /*
   *  The values are the photosynthetically usable radiation (PUR) for a pixel
   *  on a given day.
   *  The units are uEinstein*m^-2*s^-1.
   */
  float array1d_iprof_PUR[NBDEPTHS];
  int iprof;
  calc_array1d_iprof_PUR(array2d_idepth_ivis_E0,
                         vis_aphy,
                         aphy443,
                         idepth_max,
                         array1d_iprof_PUR);
  for(iprof = 0; iprof < idepth_max; iprof++){
    array2d_iprof_h_PUR[iprof][h] = array1d_iprof_PUR[iprof];
  }
}

/*
 * IN
 * nb_depths: Number of geometric depths.
 *	      The geometric depths are from 0 to 100 by step 1. Units: m.
 * depth_step: Difference between two depths.
 *	       Units: m.
 * OUT
 * Z: Array of dimensions 101.
 *    The first dimension is the index of the geometrical depths.
 *    The values are the geometrical depths.
 *    The units are m.
 */
void calc_Z(int nb_depths, float depth_step, float Z[NBDEPTHS]){
  int idepth;
  for(idepth = 0; idepth < nb_depths; idepth++){
    Z[idepth] = idepth * depth_step;
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_iband_atotal:
 *  Array of dimension NBANDS = 6.
 *  The first dimension are the wavelengths of the bands of the satellite.
 *  The values are the total absorption coefficients (a or a_t).
 *  The units are m^-1.
 * array1d_iband_aw:
 *  Array of dimension NBANDS = 6.
 *  The first dimension are the wavelengths of the bands of the satellite.
 *  The values are the water absorption coefficients (a_w).
 *  The units are m^-1.
 * array2d_idepth_iband_aphy:
 *  Array of dimensions NBDEPTHS * NBANDS = 101 * 6.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths of the bands of the satellite.
 *  Units: nm.
 *  The values are the phytoplankton absorption coefficient (a_phy)
 *  The units are m^-1.
 * OUT
 * array1d_iband_aCDOM:
 *  Array of dimension NBANDS = 6.
 *  The first dimension are the wavelengths of the bands of the satellite.
 *  The values are the colored dissolved organic matter (CDOM) absorption
 *  coefficients (a_CDOM). CDOM is also known as yellow substances or
 *  gelbstoff.
 *  The units are m^-1.
 * Return aCDOM.
 */
void get_array1d_iband_aCDOM(float array1d_iband_atotal[NBANDS],
                             float array1d_iband_aw[NBANDS],
                             float array2d_idepth_iband_aphy[NBDEPTHS][NBANDS],
                             float array1d_iband_aCDOM[NBANDS]){
  float aCDOM;
  float aphy;
  float atotal;
  float aw;
  int iband;
  for(iband = 0; iband < NBANDS; iband++){
    atotal = array1d_iband_atotal[iband];
    aw = array1d_iband_aw[iband];
    aphy = array2d_idepth_iband_aphy[0][iband];
    aCDOM = atotal -aw -aphy;
    array1d_iband_aCDOM[iband] = aCDOM;
  }
}
/* ------------------------------------------------------------------ */

/* 
 * IN
 * p:
 *  Pixel with information about the water.
 * OUT
 * array1d_iband_atotal:
 * Array of dimension NBANDS = 6.					        
 * The first dimension are the wavelengths of the bands of the satellite.    
 * The values are the total absorption coefficients (a or a_t).	       
 * The units are m^-1.                                                       
 */
void get_array1d_iband_atotal_lee2002(PixelWater p,
				      float array1d_iband_atotal[NBANDS]){
  /*
   * Array of dimension NBANDS = 6.
   * The first dimension are the wavelengths of the bands of the satellite.
   * The values are the bands of the satellite.
   * The units are nm.
   */
  float array1d_iband_band[NBANDS];
  /*
   * Array of dimension NBANDS = 6.
   * The first dimension are the wavelengths of the bands of the satellite.
   * The values are the total backscattering coefficients (bb or b_bt) at
   * the surface (z = 0).
   * The algorithm is Lee 2002.
   * The units are m^-1.
   * Note that these values are returned by functions qaaSW and qaaMA but are
   * not used.
   */
  float array1d_iband_bb[NBANDS];
  /*
   * Array of dimension NBANDS = 6.
   * The first dimension are the wavelengths of the bands of the satellite.
   * The values are the remote sensing reflectances.
   * The units are sr^-1.
   */
  float array1d_iband_Rrs[NBANDS];
  int iband;
  /*
   * Array of dimension NBANDS = 6.					     
   * The first dimension are the wavelengths of the bands of the satellite.  
   * The values are the bands of the satellite.				     
   * The units are nm.                                                       
   */
  float *ptr_array1d_iband_band = NULL;
  if(p.rrs_type == SEAWIFS){
    ptr_array1d_iband_band = ARRAY1D_IBAND_BANDSEAWIFS;
    qaaSW(p.ptr_array1d_iband_Rrs,
	  array1d_iband_atotal,
	  array1d_iband_bb);
  }else if(p.rrs_type == MODISA){
    ptr_array1d_iband_band = ARRAY1D_IBAND_BANDMODISA;
    qaaMA(p.ptr_array1d_iband_Rrs,
	  array1d_iband_atotal,
	  array1d_iband_bb);
  }
  /////////// Print. ///////////
  if(DEBUG >= DEBUG_1){
    for(iband = 0; iband < NBANDS; iband++){
      array1d_iband_band[iband] = *(ptr_array1d_iband_band + iband);
      array1d_iband_Rrs[iband] = *(p.ptr_array1d_iband_Rrs + iband);
    }
    print_array1d_iband_3col("Lambda (nm)",
			     "Rrs (sr^-1)",
			     "a from Lee 2002 (m^-1)",
			     array1d_iband_band,
			     array1d_iband_Rrs,
			     array1d_iband_atotal);
  }
}
/* ------------------------------------------------------------------ */

/* 
 * IN
 * p:
 *  Pixel with information about the water.
 * OUT
 * array1d_iband_atotal:
 * Array of dimension NBANDS = 6.					        
 * The first dimension are the wavelengths of the bands of the satellite.    
 * The values are the total backscattering coefficients (bb or b_bt).	       
 * The units are m^-1.                                                       
 */
void get_array1d_iband_bbtotal_lee2002(PixelWater p,
				       float array1d_iband_bbtotal[NBANDS]){
  /*
   * Array of dimension NBANDS = 6.
   * The first dimension are the wavelengths of the bands of the satellite.
   * The values are the bands of the satellite.
   * The units are nm.
   */
  float array1d_iband_band[NBANDS];
  /*
   * Array of dimension NBANDS = 6.
   * The first dimension are the wavelengths of the bands of the satellite.
   * The values are the total absorption coefficients (a or a_t) at
   * the surface (z = 0).
   * The algorithm is Lee 2002.
   * The units are m^-1.
   * Note that these values are returned by functions qaaSW and qaaMA but are
   * not used.
   */
  float array1d_iband_a[NBANDS];
  /*
   * Array of dimension NBANDS = 6.
   * The first dimension are the wavelengths of the bands of the satellite.
   * The values are the remote sensing reflectances.
   * The units are sr^-1.
   */
  float array1d_iband_Rrs[NBANDS];
  int iband;
  /*
   * Array of dimension NBANDS = 6.					     
   * The first dimension are the wavelengths of the bands of the satellite.  
   * The values are the bands of the satellite.				     
   * The units are nm.                                                       
   */
  float *ptr_array1d_iband_band = NULL;
  if(p.rrs_type == SEAWIFS){
    ptr_array1d_iband_band = ARRAY1D_IBAND_BANDSEAWIFS;
    qaaSW(p.ptr_array1d_iband_Rrs,
	  array1d_iband_a,
	  array1d_iband_bbtotal);
  }else if(p.rrs_type == MODISA){
    ptr_array1d_iband_band = ARRAY1D_IBAND_BANDMODISA;
    qaaMA(p.ptr_array1d_iband_Rrs,
	  array1d_iband_a,
	  array1d_iband_bbtotal);
  }
  /////////// Print. ///////////
  if(DEBUG >= DEBUG_1){
    for(iband = 0; iband < NBANDS; iband++){
      array1d_iband_band[iband] = *(ptr_array1d_iband_band + iband);
      array1d_iband_Rrs[iband] = *(p.ptr_array1d_iband_Rrs + iband);
    }
    print_array1d_iband_3col("Lambda (nm)",
			     "Rrs (sr^-1)",
			     "bb from Lee 2002 (m^-1)",
			     array1d_iband_band,
			     array1d_iband_Rrs,
			     array1d_iband_bbtotal);
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * p:
 *  Pixel with information about the water.
 * OUT
 * array1d_ivis_bbtotal_lee2002:
 *  Array of dimension NVIS = 61.					       
 *  The first dimension are are the wavelengths in the visible spectrum.      
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.		       
 *  The values are the total absorption coefficients (bb or b_bt).	       
 *  The units are m^-1.                                                       
 * Compute the total backscattering coefficients 
 * (bbt(lambda, z = 0, algo = Lee)).
 * Reference:
 * Lee et al. 2002.
 */
void get_array1d_ivis_bbtotal_lee2002(PixelWater p,
				      float array1d_ivis_bbtotal_lee2002[NVIS]){
  /*
   * Array of dimension NBANDS = 6.					       
   * The first dimension are the wavelengths of the bands of the satellite.    
   * The values are the total backscattering coefficients (bb or b_bt).	       
   * The units are m^-1.                                                       
   */
  float array1d_iband_bbtotal[NBANDS];

  get_array1d_iband_bbtotal_lee2002(p,
				    array1d_iband_bbtotal);
  get_array1d_ivis_from_iband(array1d_iband_bbtotal,
			      p.rrs_type,
 			      array1d_ivis_bbtotal_lee2002);
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_ivis_value:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are some values.
 * idepth:
 *  The index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 * OUT
 * array1d_ivis_value:
 *  Array of dimensions NVIS = 61.
 *  The first dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  Units: nm.
 * Get the values at a specific depth.
 */
void get_array1d_ivis_value(float array2d_idepth_ivis_value[NBDEPTHS][NVIS],
			    int idepth,
			    float array1d_ivis_value[NVIS]){
  int ivis;
  float value;
  for(ivis = 0; ivis < NVIS; ivis++){
    value = array2d_idepth_ivis_value[idepth][ivis];
    array1d_ivis_value[ivis] = value;
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_chl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array1d_idepth_bbp555:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the particulate backscattering coefficient at 555 nm.
 *  The units are m^-1.
 * Compute the particulate backscattering coefficient at 555 nm using Wang
 * et al. (2005) equation 12.
 */
void get_array1d_idepth_bbp555(float array1d_idepth_chl[NBDEPTHS],
                               int idepth_max,
                               float array1d_idepth_bbp555[NBDEPTHS]){
  float bbp555;
  float chl;
  /*
   * The index of the geometrical depths.
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth;
  for(idepth = 0; idepth < idepth_max; idepth++){
    chl = array1d_idepth_chl[idepth];
    bbp555 = 0.004 * pow(chl, 0.357);
    array1d_idepth_bbp555[idepth] = bbp555;
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_ivis_bbw:
 *  Array of dimension NVIS = 61.
 * The first dimension are the wavelengths in the visible spectrum.
 *  The values are the pure sea water backscattering coefficients (bb_w).
 *  The units are m^-1.
 * array1d_idepth_bbp555:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the particulate backscattering coefficient at 555 nm.
 *  The units are m^-1.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array1d_idepth_bbtotal555:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The values are the (total) backscattering coefficient at 555 nm.
 *  The units are m^-1.
 */
void get_array1d_idepth_bbtotal555(float array1d_ivis_bbw[NVIS],
                                   float array1d_idepth_bbp555[NBDEPTHS],
                                   int idepth_max,
                                   float array1d_idepth_bbtotal555[NBDEPTHS]){
  float bbw555;
  float bbp555;
  int i555;
  /*
   * The index of the geometrical depths.
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth;
  float bbtotal555;
  i555 = (555 - 400) / 5;
  bbw555 = array1d_ivis_bbw[i555];
  for(idepth = 0; idepth < idepth_max; idepth++){
    bbp555 = array1d_idepth_bbp555[idepth];
    bbtotal555 = bbw555 + bbp555;
    array1d_idepth_bbtotal555[idepth] = bbtotal555;
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_inchl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * chl_option:
 *  The value of the option chl to use the chlorophyll-a concentration.
 *  0 for the chlorophyll-a concentration vertical profile in the water column.
 *  1 for the surface chlorophyll-a concentration.
 * OUT
 * array1d_idepth_outchl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 */
void get_array1d_idepth_chl(float array1d_idepth_inchl[NBDEPTHS],
			    int idepth_max,
			    int chl_option,
			    float array1d_idepth_outchl[NBDEPTHS]){
  float chl;
  int idepth;
  int idepth_tempo;
  for (idepth = 0; idepth < idepth_max; idepth++){
    if(chl_option == CHL_SURFACE){
      idepth_tempo = 0;
    }else if(chl_option == CHL_COLUMN){
      idepth_tempo = idepth;
    }
    chl = array1d_idepth_inchl[idepth_tempo];
    array1d_idepth_outchl[idepth] = chl;
  }
  if(DEBUG >= DEBUG_1){
    print_array1d_idepth_chl(array1d_idepth_outchl);
  }
  
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_bbtotal555:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The values are the (total) backscattering coefficient at 555 nm.
 *  The units are m^-1.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array1d_idepth_gamma:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The values are the parameter describing backscattering spectral
 *  dependency (gamma)
 *  Unitless.
 * Compute gamma using Wang et al. 2005 eq. 13.
 */
void get_array1d_idepth_gamma(float array1d_idepth_bbtotal555[NBDEPTHS],
                              int idepth_max,
                              float array1d_idepth_gamma[NBDEPTHS]){
  float bbtotal555;
  int idepth;
  float gamma;
  for(idepth = 0; idepth < idepth_max; idepth++){
    bbtotal555 = array1d_idepth_bbtotal555[idepth];
    gamma = -2.348 * log10(bbtotal555) -4.353;
    array1d_idepth_gamma[idepth] = gamma;
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_ivis_Ed:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the downward irradiances.
 *  The units are umol photons.m^-2.s^-1.nm^-1.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array1d_idepth_PAR:
 *  Array of dimensions NBDEPTHS.
 *  The first dimension is the index of the physical depths.
 *  The values are the photosynthetically active radiation (PAR) integrated
 *  over the wavelenghts.
 *  The units are umol photons.m^-2.s^-1.
 * Compute PAR(z).
 */
void get_array1d_idepth_PAR(float array2d_idepth_ivis_Ed[NBDEPTHS][NVIS],
                            int idepth_max,
                            float array1d_idepth_PAR[NBDEPTHS]){
  /////////// Declaration of the variables. ///////////
  /*
   * Array of dimensions NVIS = 61.
   * The first dimension are the  wavelengths from 400 nm to 700 nm by step
   * of 5. Units: nm.
   * The values are the downward irradiances.
   * The units are umol photons.m^-2.s^-1.nm^-1.
   */
  float array1d_ivis_Ed[NVIS];
  int idepth;
  int ivis;
  float PAR;
  /////////// Initialize variables with foo values. ///////////
  for(ivis = 0; ivis < NVIS; ivis++){
    array1d_ivis_Ed[ivis] = -999.;
  }
  /////////// Compute. ///////////
  for(idepth = 0; idepth < idepth_max; idepth++){
    get_array1d_ivis_Ed(array2d_idepth_ivis_Ed,
                        idepth,
                        array1d_ivis_Ed);
    PAR = get_PAR(array1d_ivis_Ed);
    array1d_idepth_PAR[idepth] = PAR;
  }
}
/* ------------------------------------------------------------------ */

void get_array1d_idepth_PAR_local_noon(int idepth_max,
                                       float array2d_idepth_ivis_Ed
                                       [NBDEPTHS][NVIS],
                                       float array1d_idepth_PAR_local_noon
                                       [NBDEPTHS]){
  int idepth;
  int ivis;
  float ed;
  float PAR_local_noon;
  for(idepth = 0; idepth < idepth_max; idepth++){
    PAR_local_noon = 0.;
    for(ivis = 0; ivis < NVIS; ivis++){
      ed = array2d_idepth_ivis_Ed[idepth][ivis];
      PAR_local_noon += (ed * 5.);
    }
    array1d_idepth_PAR_local_noon[idepth] = PAR_local_noon;
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_itime_ivis_Ed0minus:
 *  Array of dimensions 9 * 61.							
 *  The first dimension is the hours from 0 to 24 by step of 3 h.		
 *  The second dimension is the wavelenght from 400 nm to 700 nm by step of 5	
 *  nm.										
 *  The values are the downward irradiances just below the surface water	
 *  (Ed0minus) for one pixel.							
 *  The units are umol photons*m^-2*s^-1*nm^-1.                                 
 lat:
 *  Latitude.
 *  The units are degrees North.
 * lon:
 *  Longitude.
 *  From -180 to 180.
 *  The units are degrees East.
 * year
 * month
 * day:
 *  Day of month.
 * doy:
 *  Day of year.
 * depth:
 *  Bathymetry.
 *  The units are m.
 * rrs_type:
 *  S for SeaWiFS and A for MODIS-AQUA.
 * array1d_iband_Rrs:
 *  Array of dimension NBANDS = 6.
 *  The first dimension are the wavelengths of the bands of the satellite.
 *  The values are the remote-sensing reflectances.
 *  The units are sr^-1.
 * array1d_idepth_chl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 * chl:
 *  The value of the option chl to use the chlorophyll-a concentration.
 *  0 for the chlorophyll-a concentration vertical profile in the water column.
 *  1 for the surface chlorophyll-a concentration.
 * OUT
 * array1d_idepth_pp:
 *  Array of dimension NBDEPTHS - 1 = 100.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the primary productivities.
 *  Units: mgC.m^-2.d^-1.
 */
void get_array1d_idepth_pp(float array2d_itime_ivis_Ed0minus[NTIMES][NVIS],
                          float lat,
                          float lon,
                          int year,
                          int month,
                          int day,
                          int doy,
                          float depth,
                          char rrs_type,
                          float array1d_iband_Rrs[NBANDS],
                          float array1d_idepth_chl[NBDEPTHS],
                          float array1d_idepth_pp[NBDEPTHS - 1]){
  /*
   * Pixel with information about the water.
   */
  PixelWater p;
  p.lat                    = lat;
  p.lon                    = lon;
  p.year                   = year;
  p.month                  = month;
  p.day                    = day;
  p.doy                    = doy;
  p.depth                  = depth;
  p.rrs_type               = rrs_type;
  p.ptr_array1d_iband_Rrs  = array1d_iband_Rrs;
  p.ptr_array1d_idepth_chl = array1d_idepth_chl;
  p.ptr_array1d_idepth_pp  = array1d_idepth_pp;
  get_array1d_idepth_pp_from_PixelWater_and_light(array2d_itime_ivis_Ed0minus,
                                                  p);
}
/* ------------------------------------------------------------------ */

/*
 * IN
 lat:
 *  Latitude.
 *  The units are degrees North.
 * lon:
 *  Longitude.
 *  From -180 to 180.
 *  The units are degrees East.
 * year
 * month
 * day:
 *  Day of month.
 * doy:
 *  Day of year.
 * depth:
 *  Bathymetry.
 *  The units are m.
 * rrs_type:
 *  S for SeaWiFS and A for MODIS-AQUA.
 * array1d_iband_Rrs:
 *  Array of dimension NBANDS = 6.
 *  The first dimension are the wavelengths of the bands of the satellite.
 *  The values are the remote-sensing reflectances.
 *  The units are sr^-1.
 * array1d_idepth_chl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 * array1d_itime_cf:
 *  Array of dimensions NTIMES.					    	   
 *  The first dimension is the hours from 0 to 24 by step of 3 h.	    
 *  The values are the cloud fraction from 0 to 1.			    
 *  array1d_idepth_pp is filled with -999 if one or more cloud fraction
 *  value is < 0.
 * array1d_itime_o3:
 *  Array of dimensions NTIMES.				     	    
 *  The first dimension is the hours from 0 to 24 by step of 3 h.   
 *  The values are the total ozone column at 00h UTC.		     
 *  Units: Dobson units.
 *  array1d_idepth_pp is filled with -999 if one or more ozone value is < 0.
 * array1d_itime_taucld:
 *  Array of dimensions NTIMES.					 	
 *  The first dimension is the hours from 0 to 24 by step of 3 h.	 
 *  The values are the cloud optical thickness at 00h UTC.   		 
 *  The values are unitless.
 *  array1d_idepth_pp is filled with -999 if one or more cloud optical
 *  thickness value is < 0.
 * array4d_itaucld_io3_ithetas_iwl_ed0minus:
 *  Array of 4 dimensions 					      
 *  ntaucl=8 * nozone=8 * nthetas=19 * nwl=83.				      
 *  The first dimension is the mean cloud optical thickness.		      
 *  The second dimension is the total ozone column.			      
 *  The third dimension is the solar zenith angle.			      
 *  The fourth dimension is the wavelengths from 290 to 700 by step 5 nm.    
 *  The values are the downward irradiance just below the water surface      
 *  from the lookup table.						      
 *  The units are umol photons*m^-2*s^-1*nm^-1.                              
 * chl:
 *  The value of the option chl to use the chlorophyll-a concentration.
 *  0 for the chlorophyll-a concentration vertical profile in the water column.
 *  1 for the surface chlorophyll-a concentration.                             
 * OUT
 * array1d_idepth_pp:
 *  Array of dimension NBDEPTHS - 1 = 100.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the primary productivities.
 *  Units: mgC.m^-2.d^-1.
 */
void get_array1d_idepth_pp_from_atm(float lat,
                                    float lon,
                                    int year,
                                    int month,
                                    int day,
                                    int doy,
                                    float depth,
                                    char rrs_type,
                                    float array1d_iband_Rrs[NBANDS],
                                    float array1d_idepth_chl[NBDEPTHS],
                                    float array1d_itime_cf[NTIMES],
                                    float array1d_itime_o3[NTIMES],
                                    float array1d_itime_taucld[NTIMES],
                                    float downward_irradiance_table_as_input[NBWL][NTHETAS][NO3][NTAUCLD][NALB],
                                    float array1d_idepth_pp[NBDEPTHS - 1]){
  float array2d_itime_ivis_ed0minus[NTIMES][NVIS];
  int itime;
  int ok = 1;
  float val;
  
  for(itime = 0; itime < NBDEPTHS - 1; itime++){
    array1d_idepth_pp[itime] = -999.;
  }
  
  for(itime = 0; itime < NTIMES; itime++){
    val = array1d_itime_cf[itime];
    if(val < 0){
      ok = 0;
    }
    val = array1d_itime_o3[itime];
    if(val < 0){
      ok = 0;
    }
    val = array1d_itime_taucld[itime];
    if(val < 0){
      ok = 0;
    }
  }
  
  if(ok){
    get_array2d_itime_ivis_ed0minus(lat,
                                    lon,
                                    doy,
                                    array1d_itime_cf,
                                    array1d_itime_o3,
                                    array1d_itime_taucld,
                                    downward_irradiance_table_as_input,
                                    array2d_itime_ivis_ed0minus);
    
    get_array1d_idepth_pp(array2d_itime_ivis_ed0minus,
                          lat,
                          lon,
                          year,
                          month,
                          day,
                          doy,
                          depth,
                          rrs_type,
                          array1d_iband_Rrs,
                          array1d_idepth_chl,
                          array1d_idepth_pp);
  }
}
  
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_itime_ivis_Ed0minus:
 *  Array of dimensions 9 * 61.
 *  The first dimension is the hours from 0 to 24 by step of 3 h.
 *  The second dimension is the wavelenght from 400 nm to 700 nm by step of 5
 *  nm.
 *  The values are the downward irradiances just below the surface water
 *  (Ed0minus) for one pixel.
 *  The units are umol photons*m^-2*s^-1*nm^-1.
 * chl:
 *  The value of the option chl to use the chlorophyll-a concentration.
 *  0 for the chlorophyll-a concentration vertical profile in the water column.
 *  1 for the surface chlorophyll-a concentration.
 * INOUT
 * p:
 *  Pixel with information about the water.
 *
 */
void get_array1d_idepth_pp_from_PixelWater_and_light(float array2d_itime_ivis_Ed0minus
                                                     [NTIMES][NVIS],
                                                     PixelWater p){
  
  /////////// Declaration of scalars equal to some members of p. ///////////
  /*
   * Latitude.
   * The units are degrees North.
   */
  float lat;
  
  float lon;
  int year;
  int month;

  int day;
  /* Day of year. */
  int doy;
  /*
   * Bathymetry.
   * The units are m.
   */
  float depth;
  /*
   * S for SeaWiFS and A for MODIS-AQUA.
   */
  char rrs_type;
  
  /////////// Copy scalars members of p ///////////
  lat      = p.lat;
  lon      = p.lon;
  year     = p.year;
  month    = p.month;
  day      = p.day;
  doy      = p.doy;
  depth    = p.depth;
  rrs_type = p.rrs_type;
  
  /////////// Declaration of the variables. ///////////
  float array1d_iband_aphy[NBANDS];
  float array1d_iband_atotal[NBANDS];
  float array1d_iband_bb_lee2002[NBANDS];
  float array1d_iband_bbt[NBANDS];
  float array1d_idepth_aphy443[NBDEPTHS];
  float array1d_idepth_chl[NBDEPTHS];
  float array1d_idepth_depth[NBDEPTHS];
  float array1d_idepth_Ed[NBDEPTHS];
  float array1d_idepth_Ek[NBDEPTHS];
  float array1d_idepth_meanPUR[NBDEPTHS];
  float array1d_idepth_PAR[NBDEPTHS];
  float array1d_idepth_PAR_local_noon[NBDEPTHS];
  int array1d_itime_idepthphy_max[NTIMES];
  float array1d_itime_thetas[NTIMES];
  float array1d_ivis_atotal_lee2002[NVIS];
  float array2d_idepth_itime_PAR[NBDEPTHS][NTIMES];
  float array2d_idepth_itime_PUR[NBDEPTHS][NTIMES];
  float array2d_idepth_ivis_aphy[NBDEPTHS][NVIS];
  float array2d_idepth_ivis_atotal[NBDEPTHS][NVIS];
  float array2d_idepth_ivis_bbtotal[NBDEPTHS][NVIS];
  float array2d_idepth_ivis_E0[NBDEPTHS][NVIS];
  float array2d_idepth_ivis_Ed[NBDEPTHS][NVIS];
  float array2d_idepth_ivis_Kd[NBDEPTHS][NVIS];
  float array1d_iwl_Ed0minus[NBWL];

  void* depth_info;
  int s_size = 100000;
  char depthInfo_s[s_size];
  int get_out;
  int iband;
  int idepth;
  int idepth_max;
  int itime;
  int ivis;
  int itime_local_noon;
  float npp0_001;
  float one_daylength;
  float phi;
  float *ptr_array1d_iband_band = NULL;
  float thetas;
  float time_local_noon;
  int tmpdoy;
  float wavelength;
  
  /////////// Initialize variables with foo values. ///////////
  get_out          =  0;
  itime_local_noon = -1;
  time_local_noon  = -999.;
  npp0_001         = -999.;
  one_daylength    = -999.;
  for(iband = 0; iband < NBANDS; iband++){
    array1d_iband_aphy[iband]         = -999.;
    array1d_iband_atotal[iband]       = -999.;
    array1d_iband_bbt[iband]          = -999.;
    array1d_iband_bb_lee2002[iband]   = -999.;
  }
  for(ivis = 0; ivis < NVIS; ivis++){
    array1d_ivis_atotal_lee2002[ivis] = -999.;
  }
  for(idepth = 0; idepth < NBDEPTHS; idepth++){
    array1d_idepth_aphy443[idepth]        = -999.;
    array1d_idepth_chl[idepth]            = -999.;
    array1d_idepth_Ed[idepth]             = -999.;
    array1d_idepth_PAR[idepth]            = -999.;
    array1d_idepth_PAR_local_noon[idepth] = -999.;
    array1d_idepth_meanPUR[idepth]        = -999.;
    array1d_idepth_Ek[idepth]             = -999.;
    for(ivis = 0; ivis < NVIS; ivis++){
      array2d_idepth_ivis_aphy[idepth][ivis]    = -999.;
      array2d_idepth_ivis_atotal[idepth][ivis]  = -999.;
      array2d_idepth_ivis_bbtotal[idepth][ivis] = -999.;
      array2d_idepth_ivis_Ed[idepth][ivis]      = -999.;
      array2d_idepth_ivis_E0[idepth][ivis]      = -999.;
      array2d_idepth_ivis_Kd[idepth][ivis]      = -999.;
    }
    for(itime = 0; itime < NTIMES; itime++){
      array2d_idepth_itime_PUR[idepth][itime] = -999.;
      array2d_idepth_itime_PAR[idepth][itime] = -999.;
    }
  }
  for(idepth = 0; idepth < NBDEPTHS - 1; idepth++){
    p.ptr_array1d_idepth_pp[idepth] = -999.;
  }
  for(itime = 0; itime < NTIMES; itime++){
    array1d_itime_thetas[itime]        = -999.;
    array1d_itime_idepthphy_max[itime] = -999;
  }
  
  /////////// Compute wavelengths. ///////////
  
  wavelength = 400.;
  for(ivis = 0; ivis < NVIS; ivis++){
    LW[ivis] = wavelength;
    wavelength += 5.;
  }
  
  /////////// Compute primary productivity. ///////////
  
  // Is the pixel valid?
  if(!get_out){
    
    time_local_noon = get_timeGMT_local_noon(lon);
    itime_local_noon = get_itime(time_local_noon);
    
    // Compute daylength.
    one_daylength = daylength(year, month, day, lat);
    
    // Compute the index of the depth to which parameters are computed
    // (exclusive).
    idepth_max = get_idepth_max(depth,
                                MAX_DEPTH,
                                DEPTH_STEP);

    
    // Find bands.
    if(rrs_type == SEAWIFS){
      ptr_array1d_iband_band = ARRAY1D_IBAND_BANDSEAWIFS;
    }else if(rrs_type == MODISA){
      ptr_array1d_iband_band = ARRAY1D_IBAND_BANDMODISA;
    }
     
    
    // Compute aphy.
    calc_aphy443(p.ptr_array1d_idepth_chl, idepth_max, array1d_idepth_aphy443);
    calc_aphy(array1d_idepth_aphy443, idepth_max, array2d_idepth_ivis_aphy);
    
   
    // Compute a(lamda_61, z).
    get_array1d_ivis_atotal_lee2002(p,
				    array1d_ivis_atotal_lee2002);

    get_array2d_idepth_ivis_atotal(array1d_ivis_atotal_lee2002,
				   array2d_idepth_ivis_aphy,
				   idepth_max,
				   array2d_idepth_ivis_atotal);
    
    // Compute bb(lambda_61, z).
    get_array2d_idepth_ivis_bbtotal(p,
				    p.ptr_array1d_idepth_chl,
				    idepth_max,
				    array2d_idepth_ivis_bbtotal);
    /* Loop on time steps of 3 hours. */
    for(itime = 0; itime < NTIMES; itime++){
      ///// Compute time. /////
      if(itime == ITIME_TOMORROW_MIDNIGHT){
        tmpdoy = doy + 1;
      }else{
        tmpdoy = doy;
      }

      double thetas = sun_zenithal_angle_approximation(tmpdoy, ARRAY1D_ITIME_HOUR[itime], lat, lon);

      array1d_itime_thetas[itime] = thetas;


      // Compute Kd(lambda, z, t).
      get_array2d_idepth_ivis_Kd(array2d_idepth_ivis_atotal,
                                 array2d_idepth_ivis_bbtotal,
                                 thetas,
                                 idepth_max,
                                 array2d_idepth_ivis_Kd);
      
      // Read Ed(lambda, z = 0-, t).
      read_Ed_pixel(array2d_itime_ivis_Ed0minus,
                    itime,
                    array1d_iwl_Ed0minus);
      
      // Compute the geometrical depths: Z(z).
      calc_Z(NBDEPTHS,
             DEPTH_STEP,
             array1d_idepth_depth);
      
      // Compute Ed(lambda, z, t).
      get_array2d_idepth_ivis_Ed(array2d_idepth_ivis_Kd,
                                 array1d_idepth_depth,
                                 array1d_iwl_Ed0minus,
                                 idepth_max,
                                 array2d_idepth_ivis_Ed);
      
      // Compute E0(lambda, z, t).
      get_array2d_idepth_ivis_E0(array2d_idepth_ivis_Ed,
				 array2d_idepth_ivis_Kd,
                                 array2d_idepth_ivis_atotal,
                                 array2d_idepth_ivis_bbtotal,
                                 idepth_max,
                                 array2d_idepth_ivis_E0);
      
      /*equation 6 */
      calc_PUR(array2d_idepth_itime_PUR,
               array2d_idepth_ivis_E0,
               itime,
               array2d_idepth_ivis_aphy,
               array1d_idepth_aphy443,
               idepth_max);
      
      if(itime == itime_local_noon){
        // Compute PAR(z, t = local noon).
        get_array1d_idepth_PAR_local_noon(idepth_max,
                                          array2d_idepth_ivis_Ed,
                                          array1d_idepth_PAR_local_noon);
      }
      
      // Compute PAR(z, t).
      get_array1d_idepth_PAR(array2d_idepth_ivis_Ed,
                             idepth_max,
                             array1d_idepth_PAR);
      fill_array2d_idepth_itime_PAR(array1d_idepth_PAR,
                                    itime,
                                    array2d_idepth_itime_PAR);
      
    } /* End of the loop on time steps of 3 hours. */
    
    // Compute Zmax(t).
    depth_info = Depth_create(array2d_idepth_itime_PAR,
                              idepth_max,
                              DEPTH_STEP);
    Depth_get_array1d_itime_idepthphy_max(depth_info,
                                          array1d_itime_idepthphy_max);
    
    /* equation 10 */
    calc_meanPUR(array2d_idepth_itime_PUR,
                 array1d_idepth_meanPUR,
                 one_daylength,
                 idepth_max);
    /* equation 8 */
    calc_Ek(array1d_idepth_Ek, array1d_idepth_meanPUR, idepth_max);
    

    // Compute PP(z)
    npp0_001 = calc_PP_down_to_depth(p.ptr_array1d_idepth_chl,
                                     array2d_idepth_itime_PUR,
                                     array1d_idepth_Ek,
                                     array1d_idepth_depth,
                                     array1d_itime_idepthphy_max,
                                     p.ptr_array1d_idepth_pp);
    

  } // End of "Is the pixel valid?".
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_itime_pp:
 *  Array of dimensions (NBDEPTHS - 1) * (NTIMES - 1) = 100 * 8.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension is the hours from 0 to 21 by step of 3 h.
 *  The values are the primary productivity.
 *  The units are mgC.m^-2.d^-1.
 * OUT
 * array1d_idepth_pp:
 *  Array of dimension NBDEPTHS - 1 = 100.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the primary productivities.
 *  Units: mgC.m^-2.d^-1.
 */
void get_array1d_idepth_ppin(float array2d_idepth_itime_pp
                             [NBDEPTHS - 1][NTIMES - 1],
                             float array1d_idepth_pp[NBDEPTHS - 1]){
  /*
   * The index of the geometrical depths.
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth;
  /*
   * Index of the time UTC from 0 to 24 by step 3.
   * Units: h.
   */
  int itime;
  /*
   * Primary productivity.
   * Units: mgC.m^-2.d^-1.
   */
  float pp;
  /*
   * Primary productivity.
   * Units: mgC.m^-2.d^-1.
   */
  float pp_tmp;
  // Loop on the depths.
  for(idepth = 0; idepth <= NBDEPTHS - 2; idepth++){
    pp = 0.;
    // Loop on the times.
    for(itime = 0; itime <= NTIMES - 2; itime ++){
      pp_tmp = array2d_idepth_itime_pp[idepth][itime];
      if (pp_tmp > 0){
	pp += pp_tmp;
      }
    } // End of the loop on the times.
    array1d_idepth_pp[idepth] = pp;
  } // End of loop on the depths.
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * p:
 *  Pixel with information about the water.
 * OUT
 * array1d_ivis_atotal_lee2002:
 *  Array of dimension NVIS = 61.					       
 *  The first dimension are are the wavelengths in the visible spectrum.      
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.		       
 *  The values are the total absorption coefficients (a or a_t).	       
 *  The units are m^-1.                                                       
 *
 */
void get_array1d_ivis_atotal_lee2002(PixelWater p,
				     float array1d_ivis_atotal_lee2002[NVIS]){
  /*
   * Array of dimension NBANDS = 6.					       
   * The first dimension are the wavelengths of the bands of the satellite.    
   * The values are the total absorption coefficients (a or a_t).	       
   * The units are m^-1.                                                       
   */
  float array1d_iband_atotal[NBANDS];

  get_array1d_iband_atotal_lee2002(p,
				   array1d_iband_atotal);
  get_array1d_ivis_from_iband(array1d_iband_atotal,
			      p.rrs_type,
			      array1d_ivis_atotal_lee2002);  

  /////////// Print ///////////
  if(DEBUG >= DEBUG_1){
    print_array1d_ivis_value(array1d_ivis_atotal_lee2002,
			     "a from Lee 2002 (m^-1)");
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_ivis_Ed:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the downward irradiances.
 *  The units are umol photons.m^-2.s^-1.nm^-1.
 * idepth:
 *  The index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 * OUT
 * array1d_ivis_Ed:
 *  Array of dimensions NVIS = 61.
 *  The first dimension are the  wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the downward irradiances.
 *  The units are umol photons.m^-2.s^-1.nm^-1.
 */
void get_array1d_ivis_Ed(float array2d_idepth_ivis_Ed[NBDEPTHS][NVIS],
                         int idepth,
                         float array1d_ivis_Ed[NVIS]){
  int ivis;
  float Ed;
  for(ivis = 0; ivis < NVIS; ivis++){
    Ed = array2d_idepth_ivis_Ed[idepth][ivis];
    array1d_ivis_Ed[ivis] = Ed;
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_iband_val:
 *  Array of dimension NBANDS = 6.					       
 *  The first dimension are the wavelengths of the bands of the satellite.    
 *  The values are any values.                                                
 * rrs_type:
 *  S for SeaWiFS and A for MODIS-AQUA.
 * OUT
 * array1d_ivis_val:
 *  Array of dimension NVIS = 61.					      
 *  The first dimension are are the wavelengths in the visible spectrum.      
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.		      
 *  The values are any values.
 */
void get_array1d_ivis_from_iband(float array1d_iband_val[NBANDS],
				 char rrs_type,
				 float array1d_ivis_val[NVIS]){
  /*
   * Array of dimension NBANDS = 6.
   * The first dimension are the wavelengths of the bands of the satellite.
   * The values are the bands of the satellite.
   * The units are nm.
   */
  float array1d_iband_band[NBANDS];
  /*
   * Index of point 1.
   */
  int i1;
  /*
   * Index of point 2.
   */
  int i2;
  /*
   * The index of the wavelengths of the bands of the satellite.
   */
  int iband;
  /*
   * The index of the wavelengths in the visible spectrum.      
   * The wavelengths are from 400 to 700 by step 5. Units: nm.		      
   */
  int ivis;
  /*
   * The wavelength in the visible spectrum.
   * Units: nm.
   */
  float lambda;
  /*
   * The wavelength in the visible spectrum in the first point used for the
   * linear interpolation.
   */
  float lambda1;
  /*
   * The wavelength in the visible spectrum in the second point used for the
   * linear interpolation.
   */
  float lambda2;
  /*
   * Array of dimension NBANDS = 6.					     
   * The first dimension are the wavelengths of the bands of the satellite.  
   * The values are the bands of the satellite.				     
   * The units are nm.                                                       
   */
  float *ptr_array1d_iband_band = NULL;
  /*
   * Interpolated value at lambda.
   */
  float val;
  /*
   * The value in the first point used for the linear interpolation.
   */
  float val1;
  /*
   * The value in the second point used for the linear interpolation.
   */
  float val2;
  
  if(rrs_type == SEAWIFS){
    ptr_array1d_iband_band = ARRAY1D_IBAND_BANDSEAWIFS;
  }else if(rrs_type == MODISA){
    ptr_array1d_iband_band = ARRAY1D_IBAND_BANDMODISA;
  }
  for(iband = 0; iband < NBANDS; iband++){
    array1d_iband_band[iband] = *(ptr_array1d_iband_band + iband);
  }
  for(ivis = 0; ivis < NVIS; ivis++){
    val = -999.;
    lambda = 400. + (ivis * 5.);
    iband = 1;
    while((lambda >= array1d_iband_band[iband]) && (iband < NBANDS - 1)){
      iband++;
    }  
    i1 = iband - 1;						    
    i2 = iband;						    
    lambda1 = array1d_iband_band[i1];			    
    lambda2 = array1d_iband_band[i2];			    
    val1    = array1d_iband_val[i1];			    
    val2    = array1d_iband_val[i2];			    
    val     = interp_line(lambda1, lambda2, lambda, val1, val2);
    array1d_ivis_val[ivis] = val;
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_ivis_atotal_lee2002[NVIS]:
 *  Array of dimension NVIS = 61.					       
 *  The first dimension are are the wavelengths in the visible spectrum.      
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.		       
 *  The values are the total absorption coefficients (a or a_t).	       
 *  The units are m^-1.                                                       
 * array2d_idepth_ivis_aphy:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.			       
 *  The first dimension are the geometrical depths.			       
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.	       
 *  The second dimension are the wavelengths in the visible spectrum.	       
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.		       
 *  The values are the phytoplankton absorption coefficient (a_phy)	       
 *  The units are m^-1.                                                       
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array2d_idepth_ivis_atotal:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.			        
 *  The first dimension are the geometrical depths.			       
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.	       
 *  The second dimension are the wavelengths in the visible spectrum.	       
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.		       
 *  The values are the total absorption coefficients (a or a_t).	       
 *  The units are m^-1.                                                       
 * Equation:
 * a(lambda, z) = a(lambda, z=0) + a_phy(lambda, z) - a_phy(lambda, z=0).
 *  where a(lambda, z=0) is atotal_lee2002 and comes from Lee 2002,
 *        a_phy(lambda, z) is aphy and comes from Matsuoka 2007,
 *        a_phy(lambda, z=0) is aphy_surf and comes from Matsuoka 2007,
 *        a(lambda, z) is atotal and is computed.
 */
void get_array2d_idepth_ivis_atotal(float array1d_ivis_atotal_lee2002[NVIS],
				    float array2d_idepth_ivis_aphy
				    [NBDEPTHS][NVIS],
				    int idepth_max,
				    float array2d_idepth_ivis_atotal
				    [NBDEPTHS][NVIS]){
  float atotal;
  float atotal_lee2002;
  float aphy;
  float aphy_surf;
  int idepth;
  int ivis;
  for(idepth = 0; idepth < idepth_max; idepth++){
    for(ivis = 0; ivis < NVIS; ivis++){
      atotal_lee2002 = array1d_ivis_atotal_lee2002[ivis];
      aphy = array2d_idepth_ivis_aphy[idepth][ivis];
      aphy_surf = array2d_idepth_ivis_aphy[0][ivis];
      atotal = atotal_lee2002 + aphy - aphy_surf;
      array2d_idepth_ivis_atotal[idepth][ivis] = atotal;
    }
  }  
  /////////// Print ///////////
  if(DEBUG >= DEBUG_1){
    print_array2d_idepth_ivis_value(array2d_idepth_ivis_atotal,
				    "a (m^-1)");
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_ivis_bbtotal_lee2002:
 *  Array of dimensions NVIS = 61.					       
 *  The first dimension are the wavelengths in the visible spectrum.	       
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.		       
 *  The values are the total backscattering coefficients (bb) from Lee 2002.  
 *  The units are m^-1.                                                       
 * array2d_idepth_ivis_bbtotal_wang2005:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.			       
 *  The first dimension are the geometrical depths.			       
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.	       
 *  The second dimension are the wavelengths in the visible spectrum.	       
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.		       
 *  The values are the total backscattering coefficients (bb) from Wang 2005. 
 *  The units are m^-1.                                                       
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array2d_idepth_ivis_bbtotal:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the total backscattering coefficients (bb or bb_t).
 *  The units are m^-1.
 * Compute bb_t(lambda, z) with Lee et al. (2002) and Wang et al. (2005).
 */
void get_array2d_idepth_ivis_bbtotalin(float array1d_ivis_bbtotal_lee2002[NVIS],
				      float array2d_idepth_ivis_bbtotal_wang2005
				       [NBDEPTHS][NVIS],
				       int idepth_max,
				       float array2d_idepth_ivis_bbtotal
				       [NBDEPTHS][NVIS]){
  float bbtotal;
  float bbtotal_lee2002;
  float bbtotal_wang2005;
  float bbtotal_wang2005_surf;
  int idepth;
  int ivis;
  for(idepth = 0; idepth < idepth_max; idepth++){
    for(ivis = 0; ivis < NVIS; ivis++){
      bbtotal_lee2002 = array1d_ivis_bbtotal_lee2002[ivis];
      bbtotal_wang2005 = array2d_idepth_ivis_bbtotal_wang2005[idepth][ivis];
      bbtotal_wang2005_surf = array2d_idepth_ivis_bbtotal_wang2005[0][ivis];
      bbtotal = bbtotal_lee2002 + bbtotal_wang2005 - bbtotal_wang2005_surf;
      array2d_idepth_ivis_bbtotal[idepth][ivis] = bbtotal;
    }
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * p:
 *  Pixel with information about the water.
 * array1d_idepth_chl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array2d_idepth_ivis_bbtotal:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the total backscattering coefficients (bb or bb_t).
 *  The units are m^-1.
 * Compute bb_t(lambda, z) with Lee et al. (2002) and Wang et al. (2005).
 */
void get_array2d_idepth_ivis_bbtotal(PixelWater p,
				     float array1d_idepth_chl[NBDEPTHS],
				     int idepth_max,
				     float array2d_idepth_ivis_bbtotal
				     [NBDEPTHS][NVIS]){
  /////////// Declare variables. ///////////
  /*
   * Array of dimension NVIS = 61.					       
   * The first dimension are the wavelengths in the visible spectrum.	       
   * The wavelengths are from 400 to 700 by step 5. Units: nm.		       
   * The values are the pure sea water backscattering coefficients (bb_w).     
   * The units are m^-1.                                                       
   */
  float array1d_ivis_bbw[NVIS] = ARRAY1D_IVIS_BBW;
  /*
   * Array of dimension NBDEPTHS = 101.					       
   * The first dimension is the index of the geometric depths.		       
   * The geometric depths are from 0 to 100 by step 1. Units: m.	       
   * The values are the particulate backscattering coefficient at 555 nm.      
   * The units are m^-1.                                                       
   */
  float array1d_idepth_bbp555[NBDEPTHS];
  /*
   * Array of dimension NBDEPTHS = 101.
   * The first dimension is the index of the geometrical depths.
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   * The values are the (total) backscattering coefficient at 555 nm.
   * The units are m^-1.
   */
  float array1d_idepth_bbtotal555[NBDEPTHS];
  /*
   * Array of dimension NBDEPTHS = 101.				     
   * The first dimension is the index of the geometrical depths.     
   * The geometrical depths are from 0 to 100 by step 1. Units: m.   
   * The values are the parameter describing backscattering spectral 
   * dependency (gamma)						     
   * Unitless.                                                       
   */
  float array1d_idepth_gamma[NBDEPTHS];
  /*
   * Array of dimensions NVIS = 61.					       
   * The first dimension are the wavelengths in the visible spectrum.	       
   * The wavelengths are from 400 to 700 by step 5. Units: nm.		       
   * The values are the total backscattering coefficients (bb) from Lee 2002.  
   * The units are m^-1.                                                       
   */
  float array1d_ivis_bbtotal_lee2002[NVIS];
  /*
   * Array of dimensions NBDEPTHS * NVIS = 101 * 61.			       
   * The first dimension are the geometrical depths.			       
   * The geometrical depths are from 0 to 100 by step 1. Units: m.	       
   * The second dimension are the wavelengths in the visible spectrum.	       
   * The wavelengths are from 400 to 700 by step 5. Units: nm.		       
   * The values are the total backscattering coefficients (bb) from Wang 2005. 
   * The units are m^-1.                                                       
   */
  float array2d_idepth_ivis_bbtotal_wang2005[NBDEPTHS][NVIS];
  /*
   * The index of the band on the satellite.
   */
  int ivis;
  /*
   * The index of the geometrical depths.
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth;
  
  /////////// Initialize variables with foo values. ///////////
  for(idepth = 0; idepth < NBDEPTHS; idepth++){
    array1d_idepth_bbp555[idepth]     = -999.;
    array1d_idepth_bbtotal555[idepth] = -999.;
    array1d_idepth_gamma[idepth]      = -999.;
    for(ivis = 0; ivis < NVIS; ivis++){
      array2d_idepth_ivis_bbtotal_wang2005[idepth][ivis] = -999.;
    }
  }
  for(ivis = 0; ivis < NVIS; ivis++){
    array1d_ivis_bbtotal_lee2002[ivis] = -999.;
  }
  
  /////////// Compute bbp(lambda = 555, z, algo = Wang) ///////////
  get_array1d_idepth_bbp555(array1d_idepth_chl,
                            idepth_max,
                            array1d_idepth_bbp555);
  
  /////////// Compute bbt(lambda = 555, z, algo = Wang) ///////////
  get_array1d_idepth_bbtotal555(array1d_ivis_bbw,
                                array1d_idepth_bbp555,
                                idepth_max,
                                array1d_idepth_bbtotal555);
  
  ///////// Compute gamma(z). /////////
  get_array1d_idepth_gamma(array1d_idepth_bbtotal555,
                           idepth_max,
                           array1d_idepth_gamma);

  /////////// Compute bbt(lambda, z, algo = Wang) ///////////
  get_array2d_idepth_ivis_bbtotal_wang2005(array1d_idepth_bbp555,
					   array1d_idepth_gamma,
					   array1d_ivis_bbw,
					   idepth_max,
					  array2d_idepth_ivis_bbtotal_wang2005);

  /////////// Compute bb(lambda_61, z, algo = Lee) ///////////
  get_array1d_ivis_bbtotal_lee2002(p,
				   array1d_ivis_bbtotal_lee2002);

  /////////// Compute bb(lambda_61, z) ///////////
  get_array2d_idepth_ivis_bbtotalin(array1d_ivis_bbtotal_lee2002,
				    array2d_idepth_ivis_bbtotal_wang2005,
				    idepth_max,
				    array2d_idepth_ivis_bbtotal);
  
  /////////// Print. ///////////
  if(DEBUG >= DEBUG_1){
    print_array1d_ivis_value(array1d_ivis_bbtotal_lee2002,
			     "bbt from Lee 2002 (m^-1)");
    print_array1d_ivis_value(array1d_ivis_bbw,
			     "b_bwater (m^-1)");
    print_chl_bbp555_bbtotal_gamma(array1d_idepth_chl,
                                   array1d_idepth_bbp555,
                                   array1d_idepth_bbtotal555,
                                   array1d_idepth_gamma);
    print_array2d_idepth_ivis_value(array2d_idepth_ivis_bbtotal_wang2005,
                                     "bbt from Wang 2005 (m^-1)");
    print_array2d_idepth_ivis_value(array2d_idepth_ivis_bbtotal,
                                     "bbt (m^-1)");
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_ivis_val:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are some values.
 * sat:
 *  S pour SeaWiFS et A pour MODISA.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array2d_idepth_iband_val:
 *  Array of dimensions NBDEPTHS * NBANDS = 101 * 6.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths of the bands of the satellite.
 *  Units: nm.
 *  The values are some values.
 */
void get_array2d_idepth_iband_val(float array2d_idepth_ivis_val[NBDEPTHS][NVIS],
                                  char sat,
                                  int idepth_max,
                                  float array2d_idepth_iband_val[NBDEPTHS][NBANDS]){
  int iband;
  int idepth;
  int ivis;
  for(idepth = 0; idepth < idepth_max; idepth++){
    for(iband = 0; iband < NBANDS; iband++){
      ivis = get_ivis(iband, sat);
      array2d_idepth_iband_val[idepth][iband] = array2d_idepth_ivis_val[idepth][ivis];
    }
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_chl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 * array2d_idepth_itime_pur:
 *  Array of dimensions NBDEPTHS * 9.
 *  The first dimension is the index of the geometrical depths.
 *  The second dimension is the index of the hours.
 *  The values are the photosynthetically usable radiation (PUR) for a pixel
 *  on a given day.
 *  The units are uEinstein*m^-2*s^-1.
 * array1d_idepth_ek:
 *  Array of dimension NBDEPTHS.
 *  The first dimension is the index of the geometrical depths.
 *  The values are the saturation irradiances.
 *  The units are uEinstein*m^-2*s^-1.
 * array1d_idepth_depthphy:
 *  Array of dimensions 101.
 *  The first dimension is the index of the geometrical depths.
 *  The values are the geometrical depths.
 *  The units are m.
 * array1d_itime_idepthphy_max:
 *  Array of dimension NTIMES = 9.
 *  The first dimension is the is the hours from 0 to 24 by step of 3 h.
 *  The values are the indices of the depth unto which the primary
 *  productivity will be computed (exclusive).
 * OUT
 * array2d_idepth_itime_pp:
 *  Array of dimensions (NBDEPTHS - 1) * (NTIMES - 1) = 100 * 8.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension is the hours from 0 to 21 by step of 3 h.
 *  The values are the primary productivity.
 *  The units are mgC.m^-2.d^-1.
 * Compute new primary productivity estimate for each depth and each time.
 * Use equation 5.
 * The units are mgC.m^-2.d^-1.
 */
void get_array2d_idepth_itime_pp(float array1d_idepth_chl[NBDEPTHS],
                                 float array2d_idepth_itime_pur
                                 [NBDEPTHS][NTIMES],
                                 float array1d_idepth_ek[NBDEPTHS],
                                 float array1d_idepth_depthphy[NBDEPTHS],
                                 int array1d_itime_idepth_max[NTIMES],
                                 float array2d_idepth_itime_pp
                                 [NBDEPTHS - 1][NTIMES - 1]){
  /*
   * Array of dimensions NTIMES = 9.
   * The first dimension is the index of the hours from 0 h to 24 h by step of
   * 3 h.
   * The values are the hours.
   * Units: h.
   */
  float array1d_itime_hour[NTIMES];
  /*
   * Chlorophyll-a concentration at cells bottomleft and bottomright.
   * Units: mgChla.m^-3.
   */
  float chlbottom;
  /*
   * Chlorophyll-a concentration at cells topleft and topright.
   * Units: mgChla.m^-3.
   */
  float chltop;
  /*
   * P^B_max.
   * Units: mgC (mg Chl-a)^-1 h^-1.
   */
  float P_Bmax_unit_h = 2.0;
  /*
   * Depth at cell bottomleft.
   * Units: m.
   */
  float depthbottomleft;
  /*
   * Depth at cell bottomright.
   * Units: m.
   */
  float depthbottomright;
  /*
   * Depth at cell topleft.
   * Units: m.
   */
  float depthtopleft;
  /*
   * Depth at cell topright.
   * Units: m.
   */
  float depthtopright;
  /*
   * Saturation irradiance at cells bottomleft and bottomright.
   * Units: umol photons*s^-1*m^-2.
   */
  float ekbottom;
  /*
   * Saturation irradiance at cells topleft and topright.
   * Units: umol photons*s^-1*m^-2.
   */
  float ektop;
  /*
   * Hour UTC at cells topleft and bottomleft.
   * Units: h.
   */
  float hourleft;
  /*
   * Hour UTC at cells topright and bottomright.
   * Units: h.
   */
  float hourright;
  /*
   * The index of the geometrical depths.
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth;
  /*
   * The index of the depth unto which the primary
   * productivity will be computed (exclusive).
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth_max;
  /*
   * The index of the depth unto which the primary
   * productivity will be computed for time itime. (exclusive).
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth_maxleft;
  /*
   * The index of the depth unto which the primary
   * productivity will be computed for time itime + 1. (exclusive).
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth_maxright;
  /*
   * Index of the time UTC from 0 to 24 by step 3.
   * Units: h.
   */
  int itime;
  /*
   * Primary productivity integrated over one time interval and one depth
   * interval.
   * Units: mgC.m^-2.d^-1.
   */
  float pp_one_cell;
  /*
   * Photosynthetically usable radiation at cell bottomleft.
   * Units: umol photons*s^-1*m^-2.
   */
  float purbottomleft;
  /*
   * Photosynthetically usable radiation at cell bottomright.
   * Units: umol photons*s^-1*m^-2.
   */
  float purbottomright;
  /*
   * Photosynthetically usable radiation at cell topleft.
   * Units: umol photons*s^-1*m^-2.
   */
  float purtopleft;
  /*
   * Photosynthetically usable radiation at cell topright.
   * Units: umol photons*s^-1*m^-2.
   */
  float purtopright;
  /*
   * Value at cell bottomleft.
   * Units: mgChla.m^-3.
   */
  float bottomleft;
  /*
   * Value at cell bottomright.
   * Units: mgChla.m^-3.
   */
  float bottomright;
  /*
   * Value at cell topleft.
   * Units: mgChla.m^-3.
   */
  float topleft;
  /*
   * Value at cell topright.
   * Units: mgChla.m^-3.
   */
  float topright;
  
  /////////// Initialize the times. ///////////
  memcpy(array1d_itime_hour,
         ARRAY1D_ITIME_HOUR,
         NTIMES * sizeof(float));
  array1d_itime_hour[NTIMES - 1] = 24.;
  
  /////////// Compute primary productivity for each depth and each time. /////
  // Loop on the times.
  for(itime = 0; itime <= NTIMES - 2; itime++){
    idepth_maxleft  = array1d_itime_idepth_max[itime];
    idepth_maxright = array1d_itime_idepth_max[itime + 1];
    idepth_max      = MAX(idepth_maxleft,
                          idepth_maxright);
    hourleft        = array1d_itime_hour[itime];
    hourright       = array1d_itime_hour[itime + 1];
    // Loop on the depths.
    for(idepth = 0; idepth <= idepth_max - 2; idepth++){
      chltop = array1d_idepth_chl[idepth];
      ektop  = array1d_idepth_ek[idepth];
      chlbottom = array1d_idepth_chl[idepth + 1];
      ekbottom  = array1d_idepth_ek[idepth + 1];
      depthtopleft     = array1d_idepth_depthphy[idepth];
      depthtopright    = array1d_idepth_depthphy[idepth];
      depthbottomleft  = array1d_idepth_depthphy[idepth + 1];
      depthbottomright = array1d_idepth_depthphy[idepth + 1];
      purtopleft       = array2d_idepth_itime_pur[idepth][itime];
      purtopright      = array2d_idepth_itime_pur[idepth][itime + 1];
      topleft          = getBelangerTmp(chltop, purtopleft, ektop);
      topright         = getBelangerTmp(chltop,purtopright, ektop);
      purbottomleft  = array2d_idepth_itime_pur[idepth + 1][itime];
      purbottomright = array2d_idepth_itime_pur[idepth + 1][itime + 1];
      bottomleft = getBelangerTmp(chlbottom, purbottomleft, ekbottom);
      bottomright = getBelangerTmp(chlbottom, purbottomright, ekbottom);
      
      pp_one_cell = P_Bmax_unit_h
      * get_one_cell_from_double_integral(hourleft,
                                          hourright,
                                          depthtopleft,
                                          depthbottomleft,
                                          depthtopright,
                                          depthbottomright,
                                          topleft,
                                          bottomleft,
                                          topright,
                                          bottomright);
      array2d_idepth_itime_pp[idepth][itime] = pp_one_cell;
      
      if(DEBUG >= DEBUG_1){
        print_pp_at_depth_and_time(idepth,
                                   itime,
                                   depthtopleft,
                                   depthtopright,
                                   depthbottomleft,
                                   depthbottomright,
                                   hourleft,
                                   hourright,
                                   chltop,
                                   chlbottom,
                                   purtopleft,
                                   purtopright,
                                   purbottomleft,
                                   purbottomright,
                                   ektop,
                                   ekbottom,
                                   topleft,
                                   topright,
                                   bottomleft,
                                   bottomright,
                                   pp_one_cell);
      } // End of DEBUG.
    }// End of the loop on the depths.
  }// End of loop on the times.
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_bbp555:
 *  Array of dimension NBDEPTHS = 101.					       
 *  The first dimension is the index of the geometric depths.		       
 *  The geometric depths are from 0 to 100 by step 1. Units: m.	       
 *  The values are the particulate backscattering coefficient at 555 nm.      
 *  The units are m^-1.                                           
 * array1d_idepth_gamma:
 *  Array of dimension NBDEPTHS = 101.				     
 *  The first dimension is the index of the geometrical depths.     
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.   
 *  The values are the parameter describing backscattering spectral 
 *  dependency (gamma)						     
 *  Unitless.                                                       
 * array1d_ivis_bbw:
 *  Array of dimension NVIS = 61.					       
 *  The first dimension are the wavelengths in the visible spectrum.	       
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.		       
 *  The values are the pure sea water backscattering coefficients (bb_w).     
 *  The units are m^-1.                                                  
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array2d_idepth_ivis_bbtotal:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the total backscattering coefficients (bb or bb_t).
 *  The units are m^-1.
 * Compute the total backscattering coefficients (bbt(lambda, z, algo = Wang)).
 * Reference:
 * Wang et al. 2005 (doi:10.1029/2002JC001653) equation 10.
 */
void get_array2d_idepth_ivis_bbtotal_wang2005(float array1d_idepth_bbp555
					      [NBDEPTHS],
					      float array1d_idepth_gamma
					      [NBDEPTHS],
					      float array1d_ivis_bbw[NVIS],
					      int idepth_max,
					      float array2d_idepth_ivis_bbtotal
					      [NBDEPTHS][NVIS]){
  float bb;
  float bbp555;
  float bbw555;
  int i555;
  int ivis;
  int idepth;
  float lambda;
  float gamma;
  i555 = (555 - 400) / 5;
  bbw555 = array1d_ivis_bbw[i555];
  for(idepth = 0; idepth < idepth_max; idepth++){
    bbp555 = array1d_idepth_bbp555[idepth];
    gamma = array1d_idepth_gamma[idepth];
    for(ivis = 0; ivis < NVIS; ivis++){
      lambda = 400. + ivis * 5.;
      bb = (bbw555 + bbp555) * pow(555. / lambda, gamma);
      array2d_idepth_ivis_bbtotal[idepth][ivis] = bb;
    }
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_ivis_Ed:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the downward irradiances.
 *  The units are umol photons.m^-2.s^-1.nm^-1.
 * array2d_idepth_ivis_Kd:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the diffuse attenuation coefficients.
 *  The units are m^-1.
 * array2d_idepth_ivis_atotal:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the total absorption coefficients (a or a_t).
 *  The units are m^-1.
 * array2d_idepth_ivis_bbtotal:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the total backscattering coefficients (bb or bb_t).
 *  The units are m^-1.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array2d_idepth_ivis_E0
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the scalar irradiances.
 *  The units are umol photons.m^-2.s^-1.nm^-1.
 * Compute the scalar irradiances at each depth and each wavelength.
 * The equation is the equation 7 of the ATBD.
 * E0(lambda, z) 
 * = Ed(lambda, z) * Kd(lambda, z) / ( a(lambda, z) + bb(lambda, z) )
 */
void get_array2d_idepth_ivis_E0(float array2d_idepth_ivis_Ed[NBDEPTHS][NVIS],
				float array2d_idepth_ivis_Kd[NBDEPTHS][NVIS],
                                float array2d_idepth_ivis_atotal
                                [NBDEPTHS][NVIS],
                                float array2d_idepth_ivis_bbtotal
                                [NBDEPTHS][NVIS],
                                int idepth_max,
                                float array2d_idepth_ivis_E0[NBDEPTHS][NVIS]){
  float atotal;
  float bbtotal;
  float Ed;
  float E0;
  int idepth;
  int ivis;
  float Kd;
  for(idepth = 0; idepth < idepth_max; idepth++){
//    Kd = array1d_idepth_Kd[idepth];
//    atotal = array2d_idepth_ivis_atotal[idepth][ISW];
//    bbtotal = array2d_idepth_ivis_bbtotal[idepth][ISW];
    for(ivis = 0; ivis < NVIS; ivis++){
      Ed = array2d_idepth_ivis_Ed[idepth][ivis];
      Kd = array2d_idepth_ivis_Kd[idepth][ivis];
      atotal = array2d_idepth_ivis_atotal[idepth][ivis];
      bbtotal = array2d_idepth_ivis_bbtotal[idepth][ivis];
      E0 = Ed * Kd / (atotal + bbtotal);
      array2d_idepth_ivis_E0[idepth][ivis] = E0;
    }
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_ivis_Kd:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the diffuse attenuation coefficients.
 *  The units are m^-1.
 * array1d_idepth_Z:
 *  Array of dimensions NBDEPTHS = 101.
 *  The first dimension are the indices of the geometrical depths.
 *  The values are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 * array1d_iwl_Ed0minus:
 *  Array of dimension NBWL = 83.
 *  The first dimension are the wavelengths from 290 nm to 700 nm by step 5.
 *  Units: nm.
 *  The values are the downward irradiances just below the water surface.
 *  Units: umol photons.m^-2.s^-1.nm^-1.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 6.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the downward irradiances.
 *  The units are umol photons.m^-2.s^-1.nm^-1.
 * Compute the downward irrandiances at each depth and each wavelength.
 * Ed(lambda, z_n)
 * = Ed(lambda, z_(n-1)) * exp(-Kd(lambda, z_n) * (z_n - z_(n-1)))
 */
void get_array2d_idepth_ivis_Ed(float array2d_idepth_ivis_Kd[NBDEPTHS][NVIS],
                                float array1d_idepth_Z[NBDEPTHS],
                                float array1d_iwl_Ed0minus[NBWL],
                                int idepth_max,
                                float array2d_idepth_ivis_Ed[NBDEPTHS][NVIS]){
  float Ed; // Ed(lambda, z_n).
  float Ed_top; // Ed(lambda, z_(n-1)).
  int idepth;
  int ivis;
  float Kd;
  float z; // z_n.
  float z_top; // z_(n-1).
  for(ivis = 0; ivis < NVIS; ivis++){
    Ed = array1d_iwl_Ed0minus[ivis + ID400];
    array2d_idepth_ivis_Ed[0][ivis] = Ed;
    for(idepth = 1; idepth < idepth_max; idepth++){
      Ed_top = array2d_idepth_ivis_Ed[idepth - 1][ivis];
      Kd = array2d_idepth_ivis_Kd[idepth][ivis];
      z_top = array1d_idepth_Z[idepth - 1];
      z = array1d_idepth_Z[idepth];
      Ed = Ed_top * exp( -Kd * (z - z_top) );
      array2d_idepth_ivis_Ed[idepth][ivis] = Ed;
    }
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_ivis_atotal:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the total absorption coefficients (a or a_t).
 *  The units are m^-1.
 * array2d_idepth_ivis_bbtotal:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the total backscattering coefficients (bb or bb_t).
 *  The units are m^-1.
 * thetas:
 *  Solar zenith angle.
 *  Units: Degrees.
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 * OUT
 * array2d_idepth_ivis_Kd:
 *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the diffuse attenuation coefficients.
 *  The units are m^-1.
 */
void get_array2d_idepth_ivis_Kd(float array2d_idepth_ivis_atotal
                                [NBDEPTHS][NVIS],
                                float array2d_idepth_ivis_bbtotal
                                [NBDEPTHS][NVIS],
                                float thetas,
                                int idepth_max,
                                float array2d_idepth_ivis_Kd[NBDEPTHS][NVIS]){  
  /*
   * Array of dimension NVIS = 61.
   * The first dimension are the wavelengths in the visible spectrum.
   * The wavelengths are from 400 to 700 by step 5. Units: nm.
   * The values are the total absorption coefficients (a or a_t).
   * The units are m^-1.
   */
  float array1d_ivis_atotal[NVIS];
  /*
   * Array of dimension NVIS = 61.
   * The first dimension are the wavelengths in the visible spectrum.
   * The wavelengths are from 400 to 700 by step 5. Units: nm.
   * The values are the (total) backscattering coefficients (bb or bb_t).
   * The units are m^-1.
   */
  float array1d_ivis_bbtotal[NVIS];
  /*
   * Array of dimension NVIS = 61.
   * The first dimension are the wavelengths in the visible spectrum.
   * The wavelengths are from 400 to 700 by step 5. Units: nm.
   * The values are the diffuse attenuation coefficients (Kd).
   * The units are m^-1.
   */
  float array1d_ivis_Kd[NVIS];
  int ivis;
  int idepth;
  float Kd;
  for(ivis = 0; ivis < NVIS; ivis++){
    array1d_ivis_atotal[ivis]  = -999.;
    array1d_ivis_bbtotal[ivis] = -999.;
    array1d_ivis_Kd[ivis]      = -999.;
  }
  for(idepth = 0; idepth < idepth_max; idepth++){
    get_array1d_ivis_value(array2d_idepth_ivis_atotal,
                            idepth,
                            array1d_ivis_atotal);
    get_array1d_ivis_value(array2d_idepth_ivis_bbtotal,
                            idepth,
                            array1d_ivis_bbtotal);
    calc_kdsimon(array1d_ivis_atotal,
                 array1d_ivis_bbtotal,
                 array1d_ivis_Kd,
                 thetas);
    for(ivis = 0; ivis < NVIS; ivis++){
      Kd = array1d_ivis_Kd[ivis];
      array2d_idepth_ivis_Kd[idepth][ivis] = Kd;
    }
  }
}
/* ------------------------------------------------------------------ */

/*
 * chl; Chlorphyll-a concentration. Units: mgChla.m^-3.
 * pur: Photosynthetically usable radiation (PUR). Units: uEinstein*m^-2*s^-1.
 * ek: saturation irradiance. Units: uEinstein*m^-2*s^-1.
 * Return 1 - e^(-pur/ek)
 * It is what is inside the double integral in Belanger et al. 2013 eq. (1)
 * or the ATBD eq. (5).
 */
float getBelangerTmp(float chl, float pur, float ek){
  float ret;
  ret = chl * (1. - exp(-pur / ek) );
  return ret;
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * depth: Bathymetry.
 *        Units: m.
 * max_depth: Maximal depth down to which the primary productivity is computed
 *            if allowed by the bathymetry.
 *            It is the same constant for each pixel: 100 m.
 *            Units: m.
 * depth_step: Difference between two depths.
 * 	       Units: m.
 * OUT
 * Return the index of the depth to which parameters are computed (exclusive).
 */
int get_idepth_max(float depth,
                   float max_depth,
                   float depth_step){
  return (int) ( MIN(depth, max_depth) / depth_step ) + 1;
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * Index of the wavelength of the bands of the satellite.
 * sat:
 *  S pour SeaWiFS et A pour MODISA.
 * Return the index of the nearest wavelength in the visible spectrum.
 * The wavelengths in the visible spectrum are from 400 to 700 by step 5.
 * Units: nm.
 */
int get_ivis(int iband, char sat){
  int ivis;
  float ivisf;
  float ivisl;
  float wl = 0.;
  if(sat == SEAWIFS){
    wl = ARRAY1D_IBAND_BANDSEAWIFS[iband];
  }else if(sat == MODISA){
    wl = ARRAY1D_IBAND_BANDMODISA[iband];
  }
  ivisf = (wl - 400) / 5;
  ivisl = lroundf(ivisf);
  assert(ivisl >= INT_MIN);
  assert(ivisl <= INT_MAX);
  ivis = ivisl;
  return ivis;
}
/* ------------------------------------------------------------------ */

/*
 * lower_bound_first_integral:        Lower bound of the first integral.
 * upper_bound_first_integral:        Upper bound of the first integral.
 * lower_bound_second_integral_left:  Lower bound of the second integral in the
 *                                    first column.
 * upper_bound_second_integral_left:  Upper bound of the second integral in the
 *                                    first column.
 * lower_bound_second_integral_right: Lower bound of the second integral in the
 *                                    second column.
 * upper_bound_second_integral_right: Upper bound of the second integral in the
 *                                    second column.
 * topleft:     Value in the first row and the first column of the array 2x2.
 * bottomleft:  Value in the second row and the first column of the array 2x2.
 * topright:    Value in the first row and the second column of the array 2x2.
 * bottomright: Value in the second row and the second column of the array 2x2.
 *
 * Return a scalar that is the double integration of the values in an array 2x2.
 * The values of the first column are integrated the with lower bound of the
 * first integral.
 * The values of the second column are integrated with the upper bound of the
 * first integral.
 * The values of the first row are integrated with the lower bound of the
 * second integral. This lower bound of the second integral can be variable in
 * function of the first integral.
 * The values of the second row are integrated with the upper bound of the
 * second integral. This upper bound of the second integral can be variable in
 * function of the first integral.
 * Use the trapezoidal rule. See http://en.wikipedia.org/wiki/Trapezoidal_rule.
 */
float get_one_cell_from_double_integral(float lower_bound_first_integral,
                                        float upper_bound_first_integral,
                                        float lower_bound_second_integral_left,
                                        float upper_bound_second_integral_left,
                                        float lower_bound_second_integral_right,
                                        float upper_bound_second_integral_right,
                                        float topleft,
                                        float bottomleft,
                                        float topright,
                                        float bottomright){
  float ret;
  ret = (upper_bound_first_integral - lower_bound_first_integral)
  * ( ( (upper_bound_second_integral_left
         - lower_bound_second_integral_left)
       * (topleft + bottomleft)
       / 2. )
     + ( (upper_bound_second_integral_right
          - lower_bound_second_integral_right)
        * (topright + bottomright)
        / 2. ) )
  / 2.;
  return ret;
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_ivis_Ed:
 *  Array of dimensions NVIS = 61.
 *  The first dimension are the  wavelengths from 400 nm to 700 nm by step
 *  of 5. Units: nm.
 *  The values are the downward irradiances.
 *  The units are umol photons.m^-2.s^-1.nm^-1.
 * Return the photosynthetically active radiation (PAR) integrated
 * over the wavelenghts.
 * The units are umol photons.m^-2.s^-1.
 */
float get_PAR(float array1d_ivis_Ed[NVIS]){
  float Ed;
  int ivis;
  float PAR = 0.;
  for(ivis = 0; ivis < NVIS; ivis++){
    Ed = array1d_ivis_Ed[ivis];
    PAR += (Ed * 5.);
  }
  return PAR;
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_pp:
 *  Array of dimension NBDEPTHS - 1 = 100.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the primary productivities.
 *  Units: mgC.m^-2.d^-1.
 * OUT
 * pp:
 *  Primary productivity.
 *  Units: mgC.m^-2.d^-1.
 */
float get_pp(float array1d_idepth_pp[NBDEPTHS - 1]){
  /*
   * The index of the geometrical depths.
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth;
  /*
   * Primary productivity.
   * Units: mgC.m^-2.d^-1.
   */
  float pp = 0.;
  /*
   * Primary productivity.
   * Units: mgC.m^-2.d^-1.
   */
  float pp_tmp;
  // Loop on the depths.
  for(idepth = 0; idepth <= NBDEPTHS - 2; idepth++){
    pp_tmp = array1d_idepth_pp[idepth];
    if(pp_tmp > 0){
      pp += pp_tmp;
    }
  } // End of the loop on the depths.
  return pp;
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_PAR:
 *  Array of dimensions NBDEPTHS.
 *  The first dimension is the index of the physical depths.
 *  The values are the photosynthetically active radiation (PAR) integrated
 *  over the wavelenghts.
 *  The units are umol photons.m^-2.s^-1.
 * itime:
 * The index of the hour for the hours from 0 to 24 by step of 3 h.
 * OUT
 * array2d_idepth_itime_PAR:
 *  Array of dimensions NBDEPTHS * NTIMES.
 *  The first dimension is the index of the physical depths.
 *  The second dimension is the hours from 0 to 24 by step of 3 h.
 *  The values are the photosynthetically active radiation (PAR) integrated
 *  over the wavelenghts.
 *  The units are umol photons.m^-2.s^-1.
 * Fill the array of PAR for one specified time.
 */
void fill_array2d_idepth_itime_PAR(float array1d_idepth_PAR[NBDEPTHS],
                                   int itime,
                                   float array2d_idepth_itime_PAR
                                   [NBDEPTHS][NTIMES]){
  int idepth;
  for(idepth = 0; idepth < NBDEPTHS; idepth++){
    array2d_idepth_itime_PAR[idepth][itime] = array1d_idepth_PAR[idepth];
  }
}
/* ------------------------------------------------------------------ */

/*
 * Linear interpolation.
 */
float interp_line(float x1, float x2, float x, float y1, float y2){
  float a,b,y;
  a=(y2-y1)/(x2-x1);
  b=y1-(a*x1);
  y=a*x+b;
  return y;
}
/* ------------------------------------------------------------------ */

/*
 * aphy443:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The values are the phytoplankton absorption coefficient at 443 nm.
 *  The units are m^-1.
 * Print aphy443.
 */
void print_aphy443(float aphy443[NBDEPTHS]){
  int idepth;
  printf(" Depth (m) aphy443 (m^-1)\n");
  for(idepth = 0; idepth < NBDEPTHS; idepth++){
    printf("       %03.0f       %8f\n",
           idepth * DEPTH_STEP,
           aphy443[idepth]);
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * name_col1:
 *  The name of column 1.
 * name_col2:
 *  The name of column 2.
 * array1d_iband_valcol1:
 *  Array of dimension NBANDS = 6.
 *  The first dimension are the wavelengths of the bands of the satellite.
 *  The values are the values for column 1.
 * array1d_iband_valcol2:
 *  Array of dimension NBANDS = 6.
 *  The first dimension are the wavelengths of the bands of the satellite.
 *  The values are the values for column 2.
 */
void print_array1d_iband_3col(char* name_col1,
			      char* name_col2,
			      char* name_col3,
			      float array1d_iband_valcol1[NBANDS],
			      float array1d_iband_valcol2[NBANDS],
			      float array1d_iband_valcol3[NBANDS]){
  char header[500] = "";
  int iband;
  float valcol1;
  float valcol2;
  float valcol3;
  strcat(header, name_col1);
  strcat(header, " ");
  strcat(header, name_col2);
  strcat(header, " ");
  strcat(header, name_col3);
  strcat(header, " ");
  printf("%s\n", header);
  for(iband = 0; iband < NBANDS; iband++){
    valcol1 = array1d_iband_valcol1[iband];
    valcol2 = array1d_iband_valcol2[iband];
    valcol3 = array1d_iband_valcol3[iband];
    printf("%f  %f    %f\n", valcol1, valcol2, valcol3);
  }
  printf("\n");
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_itime_ivalue:
 *  Array of dimensions NTIME = 9.
 *  The first dimension is the is the hours from 0 to 24 by step of 3 h.
 *  The values are the values of some product.
 * value_name:
 *  Name of the product.
 * Print the values of the product for each time.
 */
void print_array1d_itime_ivalue(int array1d_itime_ivalue[NTIMES],
                                char* value_name){
  char header[500] = "Time UTC ";
  int itime;
  int ivalue;
  int time;
  strcat(header, value_name);
  printf("%s\n", header);
  for(itime = 0; itime < NTIMES; itime++){
    time = 3 * itime;
    ivalue = array1d_itime_ivalue[itime];
    printf("  %2d UTC %3d\n", time, ivalue);
  }
  printf("\n");
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_ivis_budgetphy:
 *  Array of dimensions NBANDS = 61.
 *  The first dimension are the wavelengths in the visible spectrum.
 *  The wavelengths are from 400 to 700 by step 5. Units: nm.
 *  The values are the values of some product.
 * value_name:
 *  Name of the product.
 * Print the values of the product for each wavelength.
 */
void print_array1d_ivis_value(float array1d_ivis_value[NVIS],
			      char* value_name){
  char header1[500] = "Wavelength(nm) ";
  int ivis;
  int lambda;
  float value;
  strcat(header1, value_name);
  printf(" %s\n", header1);
  for(ivis = 0; ivis < NVIS; ivis++){
    lambda = 400 + ivis * 5;
    value = array1d_ivis_value[ivis];
    printf(" %d %19f\n", lambda, value);
  }
  printf("\n");
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_chl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 */
void print_array1d_idepth_chl(float array1d_idepth_chl[NBDEPTHS]){
  float chl;
  int idepth;
  printf("array1d_idepth_chl (mg Chl-a m^-3)\n");
  printf("Depth[m] chl\n");
  for(idepth = 0; idepth < NBDEPTHS; idepth++){
    chl = array1d_idepth_chl[idepth];
    printf("%.0f: %f \n",idepth * DEPTH_STEP, chl);
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 *
 * array1d_idepth_pp:
 *  Array of dimension NBDEPTHS - 1 = 100.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the primary productivities.
 *  Units: mgC.m^-2.d^-1.
 */
void print_array1d_idepth_pp(float array1d_idepth_pp[NBDEPTHS - 1]){
  float depth_bottom;
  float depth_top;
  int idepth;
  float pp;
  printf("array1d_idepth_pp (mgC.m^-2.d^-1)\n");
  for(idepth = 0; idepth < NBDEPTHS - 1; idepth++){
    depth_top = idepth * DEPTH_STEP;
    depth_bottom = depth_top + DEPTH_STEP;
    pp = array1d_idepth_pp[idepth];
    printf("%.0f to %.0f m: %f \n", depth_top, depth_bottom, pp);
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_iband_value:
 *  Array of dimensions NBDEPTHS * NBANDS = 101 * 6.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension are the wavelengths of the bands of the satellite.
 *  Units: nm.
 *  The values are the values of some product.
 * value_name:
 *  Name of the product.
 * Print the values of the product for each depth and each wavelength.
 */
void print_array2d_idepth_iband_value(float array2d_idepth_iband_value[NBDEPTHS][NBANDS],
                                      char* value_name){
  int iband;
  int idepth;
  char header[500] = "Depth(m) ";
  float value;
  strcat(header, value_name);
  printf("%s\n", header);
  for(idepth = 0; idepth < NBDEPTHS; idepth++){
    printf("%03.0f", idepth * DEPTH_STEP);
    iband = 0;
    value = array2d_idepth_iband_value[idepth][iband];
    printf("      %f", value);
    for(iband = 1; iband < NBANDS; iband++){
      value = array2d_idepth_iband_value[idepth][iband];
      printf(" %f", value);
    }
    printf("\n");
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_itime_value:
 *  Array of dimensions NBDEPTHS * NTIMES = 101 * 9.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension is the hours from 0 to 24 by step of 3 h.
 *  Units: Time UTC.
 *  The values are the values of some product.
 * value_name:
 *  Name of the product.
 * Print the values of the product for each depth and each time.
 */
void print_array2d_idepth_itime_value(float array2d_idepth_itime_value
                                      [NBDEPTHS][NTIMES],
                                      char* value_name){
  int itime;
  int idepth;
  char line1[500] = "         ";
  char line2[500] = "Depth(m)  00UTC       03UTC       06UTC       09UTC       12UTC       15UTC       18UTC       21UTC       24UTC";
  float value;
  strcat(line1, value_name);
  printf("%s\n", line1);
  printf("%s\n", line2);
  for(idepth = 0; idepth < NBDEPTHS; idepth++){
    printf("%03.0f", idepth * DEPTH_STEP);
    itime = 0;
    value = array2d_idepth_itime_value[idepth][itime];
    printf("      %11.6f", value);
    for(itime = 1; itime < NTIMES; itime++){
      value = array2d_idepth_itime_value[idepth][itime];
      printf(" %11.6f", value);
    }
    printf("\n");
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array2d_idepth_itime_value:
 *  Array of dimensions NBDEPTHS - 1 * NTIMES - 1 = 100 * 8.
 *  The first dimension are the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The second dimension is the hours from 0 to 21 by step of 3 h.
 *  Units: Time UTC.
 *  The values are the values of some product.
 * value_name:
 *  Name of the product.
 * Print the values of the product for each depth and each time.
 */
void print_array2d_idepthminus1_itime_value(float array2d_idepth_itime_value[NBDEPTHS - 1][NTIMES - 1],
                                      char* value_name){
  int itime;
  int idepth;
  char line1[500] = "         ";
  char line2[500] = "Depth(m) 00UTC    03UTC    06UTC    09UTC    12UTC    15UTC    18UTC    21UTC";
  float value;
  strcat(line1, value_name);
  printf("%s\n", line1);
  printf("%s\n", line2);
  for(idepth = 0; idepth < NBDEPTHS - 1; idepth++){
    printf("%03.0f", idepth * DEPTH_STEP);
    itime = 0;
    value = array2d_idepth_itime_value[idepth][itime];
    printf("      %f", value);
    for(itime = 1; itime < NTIMES - 1; itime++){
      value = array2d_idepth_itime_value[idepth][itime];
      printf(" %f", value);
    }
    printf("\n");
  }
}
/* ------------------------------------------------------------------ */
  
  /*
   * IN
   * array2d_idepth_ivis_value:
   *  Array of dimensions NBDEPTHS * NVIS = 101 * 61.
   *  The first dimension are the geometrical depths.
   *  The geometrical depths are from 0 to 100 by step 1. Units: m.
   *  The second dimension are the wavelengths from 400 nm to 700 nm by step
   *  of 5. Units: nm.
   *  The values are the values of some product.
   * value_name:
   *  Name of the product.
   * Print the values of the product for each depth and each wavelength.
   */
  void print_array2d_idepth_ivis_value(float array2d_idepth_ivis_value
                                       [NBDEPTHS][NVIS],
                                       char* value_name){
    float depth;
    char header1[500] = "Depth(m) ";
    char header2[100000] = "         ";
    int idepth;
    int ivis;
    int lambda;
    char slambda[12];
    float value;
    strcat(header1, value_name);
    printf(" %s\n", header1);
    for(ivis = 0; ivis < NVIS; ivis++){
      lambda = 400 + ivis * 5;
      sprintf(slambda, "%d        ", lambda);
      strcat(header2, slambda);
    }
    printf("%s\n", header2);
    for(idepth = 0; idepth < NBDEPTHS; idepth++){
      depth = idepth * DEPTH_STEP;
      printf("%03.0f      ", depth);
      for(ivis = 0; ivis < NVIS; ivis++){
        value = array2d_idepth_ivis_value[idepth][ivis];
        printf("%10f ", value);
      }
      printf("\n");
    }
  }
  /* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_chl:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the chlorophyll-a concentration.
 *  The units are mg Chl-a m^-3.
 * array1d_idepth_bbp555:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the particulate backscattering coefficient at 555 nm.
 *  The units are m^-1.
 * array1d_idepth_bbtotal555:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The values are the (total) backscattering coefficient at 555 nm.
 *  The units are m^-1.
 * array1d_idepth_gamma:
 *  Array of dimension NBDEPTHS = 101.
 *  The first dimension is the index of the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 *  The values are the parameter describing backscattering spectral
 *  dependency (gamma)
 *  Unitless.
 */
void print_chl_bbp555_bbtotal_gamma(float array1d_idepth_chl[NBDEPTHS],
                                    float array1d_idepth_bbp555[NBDEPTHS],
                                    float array1d_idepth_bbtotal555[NBDEPTHS],
                                    float array1d_idepth_gamma[NBDEPTHS]){
  float bbp555;
  float bbt555;
  float chl;
  float depth;
  float gamma;
  /*
   * The index of the geometrical depths.
   * The geometrical depths are from 0 to 100 by step 1. Units: m.
   */
  int idepth;
  printf("Depth chl            bbp555      bbt555      gamma\n");
  printf("  (m) (mg Chla.m^-3) (m^-1)      (m^-1)\n");
  for(idepth = 0; idepth < NBDEPTHS; idepth++){
    depth = idepth * DEPTH_STEP;
    chl = array1d_idepth_chl[idepth];
    bbp555 = array1d_idepth_bbp555[idepth];
    bbt555 = array1d_idepth_bbtotal555[idepth];
    gamma = array1d_idepth_gamma[idepth];
    printf("  %03.0f %14f %11f %11f %11f\n",
           depth,
           chl,
           bbp555,
           bbt555,
           gamma);
  }
  
}
/* ------------------------------------------------------------------ */

/*
 * idepth_max:
 *  Index of the depth to which parameters are computed (exclusive).
 */
void print_idepth_max(int idepth_max){
  printf(" idepth_max: %d\n", idepth_max);
}
  /* ------------------------------------------------------------------ */
  
  /*
   * array1d_iband_Rrs: Rrs.
   * array1d_iband_a: a.
   * array1d_iband_bb: bb.
   * Print Rrs, a and bb for the 6 bands of the satellite.
   */
  void print_iop_6bands(float array1d_iband_Rrs[NBANDS],
                        float array1d_iband_a[NBANDS],
                        float array1d_iband_bb[NBANDS]){
    int iband;
    float Rrs, a, bb;
    printf("Rrs      atotal\n");
    printf("(m^-1)   (m^-1)\n");
    for(iband = 0; iband < NBANDS; iband++){
      Rrs = array1d_iband_Rrs[iband];
      a = array1d_iband_a[iband];
      bb = array1d_iband_bb[iband];
      printf("%f %f \n", Rrs, a);
    }
}
  /* ------------------------------------------------------------------ */

/*
 * Affiche le PUR moyen et le Ek pour chaque profondeur.
 * meanPUR: Le PUR moyen
 * Ek: Le Ek
 */
void print_meanpur_ek(float meanPUR[NBDEPTHS], float Ek[NBDEPTHS]){
  int iprof;
  printf(" Unites de Profondeur: m\n");
  printf(" Unites de PUR moyen:  uE*s^-1*m^-2\n");
  printf(" Unites de Ek:         uE*s^-1*m^-2\n");
  printf(" Profondeur PUR moyen  Ek\n");
  for(iprof = 0; iprof < NBDEPTHS; iprof++){
    printf("  %03.0f       %10.6f %f\n",
           iprof * DEPTH_STEP,
           meanPUR[iprof],
           Ek[iprof]);
  }
}
/* ------------------------------------------------------------------ */

/*
 * Affiche la production primaire.
 * pp: La production primaire.
 */
void print_pp(float pp){
  printf("Primary productivity (mgC*m^-2*d^-1): %f\n", pp);
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * idepth:
 *  The index of the geometrical depths.
 *  The geometrical depths are from 0 to 100 by step 1. Units: m.
 * itime:
 *  Index of the time UTC from 0 to 24 by step 3.
 *  Units: h.
 * depthtopleft:
 *  Depth at cell topleft.
 *  Units: m.
 * depthtopright:
 *  Depth at cell topright.
 *  Units: m.
 * depthbottomleft:
 *  Depth at cell bottomleft.
 *  Units: m.
 * depthbottomright:
 *  Depth at cell bottomright.
 *  Units: m.
 * hourleft:
 *  Hour UTC at cells topleft and bottomleft.
 *  Units: h.
 * hourright:
 *  Hour UTC at cells topright and bottomright.
 *  Units: h.
 * chltop:
 *  Chlorophyll-a concentration at cells topleft and topright.
 *  Units: mgChla.m^-3.
 * chlbottom:
 *  Chlorophyll-a concentration at cells bottomleft and bottomright.
 *  Units: mgChla.m^-3.
 * purtopleft:
 *  Photosynthetically usable radiation at cell topleft.
 *  Units: umol photons*s^-1*m^-2.
 * purtopright:
 *  Photosynthetically usable radiation at cell topright.
 *  Units: umol photons*s^-1*m^-2.
 * purbottomleft:
 *  Photosynthetically usable radiation at cell bottomleft.
 *  Units: umol photons*s^-1*m^-2.
 * purbottomright:
 *  Photosynthetically usable radiation at cell bottomright.
 *  Units: umol photons*s^-1*m^-2.
 * ektop:
 *  Saturation irradiance at cells topleft and topright.
 *  Units: umol photons*s^-1*m^-2.
 * ekbottom:
 *  Saturation irradiance at cells bottomleft and bottomright.
 *  Units: umol photons*s^-1*m^-2.
 * topleft:
 *  Value at cell topleft.
 *  Units: mgChla.m^-3.
 * topright:
 *  Value at cell topright.
 *  Units: mgChla.m^-3.
 * bottomleft:
 *  Value at cell bottomleft.
 *  Units: mgChla.m^-3.
 * bottomright:
 *  Value at cell bottomright.
 *  Units: mgChla.m^-3.
 * pp_one_cell:
 *  Primary productivity integrated over one time interval and one depth
 *  interval.
 *  Units: mgC.m^-2.d^-1.
 * Print primary productivity and intermdiate parameters over one time
 * interval and one depth interval.
 */
void print_pp_at_depth_and_time(int idepth,
                                int itime,
                                float depthtopleft,
                                float depthtopright,
                                float depthbottomleft,
                                float depthbottomright,
                                float hourleft,
                                float hourright,
                                float chltop,
                                float chlbottom,
                                float purtopleft,
                                float purtopright,
                                float purbottomleft,
                                float purbottomright,
                                float ektop,
                                float ekbottom,
                                float topleft,
                                float topright,
                                float bottomleft,
                                float bottomright,
                                float pp_one_cell){
  printf("idepth: %d\n", idepth);
  printf(" itime: %d\n", itime);
  printf("  depthtopleft (m): %f\n", depthtopleft);
  printf("  depthtopright (m): %f\n", depthtopright);
  printf("  depthbottomleft (m): %f\n", depthbottomleft);
  printf("  depthbottomright (m): %f\n", depthbottomright);
  printf("  hourleft (h): %f\n", hourleft);
  printf("  hourright (h): %f\n", hourright);
  printf("  chltop (mgChla.m^-3): %f\n", chltop);
  printf("  chlbottom (mgChla.m^-3): %f\n", chlbottom);
  printf("  purtopleft (umol photons*s^-1*m^-2): %f\n", purtopleft);
  printf("  purtopright (umol photons*s^-1*m^-2): %f\n", purtopright);
  printf("  purbottomleft (umol photons*s^-1*m^-2): %f\n", purbottomleft);
  printf("  purbottomright (umol photons*s^-1*m^-2): %f\n", purbottomright);
  printf("  ektop (umol photons*s^-1*m^-2): %f\n", ektop);
  printf("  ekbottom (umol photons*s^-1*m^-2): %f\n", ekbottom);
  printf("  topleft (mgChla.m^-3): %f\n", topleft);
  printf("  topright (mgChla.m^-3): %f\n", topright);
  printf("  bottomleft (mgChla.m^-3): %f\n", bottomleft);
  printf("  bottomright (mgChla.m^-3): %f\n", bottomright);
  printf("  pp_one_cell (mgC.m^-2): %f\n", pp_one_cell);
}
/* ------------------------------------------------------------------ */
  
  /*
   * Affiche le PUR pour chaque profondeur.
   * k: L'indice de l'heure
   * PUR: Le PUR
   */
  void print_pur(int k, float PUR[NBDEPTHS][NTIMES]){
    int iprof;
    printf("  PUR\n");
    for(iprof = 0; iprof < NBDEPTHS; iprof++){
      printf("   %03.0f (uE*s^-1*m^-2): %f\n",
             iprof * DEPTH_STEP,
             PUR[iprof][k]);
    }
  }
	/* ------------------------------------------------------------------ */

/*
 * Affiche les parametres d'entree pour le calcul de thetas et affiche thetas.
 * julien: Jour julien
 * hh: Heure UTC
 * xlat: Latitude
 * xlon: Longitude
 * thetas
 */
void print_thetas(int julien, float hh, float xlat, float xlon, float thetas){
  printf("  Calcul de thetas pour Kd\n");
  printf("   ENTREES\n");
  printf("    julien %d\n", julien);
  printf("    hh (heure UTC en heures): %.0f\n", hh);
  printf("    xlat (degres): %f\n", xlat);
  printf("    xlon (degres): %f\n", xlon);
  printf("   SORTIE\n");
  printf("    thetas pour le calcul de Kd (degres): %f\n", thetas);
}
  /* ------------------------------------------------------------------ */
  
  /*
   * Affiche les profondeurs geometriques.
   * Z: Les profondeurs geometriques (en m).
   */
  void print_Z(float Z[NBDEPTHS]){
    int i;
    printf("  Profondeurs geometriques (m)\n");
    for(i = 0; i < NBDEPTHS; i++){
      printf("                      %f\n", Z[i]);
    }
  }
  /* ------------------------------------------------------------------ */

/*
 * array2d_k_ivis_Ed0moins:
 *  Array of dimensions 9 * 61.
 *  The first dimension is the hours from 0 to 24 by step of 3 h.
 *  The second dimension is the wavelenght from 400 nm to 700 nm by step of 5
 *  nm.
 *  The values are the downward irradiances just below the surface water
 *  (Ed0moins) for one pixel.
 *  The units are uEinstein*m^-2*s^-1*nm^-1.
 * k:
 *  Index of the hours in Lheures.
 * Ed_pixel:
 *  Array of dimensions 81.
 *  The second dimension is the wavelenght from 400 nm to 700 nm by step of 5
 *  nm.
 *  The values are the downward irradiances just below the surface water
 *  (Ed0moins) for one pixel.
 *  The units are uEinstein*m^-2*s^-1*nm^-1.
 * Select the irradiances for one time. Fill the wavelengths below 400 nm with
 * fill values.
 */
void read_Ed_pixel(float array2d_k_ivis_Ed0moins[NTIMES][NVIS],
                   int k,
                   float Ed_pixel[NBWL]){
  int iwl;
  int n_too_low;
  
  n_too_low = NBWL - NVIS;
  for(iwl = 0; iwl < NBWL; iwl++){
    if(iwl < n_too_low){
      Ed_pixel[iwl] = -999.;
    }else{
      Ed_pixel[iwl] = array2d_k_ivis_Ed0moins[k][iwl - n_too_low];
    }
  }
  
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_pp:
 *  Array of dimension NBDEPTHS - 1 = 100.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the primary productivities.
 *  Units: mgC.m^-2.d^-1.
 * chl:
 *  The value of the option chl to use the chlorophyll-a concentration.
 *  0 for the chlorophyll-a concentration vertical profile in the water column.
 *  1 for the surface chlorophyll-a concentration.
 * Test if array1d_idepth_pp = array1d_idepth_pp_ref.
 */
void test_get_array1d_idepth_pp(float array1d_idepth_pp[NBDEPTHS - 1],
				int chl){
  float array1d_idepth_pp_ref[NBDEPTHS - 1];
  float ARRAY1D_IDEPTH_PP_REF_COLUMN[NBDEPTHS - 1]
    = {9.165866,9.075148,8.981170,8.881427,8.773249,8.653952,8.521031,8.372564,8.207620,8.026717,7.832196,7.628336,7.421108,7.217455,7.024190,6.846815,6.688540,6.549751,6.428077,6.318885,6.216055,6.112847,6.002728,5.879945,5.739959,5.579689,5.397561,5.193474,4.968619,4.725286,4.466611,4.196304,3.918381,3.636929,3.355901,3.078957,2.809335,2.549778,2.302494,2.069162,1.850944,1.648532,1.462206,1.291892,1.137228,0.997624,0.872317,0.760429,0.661005,0.573055,0.495580,0.427599,0.368165,0.185582,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000};
  float ARRAY1D_IDEPTH_PP_REF_SURFACE[NBDEPTHS - 1]
  = {9.120220,8.932844,8.731698,8.514927,8.280903,8.028418,7.756937,7.466886,7.159950,6.839290,6.509616,6.176983,5.848259,5.530313,5.229079,4.948763,4.691380,4.456733,4.242784,4.046261,3.863321,3.690129,3.523285,3.360072,3.198549,3.037541,2.876546,2.715611,2.555200,2.396057,2.239088,2.085261,1.935529,1.790770,1.651747,1.519081,1.393247,1.274570,1.163235,1.059296,0.962700,0.873297,0.790861,0.715110,0.645717,0.582327,0.524566,0.472054,0.424412,0.381267,0.342259,0.307042,0.275291,0.246697,0.220973,0.197852,0.103890,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000};
  int cmp;
  
  /////////// Get reference primary productivity(z) ///////////
  if(chl == CHL_SURFACE){
    memcpy(array1d_idepth_pp_ref,
	   &ARRAY1D_IDEPTH_PP_REF_SURFACE[0],
	   (NBDEPTHS - 1) * sizeof(float));
  }else if(chl == CHL_COLUMN){
    memcpy(array1d_idepth_pp_ref,
	   &ARRAY1D_IDEPTH_PP_REF_COLUMN[0],
	   (NBDEPTHS - 1) * sizeof(float));
  }
  /////////// Compare ///////////
  printf("Test of get_array1d_idepth_pp()\n");
  printf(" Options:\n");
  if(chl == CHL_SURFACE){
    printf(" chl = surface\n");
  }else if(chl == CHL_COLUMN){
    printf(" chl = column\n");
  }
  print_array1d_idepth_pp(array1d_idepth_pp);
  cmp = array1dfcmp(array1d_idepth_pp, array1d_idepth_pp_ref, NBDEPTHS - 1);
  if(cmp){
    printf("FAIL\n");
  }else{
    printf("PASS\n");
  }
}
/* ------------------------------------------------------------------ */

/*
 * IN
 * array1d_idepth_pp:
 *  Array of dimension NBDEPTHS - 1 = 100.
 *  The first dimension is the index of the geometric depths.
 *  The geometric depths are from 0 to 100 by step 1. Units: m.
 *  The values are the primary productivities.
 *  Units: mgC.m^-2.d^-1.
 * chl:
 *  The value of the option chl to use the chlorophyll-a concentration.
 *  0 for the chlorophyll-a concentration vertical profile in the water column.
 *  1 for the surface chlorophyll-a concentration.
 * Test if array1d_idepth_pp_from_atm = array1d_idepth_pp_ref.
 */
void test_get_array1d_idepth_pp_from_atm(float array1d_idepth_pp[NBDEPTHS - 1],
					 int chl){
  /*
   * Array of dimension NBDEPTHS - 1 = 100.
   * The first dimension is the index of the geometric depths.
   * The geometric depths are from 0 to 100 by step 1. Units: m.
   * The values are the primary productivities.
   * Units: mgC.m^-2.d^-1.
   */
  float array1d_idepth_pp_ref[NBDEPTHS - 1];
  /*
   * Array of dimension NBDEPTHS - 1 = 100.
   * The first dimension is the index of the geometric depths.
   * The geometric depths are from 0 to 100 by step 1. Units: m.
   * The values are the primary productivities.
   * Units: mgC.m^-2.d^-1.
   * With the chlorophyll-a concentration vertical profile in the water column.
   */
  float ARRAY1D_IDEPTH_PP_REF_COLUMN[NBDEPTHS - 1]
  = {7.312701,7.213396,7.104436,6.984052,6.851217,6.706019,6.549954,6.386131,6.219142,6.054544,5.898037,5.754498,5.627139,5.517017,5.422954,5.341844,5.269215,5.199850,5.128415,5.049937,4.960158,4.855750,4.734463,4.595119,4.437569,4.262619,4.071864,3.867557,3.652403,3.429402,3.201684,2.972346,2.744327,2.520310,2.302652,2.093337,1.893964,1.705737,1.529494,1.365736,1.214662,1.076212,0.950117,0.835938,0.733108,0.640966,0.558790,0.485827,0.421314,0.364493,0.314631,0.271026,0.233016,0.157494,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000};
  /*
   * Array of dimension NBDEPTHS - 1 = 100.
   * The first dimension is the index of the geometric depths.
   * The geometric depths are from 0 to 100 by step 1. Units: m.
   * The values are the primary productivities.
   * Units: mgC.m^-2.d^-1.
   * With surface chlorophyll-a concentration.
   */
  float ARRAY1D_IDEPTH_PP_REF_SURFACE[NBDEPTHS - 1]
  = {7.276281,7.100162,6.906811,6.695390,6.466120,6.220589,5.961941,5.694836,5.425088,5.158994,4.902441,4.660063,4.434651,4.226973,4.035987,3.859332,3.693932,3.536549,3.384216,3.234498,3.085626,2.936507,2.786663,2.636134,2.485361,2.335063,2.186132,2.039538,1.896248,1.757170,1.623110,1.494745,1.372607,1.257085,1.148426,1.046745,0.952045,0.864230,0.783121,0.708477,0.640008,0.577388,0.520272,0.468301,0.421114,0.378354,0.339673,0.304737,0.273227,0.244842,0.219301,0.196341,0.175719,0.157211,0.140612,0.125734,0.088520,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000};
  int cmp;
  /////////// Get reference primary productivity(z) ///////////
  if(chl == CHL_SURFACE){
    memcpy(array1d_idepth_pp_ref,
	   &ARRAY1D_IDEPTH_PP_REF_SURFACE[0],
	   (NBDEPTHS - 1) * sizeof(float));
  }else if(chl == CHL_COLUMN){
    memcpy(array1d_idepth_pp_ref,
	   &ARRAY1D_IDEPTH_PP_REF_COLUMN[0],
	   (NBDEPTHS - 1) * sizeof(float));
  }
  /////////// Compare ///////////
  printf("Test of get_array1d_idepth_pp_from_atm()\n");
  printf(" Options:\n");
  if(chl == CHL_SURFACE){
    printf(" chl = surface\n");
  }else if(chl == CHL_COLUMN){
    printf(" chl = column\n");
  }
  print_array1d_idepth_pp(array1d_idepth_pp);
  cmp = array1dfcmp(array1d_idepth_pp, array1d_idepth_pp_ref, NBDEPTHS - 1);
  if(cmp){
    printf("FAIL\n");
  }else{
    printf("PASS\n");
  }
}
/* ------------------------------------------------------------------ */

/* ================================= MAIN ================================= */
/*
 * Uncomment to test.
 */
int main(int argc, char *argv[]){

  /////////////////////////////////////////////////////////////////////////////
  /////////// test for get_array1d_idepth_pp with pixels at rows 2  ///////////
  /////////// and 48 of the prototype for Mathieu in                ///////////
  /////////// /Volumes/Disk6TB/Takuvik/Teledetection/Couleur/Other/ ///////////
  /////////// Mathieu/Malina/Fig8/IN/IN20140815/                    ///////////
  /////////// PPARR5_Mathieu_BG_RRS_Profile_1_1000.txt              ///////////
  /////////////////////////////////////////////////////////////////////////////
  
  /////////// Declaration of inputs ///////////
  
  /*
   * Latitude.			 
   * The units are degrees North.
   */
  float lat;
  /*
   * Longitude.			
   * From -180 to 180.		
   * The units are degrees East.
   */
  float lon;
  int year;
  int month;
  /* Day of month. */
  int day;
  /* Day of year. */
  int doy;
  /*
   * Bathymetry.     
   * The units are m.
   */
  float depth;
  /*
   * S for SeaWiFS and A for MODIS-AQUA.
   */
  char rrs_type;
  /*
   * Array of dimension NBANDS = 6.					       
   * The first dimension are the wavelengths of the bands of the satellite.    
   * The values are the remote-sensing reflectances.			       
   * The units are sr^-1.                                                      
   */
  float array1d_iband_Rrs[NBANDS]
  = {0.008642, 0.008084, 0.006332, 0.004698, 0.003626, 0.002036};
  /*
   * Array of dimensions 9 * 61.
   * The first dimension is the hours from 0 to 24 by step of 3 h.
   * The second dimension is the wavelenght from 400 nm to 700 nm by step of 5
   * nm.
   * The values are the downward irradiances just below the surface water     
   * (Ed0minus) for one pixel.						   
   * The units are umol photons*m^-2*s^-1*nm^-1.                              
   */
  float array2d_itime_ivis_Ed0minus[NTIMES][NVIS]
  = {
    {1.759203716,1.725188282,1.685903252,2.044845854,1.685061817,1.962247802,1.344674087,2.019756521,2.215382246,2.467011613,2.643739011,2.671308186,2.702406782,2.748445381,2.852862125,3.000272902,2.967503347,2.955102347,3.122189635,3.148630843,2.906831189,3.024799846,3.045508205,2.949611165,2.969618299,3.118385141,3.049601511,3.110845621,3.154810038,3.234265488,3.174966213,3.302136091,3.094711754,3.274718617,3.120023212,3.151901953,3.294664562,3.349053055,2.862327837,3.057414035,3.278147017,3.427146986,3.308324376,3.339655836,3.394040234,3.230107814,3.197759141,3.353710003,3.341428349,3.415130149,3.136836921,3.24782228,3.432887908,3.490297164,3.53879719,3.506574595,3.513373321,3.531725667,3.030819883,3.060720262,3.135589093},
    {0.696570167,0.682739698,0.666915551,0.808487573,0.66609804,0.77548348,0.53115729,0.797407231,0.874184325,0.972697861,1.042612426,1.05344867,1.06420021,1.082005404,1.122154351,1.172289446,1.157891797,1.157496812,1.224426411,1.233325002,1.133932214,1.174860964,1.183072209,1.145212405,1.149490508,1.201945977,1.16940023,1.190053444,1.206031623,1.234119914,1.208179135,1.251338806,1.166849533,1.225166357,1.145262362,1.149402495,1.212087685,1.24978214,1.033574645,1.112053786,1.217725315,1.281205205,1.241235254,1.257177497,1.279437052,1.215269436,1.190019869,1.266302835,1.280499806,1.31321872,1.203613547,1.243449056,1.335514814,1.368367415,1.39518875,1.387615055,1.392492542,1.400957349,1.138664907,1.164111882,1.201399011},
    {0.07512039,0.073520563,0.071706056,0.086699097,0.071389291,0.082943877,0.05658151,0.084524828,0.092201129,0.102081499,0.1090699,0.109619909,0.109142919,0.110456048,0.114380385,0.117086153,0.112762911,0.111147331,0.117721233,0.116732388,0.102905256,0.102091599,0.10219102,0.09778043,0.095000162,0.095632421,0.088900227,0.087561504,0.086684912,0.086350592,0.081729637,0.081146584,0.072270784,0.072398641,0.065714618,0.063257637,0.066646627,0.070860746,0.060785447,0.06467445,0.066117188,0.067626913,0.067034647,0.070019465,0.072996915,0.070373963,0.070414615,0.077836878,0.08326745,0.089839617,0.085349086,0.09043083,0.099278777,0.103402306,0.108550193,0.110917133,0.113521205,0.116351095,0.09185957,0.100297309,0.104810026},
    {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
    {0.152120061,0.14885851,0.145165306,0.175578054,0.144479818,0.16787223,0.114627512,0.171476158,0.187311715,0.207644632,0.222021026,0.22353045,0.223910281,0.226886845,0.234763997,0.241841811,0.235717218,0.234427866,0.24801366,0.24763955,0.222719033,0.225571013,0.226329954,0.217676135,0.214777312,0.220058361,0.208982292,0.209164417,0.209573785,0.211528702,0.203533968,0.206267431,0.187776392,0.191963251,0.175339043,0.171318833,0.181142749,0.191677195,0.158793157,0.170428473,0.183004382,0.190450967,0.186659513,0.191800737,0.197097049,0.187678911,0.183704887,0.200908658,0.21015025,0.221064199,0.205425234,0.214047373,0.234001318,0.242090479,0.250678525,0.252529952,0.255380396,0.25880953,0.1972514,0.211491069,0.220430429},
    {0.893339542,0.876045006,0.856150849,1.03842996,0.855896765,0.99688584,0.683156766,1.026140593,1.125531977,1.253110164,1.343591927,1.358083754,1.373078691,1.396661618,1.449281961,1.51744578,1.500147168,1.498716028,1.585302183,1.597991882,1.471746625,1.527590576,1.538694069,1.490193078,1.49775482,1.56878316,1.529369595,1.558149115,1.580014685,1.618332826,1.586269897,1.645631522,1.53744582,1.618630152,1.52123372,1.53058628,1.61065571,1.653792371,1.379154605,1.481333541,1.614358545,1.696441388,1.641865962,1.661337486,1.690131635,1.60644151,1.577780056,1.671917161,1.683289172,1.724061952,1.580806913,1.633964178,1.74743701,1.786809505,1.818882792,1.807069142,1.81267805,1.823246093,1.504914039,1.532412026,1.578235493},
    {1.948078665,1.909984108,1.866060501,2.262870353,1.864286541,2.170449271,1.487044894,2.23315901,2.448984224,2.726726882,2.921321391,2.951119812,2.985167083,3.035470952,3.150457737,3.314714799,3.278104199,3.262383911,3.445842251,3.4747049,3.208295096,3.339019062,3.361261055,3.255004073,3.277307045,3.44210824,3.367026757,3.434699662,3.482817882,3.570478871,3.505221857,3.646376108,3.418281973,3.619072774,3.454585159,3.491062619,3.645368136,3.700644618,3.174482248,3.387896073,3.623031962,3.784434091,3.651693472,3.685075944,3.744509872,3.564108697,3.532376325,3.699384675,3.680697823,3.761135809,3.455665279,3.578872767,3.776365924,3.836286801,3.887459244,3.850674055,3.857453907,3.877276215,3.345568659,3.375026942,3.454999612},
    {2.365827284,2.318212182,2.263561878,2.743365842,2.258838361,2.628293703,1.799798694,2.70148016,2.961154953,3.295642571,3.528801773,3.562915205,3.602912336,3.662041147,3.799658394,4.000597445,3.955069947,3.931270017,4.149827423,4.18348831,3.863217052,4.021376439,4.04656118,3.917423873,3.944453176,4.143772446,4.05488601,4.1361585,4.192841947,4.297975318,4.219509368,4.390805184,4.11814971,4.363837877,4.179892353,4.226149014,4.404260463,4.460283259,3.852762912,4.105024295,4.368061499,4.554633723,4.392119335,4.429574342,4.499399523,4.283467995,4.254237599,4.443748016,4.410121139,4.505108132,4.141550083,4.291343858,4.513655791,4.578217603,4.634603007,4.587617525,4.594256432,4.617034367,4.024567146,4.05233581,4.14206576},
    {1.764808139,1.730674175,1.691253899,2.051324827,1.690388251,1.968436035,1.348909011,2.02610492,2.22233564,2.474740123,2.652003375,2.679641511,2.7108318,2.756997678,2.861732971,3.009646276,2.976762307,2.964267308,3.131847087,3.158357949,2.915830699,3.034177593,3.054937457,2.958734757,2.978809547,3.1280565,3.059086412,3.120521486,3.164611708,3.244317249,3.184837161,3.312426924,3.104381411,3.285009115,3.130014912,3.162030063,3.305145928,3.359566912,2.871645014,3.067280655,3.28846261,3.437832978,3.318603511,3.349995246,3.404533383,3.240107621,3.2077685,3.36406397,3.35159039,3.425495466,3.146388181,3.257734649,3.443181156,3.500671811,3.549253498,3.516896701,3.523696554,3.542090033,3.040239387,3.070133979,3.145155528}
    
  };
  /*
   * Array of dimension NBDEPTHS = 101.				  
   * The first dimension is the index of the geometric depths.	  
   * The geometric depths are from 0 to 100 by step 1. Units: m.  
   * The values are the chlorophyll-a concentration.		  
   * The units are mg Chl-a m^-3.                                 
   */
  float array1d_idepth_chl[NBDEPTHS]
  = {0.282579,0.285409,0.288703,0.292495,0.296817,0.301702,0.307180,0.313277,0.320018,0.327422,0.335505,0.344276,0.353738,0.363886,0.374709,0.386185,0.398286,0.410972,0.424194,0.437894,0.452004,0.466445,0.481129,0.495963,0.510840,0.525652,0.540281,0.554607,0.568507,0.581854,0.594524,0.606395,0.617348,0.627270,0.636055,0.643606,0.649838,0.654677,0.658062,0.659947,0.660302,0.659110,0.656372,0.652104,0.646339,0.639124,0.630520,0.620601,0.609454,0.597176,0.583874,0.569660,0.554655,0.538980,0.522760,0.506121,0.489187,0.472077,0.454907,0.437789,0.420825,0.404111,0.387733,0.371768,0.356286,0.341342,0.326987,0.313258,0.300184,0.287786,0.276074,0.265053,0.254720,0.245065,0.236073,0.227722,0.219990,0.212849,0.206268,0.200216,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000};
  /*
   * The value of the option chl to use the chlorophyll-a concentration. 
   * 0 for the chlorophyll-a concentration vertical profile in the water 
   * column.								 
   * 1 for the surface chlorophyll-a concentration.                      
   */
  int chl;
  
  ///////// Assing values to inputs /////////
  lat = 68.76786;
  lon = -104.884529;
  year = 2009;
  month = 8;
  day = 21;
  doy = 233;
  depth = 79.900002;
  rrs_type = MODISA;
  
  /////////// Future output. ///////////
  /*
   * Array of dimension NBDEPTHS - 1 = 100.
   * The first dimension is the index of the geometric depths.
   * The geometric depths are from 0 to 100 by step 1. Units: m.
   * The values are the primary productivities.
   * Units: mgC.m^-2.d^-1.
   */
  float array1d_idepth_pp[NBDEPTHS - 1];
  
//  // Compute primary productivity with chl = surface //
//
//  chl = CHL_SURFACE;
//  get_array1d_idepth_pp(array2d_itime_ivis_Ed0minus,
//                        lat,
//                        lon,
//                        year,
//                        month,
//                        day,
//                        doy,
//                        depth,
//                        rrs_type,
//                        array1d_iband_Rrs,
//                        array1d_idepth_chl,
//                        array1d_idepth_pp,
// 			chl);
//  // Regression test.
//  test_get_array1d_idepth_pp(array1d_idepth_pp,
//			     chl);
// 
  // Compute primary productivity with chl = column //

  chl = CHL_COLUMN;
  get_array1d_idepth_pp(array2d_itime_ivis_Ed0minus,
                        lat,
                        lon,
                        year,
                        month,
                        day,
                        doy,
                        depth,
                        rrs_type,
                        array1d_iband_Rrs,
                        array1d_idepth_chl,
                        array1d_idepth_pp);
  
  // Regression test.
  test_get_array1d_idepth_pp(array1d_idepth_pp,
			     chl);
 
//  /////////////////////////////////////////////////////////////////////////////
//  /////////// test of get_array1d_idepth_pp_from_atm with pixel     ///////////
//  /////////// at row 2 of the prototype for Mathieu in              ///////////
//  /////////// /Volumes/Disk6TB/Takuvik/Teledetection/Couleur/Other/ ///////////
//  /////////// Mathieu/Malina/Fig8/IN/IN20140815/                    ///////////
//  /////////// PPARR5_Mathieu_BG_RRS_Profile_1_1000.txt              ///////////
//  /////////// and the atmospheric products at corresponding pixel   ///////////
//  /////////// 2672663 (0-based) of AM2006225_PP.nc                  ///////////
//  /////////// (version 34.0.0).                                     ///////////
//  /////////////////////////////////////////////////////////////////////////////
//
//  /////////// Declaration of inputs ///////////
//  /*
//   * Array of dimensions NTIMES.					      
//   * The first dimension is the hours from 0 to 24 by step of 3 h.	      
//   * The values are the cloud fraction from 0 to 1.			      
//   * Units: unitless.                                                       
//   */
//  float array1d_itime_cf[NTIMES]
//    = {0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822, 0.5822};
//  /*
//   * Array of dimensions NTIMES.				       
//   * The first dimension is the hours from 0 to 24 by step of 3 h.   	      
//   * The values are the total ozone column at 00h UTC.	       	     
//   * Units: Dobson units.                                            
//   */
//  float array1d_itime_o3[NTIMES]
//    = {276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8, 276.8};
//  /*
//   * Array of dimensions NTIMES.					   
//   * The first dimension is the hours from 0 to 24 by step of 3 h.	      
//   * The values are the cloud optical thickness at 00h UTC.   	   	 
//   * The values are unitless.                                            
//   */
//  float array1d_itime_taucld[NTIMES]
//    = {5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52};
//  
//  /*
//   * Array of 4 dimensions : 						      	
//   * NTAUCLD=8 * NO3=8 * NTHETAS=19 * NBWL=83.				      
//   * The first dimension is the mean cloud optical thickness.		      	
//   * The second dimension is the total ozone column.			      	
//   * The third dimension is the solar zenith angle.			      	
//   * The fourth dimension is the wavelengths from 290 to 700 by step 5 nm.    
//   * The values are the downward irradiance just below the water surface      
//   * from the lookup table.						      	
//   * The units are umol photons*m^-2*s^-1*nm^-1.                              
//   */
//  float array4d_itaucld_io3_ithetas_iwl_ed0minus[NTAUCLD][NO3][NTHETAS][NBWL];
//  
//  /////////// Future output. ///////////
//  /*
//   * Array of dimension NBDEPTHS - 1 = 100.
//   * The first dimension is the index of the geometric depths.
//   * The geometric depths are from 0 to 100 by step 1. Units: m.
//   * The values are the primary productivities.
//   * Units: mgC.m^-2.d^-1.
//   */
//  float array1d_idepth_pp_from_atm[NBDEPTHS - 1];
//  
//  /////////// Compute irradiance ///////////
//
//  get_array4d_itaucld_io3_ithetas_iwl_ed0minus(LUT,
//					       array4d_itaucld_io3_ithetas_iwl_ed0minus);
//  
//  // Compute primary productivity with chl = surface //
//
//  chl = CHL_SURFACE;
//  get_array1d_idepth_pp_from_atm(lat,
//				 lon,
//				 year,
//				 month,
//				 day,
//				 doy,
//				 depth,
//				 rrs_type,
//				 array1d_iband_Rrs,
//				 array1d_idepth_chl,
//				 array1d_itime_cf,
//				 array1d_itime_o3,
//				 array1d_itime_taucld,
//				 array4d_itaucld_io3_ithetas_iwl_ed0minus,
//				 array1d_idepth_pp_from_atm,
//				 chl);
//  
//  // Regression test.
//  test_get_array1d_idepth_pp_from_atm(array1d_idepth_pp_from_atm,
// 				      chl);
//  
//  // Compute primary productivity with chl = column //
//
//  chl = CHL_COLUMN;
//  get_array1d_idepth_pp_from_atm(lat,
//				 lon,
//				 year,
//				 month,
//				 day,
//				 doy,
//				 depth,
//				 rrs_type,
//				 array1d_iband_Rrs,
//				 array1d_idepth_chl,
//				 array1d_itime_cf,
//				 array1d_itime_o3,
//				 array1d_itime_taucld,
//				 array4d_itaucld_io3_ithetas_iwl_ed0minus,
//				 array1d_idepth_pp_from_atm,
//				 chl);
//  
//  // Regression test.
//  test_get_array1d_idepth_pp_from_atm(array1d_idepth_pp_from_atm,
// 				      chl);
  
  exit(0);

}
