#include <stdio.h>
#include <strings.h>
#include <fstream>
#include <iostream>
#include <vector>


#define NVIS 61
#define NBWL 83
#define NO3 10
#define NTAUCLD 8
#define NTHETAS 19
#define NALB 7



int sub2index(float dim[5], int idx_r, int idx_l, int idx_rho, int idx_alpha,
              int idx_beta);

extern "C" void ed0moins(int jday, double rtime, double lat, double lon,
                             double o3, double tcl, double cf, 
                             float Ed_pixel[NBWL],
                             float ed_lut[NBWL][NTHETAS][NO3][NTAUCLD][NALB], 
                             double thetas);


extern "C" void read_ed0moins_lut_(const char *filename, float ptr[NBWL][NTHETAS][NO3][NTAUCLD][NALB]);

extern "C" void convert_4d_to_5d_with_constant_albedo(float lut_4d[NTAUCLD][NO3][NTHETAS][NBWL], float lut_5d[NBWL][NTHETAS][NO3][NTAUCLD][NALB]);

void get_indice(std::vector<float> vec, float target, int &ii, float &rr, float overflow_max_value);

std::vector<float> interpol_ed0moins(float ed_lut[NBWL][NTHETAS][NO3][NTAUCLD][NALB],
                                          double thetas, double ozone, double taucl,
                                          double alb);
