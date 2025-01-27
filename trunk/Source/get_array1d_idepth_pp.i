/* File : get_array1d_idepth_pp.i */
%module get_array1d_idepth_pp

%{
#define SWIG_FILE_WITH_INIT
/* Put headers and other declarations here */
  extern void get_array1d_idepth_pp(float array2d_itime_ivis_Ed0minus[9][61],
				    float lat,
				    float lon,
				    int year,
				    int month,
				    int day,
				    int doy,
				    float depth,
				    char rrs_type,
				    float array1d_iband_Rrs[6],
				    float array1d_idepth_chl[101],
				    float array1d_idepth_pp[100]);
extern void get_array1d_idepth_pp_from_atm(float lat,
					   float lon,
					   int year,
					   int month,
					   int day,
					   int doy,
					   float depth,
					   char rrs_type,
					   float array1d_iband_Rrs[6],
					   float array1d_idepth_chl[101],
					   float array1d_itime_cf[9],
					   float array1d_itime_o3[9],
					   float array1d_itime_taucld[9],
					   float downward_irradiance_table[83][19][10][8][7],
					   float array1d_idepth_pp[100]);
%}

%include "numpy.i"

%init %{
  import_array();
%}

#define CHL_COLUMN 1
#define CHL_SURFACE 0
#define NBDEPTHS 101

// Common arguments
%apply (float IN_ARRAY1[ANY]) {(float array1d_iband_Rrs[6])};
%apply (float IN_ARRAY1[ANY]) {(float array1d_idepth_chl[NBDEPTHS])};
%apply (float INPLACE_ARRAY1[ANY]) {(float array1d_idepth_pp[100])};

%apply (float IN_ARRAY2[ANY][ANY]) {(float array2d_itime_ivis_Ed0minus[9][61])};
extern void get_array1d_idepth_pp(float array2d_itime_ivis_Ed0minus[9][61],
				  float lat,
				  float lon,
				  int year,
				  int month,
				  int day,
				  int doy,
				  float depth,
				  char rrs_type,
				  float array1d_iband_Rrs[6],
				  float array1d_idepth_chl[NBDEPTHS],
				  float array1d_idepth_pp[100]);
%clear (float array2d_itime_ivis_Ed0minus[9][61]);

%apply (float IN_ARRAY1[ANY]) {(float array1d_itime_cf[9])};
%apply (float IN_ARRAY1[ANY]) {(float array1d_itime_o3[9])};
%apply (float IN_ARRAY1[ANY]) {(float array1d_itime_taucld[9])};
%apply (float IN_ARRAY5[ANY][ANY][ANY][ANY][ANY]) {(float downward_irradiance_table[83][19][10][8][7])};
extern void get_array1d_idepth_pp_from_atm(float lat,
					   float lon,
					   int year,
					   int month,
					   int day,
					   int doy,
					   float depth,
					   char rrs_type,
					   float array1d_iband_Rrs[6],
					   float array1d_idepth_chl[NBDEPTHS],
					   float array1d_itime_cf[9],
					   float array1d_itime_o3[9],
					   float array1d_itime_taucld[9],
					   float downward_irradiance_table[83][19][10][8][7],
					   float array1d_idepth_pp[100]);
%clear (float array1d_itime_cf[9]);
%clear (float array1d_itime_o3[9]);
%clear (float array1d_itime_taucld[9]);
%clear (float downward_irradiance_table[83][19][10][8][7]);

// Common arguments
%clear (float array1d_iband_Rrs[6]);
%clear (float array1d_idepth_chl[NBDEPTHS]);
%clear (float array1d_idepth_pp[100]);
