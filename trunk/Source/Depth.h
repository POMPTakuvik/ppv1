// 
//  Depth.h
//  
//  Created by Maxime Benoit-Gagne on 2016-12-15.
//  Takuvik - Canada.
//  
//  compiler:
//  $ g++ -v
//  Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1
//  Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)
//  Target: x86_64-apple-darwin12.6.0
//  Thread model: posix
//  
//  usage:
//  ./depth
//  
//  description:
//   Class containing the physical depths associated with each optical depth.
//  
//  uses: 
//  
//  keywords: C++

#ifndef __Depth__
#define __Depth__

#include "Color.h"
#include "Depth_params.h"

using namespace std;

// Depth class definition

class Depth{
  ////////////////////////// private //////////////////////////
private:
  /*
   * Array of dimensions NBDEPTHS_OPT * NTIMES = 12 * 9.
   * The first dimension is the number of optical depths.
   * The optical depths are 100%, 90%, 80%, 70%, 60%, 50%, 40%, 30%, 20%, 10%,
   * 1%, 0.1%. Unitless.
   * The second dimension is the hours UTC from 0 to 24 by step of 3 h.
   * Units: hour.
   * The values are the physical depth associated with each optical depth
   * at each time.
   * The units are m.
   */
  float array2d_idepthopt_itime_depthphy[NBDEPTHS_OPT][NTIMES];
  /*
   * The step between two physical depths.
   * Units: m.
   */
  float depthphy_step;
  
  /*
   * IN
   * array1d_idepthphy_PAR:
   *  Array of dimension NBDEPTHS = 101.
   *  The first dimension is the geometrical depths. Units: m.
   *  The values are the photosynthetically active radiation (PAR) integrated
   *  over the wavelenghts at local noon.
   *  The units are umol photons.m^-2.s^-1.
   * @param idepthphy_max:
   *  Index of the physical depth to which parameters are computed (exclusive).
   * OUT
   * array1d_idepthopt_depthphy:
   *  Array of dimensions NBDEPTHS_OPT = 12.
   *  The first dimension is the number of optical depths.
   *  The optical depths are 100%, 90%, 80%, 70%, 60%, 50%, 40%, 30%, 20%, 10%,
   *  1%, 0.1%. Unitless.
   *  The values are the physical depth associated with each optical depth
   *  at each time.
   *  The units are m.
   */
  void get_array1d_idepthopt_depthphy(float array1d_idepthphy_PAR[NBDEPTHS],
                                      int idepthphy_max,
                                      float array1d_idepthopt_depthphy
                                      [NBDEPTHS_OPT]);
  /*
   * IN
   * @param array2d_idepthphy_itime_PAR:
   *  Array of dimensions NBDEPTHS * NTIMES = 101 * 9.
   *  The first dimension are the geometrical depths. Units: m.
   *  The second dimension is the hours UTC from 0 to 24 by step of 3 h.
   *  Units: hour.
   *  The values are the photosynthetically active radiation (PAR) integrated
   *  over the wavelenghts at local noon.
   *  The units are umol photons.m^-2.s^-1.
   * itime:
   *  Index of the time UTC from 0 to 24 by step 3.
   * OUT
   * array1d_idepthphy_PAR:
   *  Array of dimension NBDEPTHS = 101.
   *  The first dimension is the geometrical depths. Units: m.
   *  The values are the photosynthetically active radiation (PAR) integrated
   *  over the wavelenghts at local noon.
   *  The units are umol photons.m^-2.s^-1.
   */
  void get_array1d_idepthphy_PAR(float array2d_idepthphy_itime_PAR
                                 [NBDEPTHS][NTIMES],
                                 int itime,
                                 float array1d_idepthphy_PAR[NBDEPTHS]);
  /*
   * IN
   * array1d_idepthphy_PAR:
   *  Array of dimension NBDEPTHS = 101.
   *  The first dimension is the geometrical depths. Units: m.
   *  The values are the photosynthetically active radiation (PAR) integrated
   *  over the wavelenghts at local noon.
   *  The units are umol photons.m^-2.s^-1.
   * @param idepthphy_max:
   *  Index of the physical depth to which parameters are computed (exclusive).
   * depthopt:
   *  An optical depth.
   *  Unitless.
   * Return the physical depth associated with the optical depth depthopt.
   * Units: m.
   */
  float get_depthphy(float array1d_idepthphy_PAR[NBDEPTHS],
                     int idepthphy_max,
                     float depthopt);
  
  /*
   * IN
   * array1d_idepthopt_depthphy:
   *  Array of dimensions NBDEPTHS_OPT = 12.
   *  The first dimension is the number of optical depths.
   *  The optical depths are 100%, 90%, 80%, 70%, 60%, 50%, 40%, 30%, 20%, 10%,
   *  1%, 0.1%. Unitless.
   *  The values are the physical depth associated with each optical depth
   *  at each time.
   *  The units are m.
   * itime:
   *  Index of the time UTC from 0 to 24 by step 3.
   * Fill the attribute array2d_idepthopt_itime_depthphy.
   */
  void fill_array2d_idepthopt_itime_depthphy(float array1d_idepthopt_depthphy[NBDEPTHS_OPT],
                                                    int itime);
  
  ////////////////////////// public //////////////////////////
public:
  /**
   * Constructor.
   *
   * IN
   * @param array2d_idepthphy_itime_PAR:
   *  Array of dimensions NBDEPTHS * NTIMES = 101 * 9.
   *  The first dimension are the geometrical depths. Units: m.
   *  The second dimension is the hours UTC from 0 to 24 by step of 3 h.
   *  Units: hour.
   *  The values are the photosynthetically active radiation (PAR) integrated
   *  over the wavelenghts at local noon.
   *  The units are umol photons.m^-2.s^-1.
   * @param idepthphy_max:
   *  Index of the physical depth to which parameters are computed (exclusive).
   * @param depthphy_step:
   *  The step between two physical depths.
   *  Units: m.
   * OUT
   * return a Depth.
   */
  Depth(float array2d_idepthphy_itime_PAR[NBDEPTHS][NTIMES],
        int idepthphy_max,
        float depthphy_step);
  
  /*
   * Destructor.
   */
  ~Depth();
  
  /**
   * OUT
   * @param array1d_itime_idepthphy_max:
   *  Array of dimension NTIMES = 9.
   *  The first dimension is the hours UTC from 0 to 24 by step of 3 h.
   *  Units: hour.
   *  The values are the indices of the physical depth for which the primary
   *  productivity will be computed (exclusive).
   *  Units: unitless because it is indices.
   * @return 0.
   */
  int get_array1d_itime_idepthphy_max(int array1d_itime_idepthphy_max[NTIMES]
                                      );
  
  /**
   * IN
   * buffersize:
   *  Size of s_arg.
   *
   * OUT
   * s_arg:
   *  A string representing Depth.
   *
   * @return 0.
   */
  int to_string(char* s_arg, int buffersize);
};


#endif /* define(__Depth__) */
