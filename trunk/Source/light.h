/* =========================================================================
 light.h
 
 author: Maxime Benoit-Gagne
 - Takuvik - Canada.
 date: December 15, 2015
 
 compiler:
 $ gcc -v
 Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1
 Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)
 Target: x86_64-apple-darwin12.6.0
 Thread model: posix
 
 description:
 light.h is a header for functions about the light.
 
 uses: TODO
 
 keywords: light
 
 ============================================================================ */

#ifndef __light_h
#define __light_h

#include "Color.h"

/*
 * Index of lambda 400 in the wavelengths 290 to 700.
 */
#define I400_FROM_290 22
/*
 * Number of limits of the time intervals:		   
 * 0 to 24h by step of 3h.                                 
 */
//#define NTIMES 9
/*
 * Number of wavelengths from 400 to 700 nm by step of 5 nm.
 */
#define NVIS 61
/*
 * Number of wavelengths from 290 to 700 nm by step of 5 nm.
 */
#define NBWL 83
/*
 * 8 values for total ozone column from 100 to 550, in Dobson units (DU) at
 * every 50 DU.
 */
#define NO3 10
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

#define NALB 7
/*
 * IN
 * lat:
 *  Latitude.			 
 *  The units are degrees North.
 * lon:
 *  Longitude.			
 *  From -180 to 180.		
 *  The units are degrees East.
 * doy:
 *  Day of year.
 * array1d_itime_cf:
 *  Array of dimensions NTIMES.					    	   
 *  The first dimension is the hours from 0 to 24 by step of 3 h.	    
 *  The values are the cloud fraction from 0 to 1.			    
 *  Units: unitless.                                                       
 *  return 0 on success.
 *  return -1 if < 0 and array2d_itime_ivis_ed0minus is filled with -999.
 * array1d_itime_o3:
 *  Array of dimensions NTIMES.				     	    
 *  The first dimension is the hours from 0 to 24 by step of 3 h.   
 *  The values are the total ozone column at 00h UTC.		     
 *  Units: Dobson units.                                            
 *  return 0 on success.
 *  return -1 if < 0 and array2d_itime_ivis_ed0minus is filled with -999.
 * array1d_itime_taucld:
 *  Array of dimensions NTIMES.					 	
 *  The first dimension is the hours from 0 to 24 by step of 3 h.	 
 *  The values are the cloud optical thickness at 00h UTC.   		 
 *  The values are unitless.                                            
 *  return 0 on success.
 *  return -1 if < 0 and array2d_itime_ivis_ed0minus is filled with -999.
 * array4d_itaucl_io3_ithetas_iwl_ed0minus:
 *  Array of 4 dimensions 					      
 *  ntaucl=8 * nozone=8 * nthetas=19 * nwl=83.				      
 *  The first dimension is the mean cloud optical thickness.		      
 *  The second dimension is the total ozone column.			      
 *  The third dimension is the solar zenith angle.			      
 *  The fourth dimension is the wavelengths from 290 to 700 by step 5 nm.    
 *  The values are the downward irradiance just below the water surface      
 *  from the lookup table.						      
 *  The units are umol photons*m^-2*s^-1*nm^-1.                              
 * OUT
 * array2d_itime_ivis_ed0minus:
 *  Array of dimensions 9 * 61.					      
 *  The first dimension is the hours from 0 to 24 by step of 3 h.	      
 *  The second dimension is the wavelenght from 400 nm to 700 nm by step of 5
 *  nm.								      
 *  The values are the downward irradiances just below the surface water     
 *  (Ed0minus) for one pixel.						      
 *  The units are umol photons*m^-2*s^-1*nm^-1.                              
 */
int get_array2d_itime_ivis_ed0minus(float lat,
				    float lon,
				    int doy,
				    float array1d_itime_cf[NTIMES],
				    float array1d_itime_o3[NTIMES],
				    float array1d_itime_taucld[NTIMES],
				    float downward_irradiance_table_as_input[NBWL][NTHETAS][NO3][NTAUCLD][NALB],
				    float array2d_itime_ivis_ed0minus[NTIMES][NVIS]);

/*
 * IN
 * lat:
 *  Latitude.			 
 *  The units are degrees North.
 * lon:
 *  Longitude.			
 *  From -180 to 180.		
 *  The units are degrees East.
 * doy:
 *  Day of year.
 * array1d_itime_cf:
 *  Array of dimensions NTIMES.					    	   
 *  The first dimension is the hours from 0 to 24 by step of 3 h.	    
 *  The values are the cloud fraction from 0 to 1.			    
 *  Units: unitless.                                                       
 *  return 0 on success.
 *  return -1 if < 0 and array2d_itime_ivis_ed0minus is filled with -999.
 * array1d_itime_o3:
 *  Array of dimensions NTIMES.				     	    
 *  The first dimension is the hours from 0 to 24 by step of 3 h.   
 *  The values are the total ozone column at 00h UTC.		     
 *  Units: Dobson units.                                            
 *  return 0 on success.
 *  return -1 if < 0 and array2d_itime_ivis_ed0minus is filled with -999.
 * array1d_itime_taucld:
 *  Array of dimensions NTIMES.					 	
 *  The first dimension is the hours from 0 to 24 by step of 3 h.	 
 *  The values are the cloud optical thickness at 00h UTC.   		 
 *  The values are unitless.                                            
 *  return 0 on success.
 *  return -1 if < 0 and array2d_itime_ivis_ed0minus is filled with -999.
 * ptr_array4d_itaucl_io3_ithetas_iwl_ed0minus:
 *  Pointer to an array of dimension 					      
 *  ntaucl=8 * nozone=8 * nthetas=19 * nwl=83.				      
 *  The first dimension is the mean cloud optical thickness.		      
 *  The second dimension is the total ozone column.			      
 *  The third dimension is the solar zenith angle.			      
 *  The fourth dimension is the wavelengths from 290 to 700 by step 5 nm.    
 *  The values are the downward irradiance just below the water surface      
 *  from the lookup table.						      
 *  The units are umol photons*m^-2*s^-1*nm^-1.                              
 * OUT
 * array2d_itime_ivis_ed0minus:
 *  Array of dimensions 9 * 61.					      
 *  The first dimension is the hours from 0 to 24 by step of 3 h.	      
 *  The second dimension is the wavelenght from 400 nm to 700 nm by step of 5
 *  nm.								      
 *  The values are the downward irradiances just below the surface water     
 *  (Ed0minus) for one pixel.						      
 *  The units are umol photons*m^-2*s^-1*nm^-1.                              
 */
int get_array2d_itime_ivis_ed0minus_in(float lat,
				       float lon,
				       int doy,
				       float array1d_itime_cf[NTIMES],
				       float array1d_itime_o3[NTIMES],
				       float array1d_itime_taucld[NTIMES],
				       float downward_irradiance_table_as_input[NBWL][NTHETAS][NO3][NTAUCLD][NALB],
				       float array2d_itime_ivis_ed0minus[NTIMES][NVIS]);

/*
 * IN
 * filename:
 *  The atmospheric lookup table.				   
 *  Dimensions: Wavelength(83) * Thetas(19) * Ozone(8) * TauCld(8).
 * OUT
 * array4d_itaucld_io3_ithetas_iwl_ed0minus:
 *  Array of 4 dimensions : 						      
 *  NTAUCLD=8 * NO3=8 * NTHETAS=19 * NBWL=83.				      
 *  The first dimension is the mean cloud optical thickness.		      
 *  The second dimension is the total ozone column.			      
 *  The third dimension is the solar zenith angle.			      
 *  The fourth dimension is the wavelengths from 290 to 700 by step 5 nm.    
 *  The values are the downward irradiance just below the water surface      
 *  from the lookup table.						      
 *  The units are umol photons*m^-2*s^-1*nm^-1.                              
 * Return 0 if success.
 * Return -1 if not.
                 
 */
int get_downward_irradiance_table(char* filename,
						 float downward_irradiance_table_as_output[NBWL][NTHETAS][NO3][NTAUCLD][NALB]);

#endif
