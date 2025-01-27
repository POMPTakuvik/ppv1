//  Depth.cpp
//  
//  Created by Maxime Benoit-Gagne on 2016-12-15.
//  Takuvik - Canada.
//  
//  See header file for comments.

#include <cstring>
#include <iomanip>
#include <iostream>
#include <math.h>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>

#include "Depth.h"

#ifdef __cplusplus
#   define API extern "C"
#else
#   define API
#endif

/*
 * See the ISO C standard at
 * http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf at page 26.
 * 1E-5.
 */
#define MY_FLT_EPSILON 0.00001

/* ==================== Prototypes ==================== */
int compare_arrays_i(const int* array1d_i_val1,
                     const int* array1d_i_val2,
                     int n);

/* ========= Global variables (only arrays of constants) ========= */

/*
 * Array of dimension NBDEPTHS_OPT = 12.
 * The first dimension is the index of the optical depth.
 * The values are the optical depth: 100%, 90%, 80%, 70%, 60%, 50%, 40%, 30%, 
 * 20%, 10%, 1%, 0.1%.
 * Unitless.
 */
float ARRAY1D_IDEPTHOPT_DEPTHOPT[NBDEPTHS_OPT] = {1., 0.9, 0.8, 0.7, 0.6, 0.5,
  0.4, 0.3, 0.2, 0.1, 0.01, 0.001};

/* ============================= functions ============================= */

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
                     int n){
  int ret = 0;
  int i;
  for(i = 0; i < n && !ret; i++){
    if(array1d_i_val1[i] - array1d_i_val2[i] != 0){
      ret = 1;
    }
  }
  return ret;
}
/* ------------------------------------------------------------------------- */

/* == Definition of class Depth == */

/* ============================= Constructor ============================= */

Depth::Depth(float array2d_idepthphy_itime_PAR[NBDEPTHS][NTIMES],
             int idepthphy_max,
             float depthphy_step){
  ////////////////// Declare variables //////////////////
  /*
   * Array of dimensions NBDEPTHS_OPT = 12.
   * The first dimension is the number of optical depths.
   * The optical depths are 100%, 90%, 80%, 70%, 60%, 50%, 40%, 30%, 20%, 10%,
   * 1%, 0.1%. Unitless.
   * The values are the physical depth associated with each optical depth
   * at each time.
   * The units are m.
   */
  float array1d_idepthopt_depthphy[NBDEPTHS_OPT];
  /*
   * Array of dimension NBDEPTHS = 101.
   * The first dimension is the geometrical depths. Units: m.
   * The values are the photosynthetically active radiation (PAR) integrated
   * over the wavelenghts at local noon.
   * The units are umol photons.m^-2.s^-1.
   */
  float array1d_idepthphy_PAR[NBDEPTHS];
  int idepthopt;
  int idepthphy;
  int itime;
  
  ////////////////// Initialize attribute //////////////////
  this->depthphy_step = depthphy_step;
  
  //////////// Initialize with foo values ////////////
  for(idepthopt = 0; idepthopt < NBDEPTHS_OPT; idepthopt++){
    array1d_idepthopt_depthphy[idepthopt] = -999.;
    for(itime = 0; itime < NTIMES; itime++){
      array2d_idepthopt_itime_depthphy[idepthopt][itime] = -999.;
    }
  }
  for(idepthphy = 0; idepthphy < NBDEPTHS; idepthphy++){
    array1d_idepthphy_PAR[idepthphy] = -999.;
  }
  
  //////// Compute the physical depth at each optical depth ////////
  for(itime = 0; itime < NTIMES; itime++){
    get_array1d_idepthphy_PAR(array2d_idepthphy_itime_PAR,
                              itime,
                              array1d_idepthphy_PAR);
    get_array1d_idepthopt_depthphy(array1d_idepthphy_PAR,
                                   idepthphy_max,
                                   array1d_idepthopt_depthphy);
    fill_array2d_idepthopt_itime_depthphy(array1d_idepthopt_depthphy,
                                          itime);
  }
}
/* ------------------------------------------------------------------------- */

/* ======================== private methods ======================== */

void Depth::get_array1d_idepthopt_depthphy(float array1d_idepthphy_PAR
                                           [NBDEPTHS],
                                           int idepthphy_max,
                                           float array1d_idepthopt_depthphy
                                           [NBDEPTHS_OPT]){
  float depthopt;
  float depthphy;
  int idepthopt;
  array1d_idepthopt_depthphy[0] = 0;
  for(idepthopt = 1; idepthopt < NBDEPTHS_OPT; idepthopt++){
    depthopt = ARRAY1D_IDEPTHOPT_DEPTHOPT[idepthopt];
    depthphy = get_depthphy(array1d_idepthphy_PAR,
                            idepthphy_max,
                            depthopt);
    array1d_idepthopt_depthphy[idepthopt] = depthphy;
  }
}
/* ------------------------------------------------------------------------- */

int Depth::get_array1d_itime_idepthphy_max(int array1d_itime_idepthphy_max
                                           [NTIMES]){
  
  float depthphy = -999;
  int idepthopt;
  int idepthopt_max = 11; // Zeu 0.1%
  int idepthphy_max = -999;
  int itime;
  int ret = 0;
  for(itime = 0; itime < NTIMES; itime++){
    idepthphy_max = -999;
    depthphy = -999.;
    for(idepthopt = idepthopt_max; idepthopt >= 0 && depthphy < 0; idepthopt--){
      depthphy = array2d_idepthopt_itime_depthphy[idepthopt][itime];
      if(depthphy >= 0){
        idepthphy_max = ceil(depthphy / depthphy_step) + MY_FLT_EPSILON + 1;
        array1d_itime_idepthphy_max[itime] = idepthphy_max;
      }
    }
  }
  return ret;
}
/* ------------------------------------------------------------------------- */

void Depth::get_array1d_idepthphy_PAR(float array2d_idepthphy_itime_PAR
                                      [NBDEPTHS][NTIMES],
                                      int itime,
                                      float array1d_idepthphy_PAR[NBDEPTHS]){
  int idepthphy;
  float PAR;
  for(idepthphy = 0; idepthphy < NBDEPTHS; idepthphy++){
    PAR = array2d_idepthphy_itime_PAR[idepthphy][itime];
    array1d_idepthphy_PAR[idepthphy] = PAR;
  }
}
/* ------------------------------------------------------------------------- */

void Depth::fill_array2d_idepthopt_itime_depthphy(float array1d_idepthopt_depthphy[NBDEPTHS_OPT],
                                                  int itime){
  int idepthopt;
  float depthphy;
  for(idepthopt = 0; idepthopt < NBDEPTHS_OPT; idepthopt++){
    depthphy = array1d_idepthopt_depthphy[idepthopt];
    array2d_idepthopt_itime_depthphy[idepthopt][itime] = depthphy;
  }
}
/* ------------------------------------------------------------------------- */

float Depth::get_depthphy(float array1d_idepthphy_PAR[NBDEPTHS],
                          int idepthphy_max,
                          float depthopt){
  float depthphy = -999.;
  int idepthphy = -999;
  int idepthphy_tmp = -999;
  int found = 0;
  int negative_PAR_found = 0;
  float PAR;
  float PAR_0minus;
  if(idepthphy_max > 0){
    PAR_0minus = array1d_idepthphy_PAR[0];
    for(idepthphy_tmp = 0;
        (idepthphy_tmp < idepthphy_max) && (!found) && (!negative_PAR_found);
        idepthphy_tmp++){
      PAR = array1d_idepthphy_PAR[idepthphy_tmp];
      if(PAR < 0){
        negative_PAR_found = 1;
      }
      if(PAR < (PAR_0minus * depthopt)){
        idepthphy = idepthphy_tmp;
        found = 1;
      }
    }
  }
  if(negative_PAR_found){                       // PAR < 0
    depthphy = -999.;
  }else if(idepthphy_tmp == NBDEPTHS){          // max depth
    depthphy = (NBDEPTHS - 1) * depthphy_step;
  }else if(idepthphy_tmp - 1 == idepthphy_max){ // bottom of the water column
    depthphy = -999.;
  }else{                                        // normal case
    depthphy = idepthphy * depthphy_step;
  }
  return depthphy;
}
/* ------------------------------------------------------------------------- */

/* ======================== public methods ======================== */
int Depth::to_string(char* s_arg, int buffersize){
  float depthopt;
  float depthphy;
  int idepthopt;
  int itime;
  ostringstream oss;
  int time;
  int time_step = 3;
  oss << "Depth" << endl;
  oss << "Step for physical depths (m): " << depthphy_step << endl;
  oss << "Physical depths of the optical depths" << endl;
  oss << "Optical depth" << endl;
  oss << "(unitless)   ";
  for(itime = 0; itime < NTIMES; itime++){
    time = time_step * itime;
    oss << setw(8) << time << " UTC";
  }
  oss << endl;
  for(idepthopt = 0; idepthopt < NBDEPTHS_OPT; idepthopt++){
    depthopt = ARRAY1D_IDEPTHOPT_DEPTHOPT[idepthopt];
    oss << fixed << setprecision(1) << setw(12) << depthopt * 100 << "%";
    for(itime = 0; itime < NTIMES; itime++){
      depthphy = array2d_idepthopt_itime_depthphy[idepthopt][itime];
      oss << " " << fixed << setprecision(6) << setw(11) << depthphy;
    }
    oss << endl;
  }
  string s = oss.str();
  strncpy(s_arg, s.c_str(), buffersize);
  s_arg[buffersize - 1] = '\0';
  return 0;
}
/* ------------------------------------------------------------------------- */

Depth::~Depth(){}
/* ------------------------------------------------------------------------- */

// External C API to Depth class

API void* Depth_create(float array2d_idepthphy_itime_PAR[NBDEPTHS][NTIMES],
		       int idepthphy_max,
		       float depthphy_step){
  return (void*) new Depth(array2d_idepthphy_itime_PAR,
			   idepthphy_max,
			   depthphy_step);
};
API int Depth_get_array1d_itime_idepthphy_max(void* depth,
					      int array1d_itime_idepthphy_max
					      [NTIMES]){
  return ( (Depth*) depth)
    -> get_array1d_itime_idepthphy_max(array1d_itime_idepthphy_max);
};
API int Depth_to_string(void* depth,
			char* s_arg,
			int buffersize){
  return ( (Depth*) depth) -> to_string(s_arg,
					buffersize);
};
API void Depth_delete(void* depth){
  delete (Depth*) depth;
};

/* ================================= MAIN ================================= */

// Uncomment to test.

//int main(int argc, char *argv[]){
//  
//  char errmsg[] = "Bad number of arguments.\n"
//  "Usage:\n"
//  "./HelloWorld\n";
//  
//  /////////// Declaration of the variables. ///////////
//  
//  /////////// Verification of the arguments. ///////////
//  if(argc != 1){
//    printf("%s", errmsg);
//    return -1;
//  }
//  
//  /////////// Test of Depth ///////////
//  cout << "Test of class Depth" << endl;
//  cout << "Test 1) deep water" << endl;
//  
//  float array2d_idepthphy_itime_PAR[NBDEPTHS][NTIMES] = {
//    {100., 100., 100., 100., 100., 100., 100., 100., 100.}, // idepthphy = 0
//    {95, 95., 95., 95., 95., 95., 95., 95., 95.},           // idepthphy = 1
//    {85., 85., 85., 85., 85., 85., 85., 85., 85.},          // idepthphy = 2
//    {75., 75., 75., 75., 75., 75., 75., 75., 75.},          // idepthphy = 3
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},
//    {75., -999., 75., 75., 75., 75., 75., 75., 75.},  // idepthphy = 97
//    {0.15, -999., 15., 15., 15., 15., 15., 15., 15.}, // idepthphy = 98
//    {0.05, -999., 15., 15., 15., 15., 15., 15., 15.}, // idepthphy = 99
//    {0.01, -999., 5., 5., 5., 5., 5., 5., 5.}         // idepthphy = 100
//  };
//  int idepthphy_max = 101;
//  float depthphy_step = 1.;
//  
//  Depth depthInfo = Depth(array2d_idepthphy_itime_PAR,
//                          idepthphy_max,
//                          depthphy_step);
//  
//  int s_size = 100000;
//  char depthInfo_s[s_size];
//  depthInfo.to_string(depthInfo_s, s_size);
//  printf("%s\n", depthInfo_s);
//  
//  /*
//   *  Array of dimension NTIMES = 9.
//   *  The first dimension is the hours UTC from 0 to 24 by step of 3 h.
//   *  Units: hour.
//   *  The values are the indices of the physical depth for which the primary
//   *  productivity will be computed.
//   *  Units: unitless because it is indices.
//   */
//  int array1d_itime_idepthphy_max[NTIMES]
//  = {-1, -1, -1, -1, -1, -1, -1, -1, -1};
//  
//  int array1d_itime_idepthphy_max_ref[NTIMES]
//  = {100, 4, 101, 101, 101, 101, 101, 101, 101};
//  depthInfo.get_array1d_itime_idepthphy_max(array1d_itime_idepthphy_max);
//  if(!compare_arrays_i(array1d_itime_idepthphy_max,
//                       array1d_itime_idepthphy_max_ref,
//                       NTIMES)){
//    cout << "PASS" << endl << endl;
//  }else{
//    cout << "FAIL" << endl << endl;
//  }
//  
//  cout << "Test 2) shallow water" << endl;
//  idepthphy_max = 3;
//  
//  depthInfo = Depth(array2d_idepthphy_itime_PAR,
//                    idepthphy_max,
//                    depthphy_step);
//  
//  depthInfo.to_string(depthInfo_s, s_size);
//  printf("%s\n", depthInfo_s);
//  
//  /*
//   *  Array of dimension NTIMES = 9.
//   *  The first dimension is the hours UTC from 0 to 24 by step of 3 h.
//   *  Units: hour.
//   *  The values are the indices of the physical depth for which the primary
//   *  productivity will be computed.
//   *  Units: unitless because it is indices.
//   */
//  int array1d_itime_idepthphy_max2[NTIMES]
//  = {-1, -1, -1, -1, -1, -1, -1, -1, -1};
//  
//  int array1d_itime_idepthphy_max_ref2[NTIMES]
//  = {3, 3, 3, 3, 3, 3, 3, 3, 3};
//  depthInfo.get_array1d_itime_idepthphy_max(array1d_itime_idepthphy_max2);
//  
//  if(!compare_arrays_i(array1d_itime_idepthphy_max2,
//                       array1d_itime_idepthphy_max_ref2,
//                       NTIMES)){
//    cout << "PASS" << endl << endl;
//  }else{
//    cout << "FAIL" << endl << endl;
//  }
//  
//  
//  /////////// Return. ///////////
//  return 0;
//}


