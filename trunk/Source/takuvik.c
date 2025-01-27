/*
 * See comments in the header takuvik.h.
 */

#include "takuvik.h"

int array1dfcmp(float* a1, float* a2, int n){
  float f1;
  float f2;
  int i   = 0;
  int ret = 0;
  while(!ret && i < n){
    f1 = a1[i];
    f2 = a2[i];
    ret = fcmp(f1, f2);
    i++;
  }
  return ret;
}

int array2dfcmp(int m, int n, float a1[m][n], float a2[m][n]){
  float f1;
  float f2;
  int i   = 0;
  int j   = 0;
  int ret = 0;
  while(!ret && i < m){
    j = 0;
    while(!ret && j < n){
      f1 = a1[i][j];
      f2 = a2[i][j];
      ret = fcmp(f1, f2);
      j++;
    }
    i++;
  }
  return ret;
}

int compare_float(const void *a, const void*b){
  float a_val = *(float*)a;
  float b_val = *(float*)b;
  int output = 0;
  if(a_val > b_val){
    output = 1;
  }else if(a_val < b_val){
    output = -1;
  }
  return output;
}

int fcmp(float f1, float f2){
  int ret = 0;
  if( gt(f1, f2) ){
    ret = 1;
  }else if( gt(f2, f1) ){
    ret = -1;
  }
  return ret;
}

int ge(float f1, float f2){
  int ret = 0;
  if(f1 - f2 > -2. * MY_FLT_EPSILON){
    ret = 1;
  }
  return ret;
}

int get_array1df_i_from_array2df_i_j(int ni,
				     int nj,
				     float array2df_i_j[ni][nj],
				     int j_target,
				     float array1df_i[ni]){
  int ret = 0;
  if(j_target < 0 || j_target >= nj){
    printf("Error in takuvik.c, get_array1df_i_from_array2df_i_j(int ni, int nj, float array2df_i_j[ni][nj], int j_target, float array1df_i[ni]).\n j_target: %d is out of bounds: %d.\n",
	   j_target,
	   nj - 1);
    ret = -1;
    exit(-1);
  }
  int i;
  for(i = 0; i < ni; i++){
    array1df_i[i] = array2df_i_j[i][j_target];
  }
  return ret;
}

float get_timeGMT_local_noon(float lon){
  if(lon < -180. || lon > 180.){
    printf("Error in takuvik.c, get_timeGMT_local_noon(float lon).\n lon: %f should be between -180 and 180 degrees East.\n",
	   lon);
    exit(-1);
  }
  float timeGMT_local_noon = -999.;
  if(lon == -180.){
    lon = 180.;
  }
  timeGMT_local_noon = 12. - (lon / 15.);
  return timeGMT_local_noon;
}

int gt(float f1, float f2){
  int ret = 0;
  if(f1 - f2 > MY_FLT_EPSILON){
    ret = 1;
  }
  return ret;
}

int is_array1df_valid(float* a1, int n){
  int i = 0;
  int ret = 1;
  while(ret && i < n){
    if(a1[i] < 0){
      ret = 0;
    }
    i++;
  }
  return ret;
}

int make_sure_last_character_is_slash(char* s){
  char last_char;
  int len; 
  len = strlen(s);
  last_char = s[len - 1];
  if(last_char != '/'){
    s[len] = '/';
    s[len + 1] = '\0';
  }
  return 0;
}

float mean(float ar[], int n){
  if(n < 1){
    printf("Error in takuvik.c, mean(float ar[], int n).\n Mean of an array of length n: %d\n", n);
  exit(-1);
  }
  float out = 0;
  int i;
  for(i = 0; i < n; i++){
    out += ar[i];
  }
  out /= n;
  return out;
}

float median_libc_qsort(float *ptr_val, int n){
  int i_median;
  float median,
    median_low,
    median_high;
  qsort(ptr_val, n, sizeof(float), compare_float);
  i_median = n / 2;
  if(n % 2 == 1){
    median = ptr_val[i_median];
  }else{
    median_low = ptr_val[i_median - 1];
    median_high = ptr_val[i_median];
    median = (median_low + median_high) / 2.;
  }
  return median;
}
