/*
 * params.h
 * Author: Maxime Benoit-Gagne
 * Creation: July 7 2013
 *
 * params.h contains parameters that one could want to change to make tests.
 */

#ifndef _PARAMS_H
#define _PARAMS_H

  /*
   * Array of dimension NVIS = 61.					       
   * The second dimension are the wavelengths in the visible spectrum.
   * The wavelengths are from 400 to 700 by step 5. Units: nm.
   * The values are the pure sea water backscattering coefficients (bb_w).
   * The units are m^-1.                                            
   * The source is 
   * Applications/seadas-7.3.2/ocssw/run/data/common/water_spectra.dat
   * for the middle of band.
   */
#define ARRAY1D_IVIS_AW {0.00663,0.0053,0.00473,0.00444,0.00454,0.00478,0.00495,0.0053,0.00635,0.00751,0.00922,0.00962,0.00979,0.01011,0.0106,0.0114,0.0127,0.0136,0.015,0.0173,0.0204,0.0256,0.0325,0.0396,0.0409,0.0417,0.0434,0.0452,0.0474,0.0511,0.0565,0.0596,0.0619,0.0642,0.0695,0.0772,0.0896,0.11,0.1351,0.1672,0.2224,0.2577,0.2644,0.2678,0.2755,0.2834,0.2916,0.3012,0.3108,0.325,0.34,0.371,0.41,0.429,0.439,0.448,0.465,0.486,0.516,0.559,0.624}

  /*
   * Array of dimension NVIS = 61.					       
   * The second dimension are the wavelengths in the visible spectrum.
   * The wavelengths are from 400 to 700 by step 5. Units: nm.
   * The values are the budget of phytoplankton, i.e. the relative 
   * contribution of the absorption coefficient of phytoplankton to the total
   * nonwater absorption coefficient.
   * Unitless.
   * The source is Matsuoka 2011 Table 3 cruise All for lambda = 440 nm.
   * The values for each wavelenght from 400 nm to 700 nm by steps of 5 nm
   * are from Matsuoka directly (unpublished).
   */
#define ARRAY1D_IVIS_BUDGETPHY {0.1223135,0.1357194,0.1504608,0.1640598,0.1773048,0.190433,0.2063735,0.2220729,0.2311892,0.2373872,0.2418397,0.2504904,0.2607066,0.2711439,0.2792328,0.283599,0.2884588,0.2939106,0.2974561,0.2978136,0.2964728,0.2947714,0.2947193,0.2929092,0.2920851,0.2930873,0.2912467,0.2882432,0.2846058,0.2824411,0.2754806,0.2737691,0.2654228,0.2683976,0.272074,0.2826506,0.2909486,0.3073148,0.3155612,0.3236175,0.3370967,0.3423567,0.3605292,0.3835262,0.4044117,0.4192232,0.4415903,0.466764,0.4877605,0.5009921,0.5124237,0.5449741,0.5980247,0.6605056,0.70609,0.7241564,0.7129954,0.6629994,0.5847232,0.4915308,0.4104123}

  /*
   * Array of dimension NVIS = 61.					       
   * The second dimension are the wavelengths in the visible spectrum.
   * The wavelengths are from 400 to 700 by step 5. Units: nm.
   * The values are the pure sea water backscattering coefficients (bb_w).
   * The units are m^-1.                                            
   * The source is 
   * Applications/seadas-7.3.2/ocssw/run/data/common/water_spectra.dat
   * for the middle of band.
   */
#define ARRAY1D_IVIS_BBW {0.00335635,0.00318122,0.003017475,0.002864235,0.00272069,0.0025861,0.0024598,0.00234118,0.00222968,0.002124785,0.00202603,0.001932985,0.00184525,0.00176247,0.00168431,0.001610455,0.001540625,0.00147456,0.00141201,0.00135276,0.0012966,0.001243335,0.00119279,0.001144795,0.001099195,0.001055855,0.001014635,0.000975415,0.00093808,0.000902515,0.000868625,0.000836315,0.000805495,0.000776085,0.00074801,0.000721195,0.00069557,0.00067108,0.00064766,0.00062525,0.000603805,0.00058327,0.000563605,0.000544765,0.0005267,0.000509385,0.000492772,0.0004768325,0.0004615335,0.000446843,0.000432733,0.0004191755,0.000406146,0.0003936185,0.0003815705,0.0003699805,0.000358827,0.000348091,0.0003377535,0.000327797,0.000318205}

  /*
   * Array of dimension NBANDS = 6.					       
   * The first dimension are the wavelengths of the bands of the satellite
   * MODIS-Aqua.
   * The values are the water absorption coefficients (a_w).	       	       
   * The units are m^-1.                                                       
   * The source is 
   * Applications/seadas-7.3.2/ocssw/run/data/common/water_spectra.dat
   * for the middle of band.
   */
#define AW_MODISA {0.00455056, 0.00706914, 0.0145167, 0.0439153, 0.0596000, 0.434888}
  /*
   * Array of dimension NBANDS = 6.					       
   * The first dimension are the wavelengths of the bands of the satellite
   * SeaWiFS.
   * The values are the water absorption coefficients (a_w).	       	       
   * The units are m^-1.     
   * The source is 
   * Applications/seadas-7.3.2/ocssw/run/data/common/water_spectra.dat
   * for the middle of band.
   */
#define AW_SEAWIFS {0.00455056, 0.00706914, 0.0150000, 0.0325000, 0.0596000, 0.439000}

  /*
   * Array of dimension NBANDS = 6.					       
   * The first dimension are the wavelengths of the bands of the satellite
   * MODIS-AQUA.
   * The values are the pure sea water backscattering coefficients (bb_w).
   * The units are m^-1.                                            
   * The source is 
   * Applications/seadas-7.3.2/ocssw/run/data/common/water_spectra.dat
   * for the middle of band.
   */
#define BBW_MODISA {0.002954965, 0.00216598, 0.00143662, 0.001006635, 0.000836315, 0.000388743}

  /*
   * Array of dimension NBANDS = 6.					       
   * The first dimension are the wavelengths of the bands of the satellite
   * SeaWiFS.
   * The values are the pure sea water backscattering coefficients (bb_w).
   * The units are m^-1.                                            
   * The source is 
   */
#define BBW_SEAWIFS {0.002954965, 0.00216598, 0.00141201, 0.00119279, 0.000836315, 0.0003815705}

  /*
   * Array of dimension NBANDS = 6.					       
   * The first dimension are the wavelengths of the bands of the satellite
   * MODIS-Aqua.
   * The values are the budget of phytoplankton, i.e. the relative 
   * contribution of the absorption coefficient of phytoplankton to the total
   * nonwater absorption coefficient.
   * Unitless.
   * The source is Matsuoka 2011 Table 3 cruise All for lambda = 440 nm.
   * The values for each wavelenght from 400 nm to 700 nm by steps of 5 nm
   * are from Matsuoka directly (unpublished).
   * The values were computed for each of the six bands of the sensor by
   * linear interpolation.
   */
#define BUDGET_MODISA {0.15590042, 0.234907986, 0.29603787, 0.290646011, 0.273769093, 0.67873936}

  /*
   * Array of dimension NBANDS = 6.					       
   * The first dimension are the wavelengths of the bands of the satellite
   * SeaWiFS.
   * The values are the budget of phytoplankton, i.e. the relative 
   * contribution of the absorption coefficient of phytoplankton to the total
   * nonwater absorption coefficient.
   * Unitless.
   * The source is Matsuoka 2011 Table 3 cruise All for lambda = 440 nm.
   * The values for each wavelenght from 400 nm to 700 nm by steps of 5 nm
   * are from Matsuoka directly (unpublished).
   * The values were computed for each of the six bands of the sensor by
   * linear interpolation.
   */
#define BUDGET_SEAWIFS {0.15590042, 0.234907986, 0.297456076, 0.294719308, 0.273769093, 0.70608999}

#endif
