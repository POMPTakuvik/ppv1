/* File : light.i */

/*
 * See comments in the header light.h.
 */
%module light

%{
#define SWIG_FILE_WITH_INIT
  #include "light.h"
  #include "sza.h"
  
%}

%include "numpy.i"

%init %{
  import_array();
%}

#define NBWL 83
#define NO3 10
#define NTAUCLD 8
#define NTIMES 9
#define NTHETAS 19
#define NALB 7 

%apply (float INPLACE_ARRAY5[ANY][ANY][ANY][ANY][ANY]) {(float downward_irradiance_table_as_output[NBWL][NTHETAS][NO3][NTAUCLD][NALB])};
extern int get_downward_irradiance_table(char* filename,
							float downward_irradiance_table_as_output[NBWL][NTHETAS][NO3][NTAUCLD][NALB]);
%clear (float downward_irradiance_table_as_output[NBWL][NTHETAS][NO3][NTAUCLD][NALB]);
