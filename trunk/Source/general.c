/*
 * See comments in the header general.h.
 */

#include "general.h"

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
