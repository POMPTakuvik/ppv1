#include "interpolation_lut.hpp"
#include "sza.h"
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdio.h>
#include <strings.h>
#include <vector>

std::vector<float> interpol_ed0moins(float ed_lut[83][19][10][8][7],
                                      double thetas, double ozone, double taucl,
                                      double alb) {

  
  

  
  int nwl = 83;

  float ed_tmp4[nwl][2][2][2];
  float ed_tmp3[nwl][2][2];
  float ed_tmp2[nwl][2];
  std::vector<float> ed(nwl);

  // Thetas
  std::vector<float> xthetas;
  for (int i = 0; i <= 90; i += 5) {
    xthetas.push_back(i);
  }

  // Ozone
  std::vector<float> xozone;
  for (int i = 100; i <= 550; i += 50) {
    xozone.push_back(i);
  }

  // Taucl
  std::vector<float> xtaucl;
  xtaucl.push_back(0);
  xtaucl.push_back(1);
  xtaucl.push_back(2);
  xtaucl.push_back(4);
  xtaucl.push_back(8);
  xtaucl.push_back(16);
  xtaucl.push_back(32);
  xtaucl.push_back(64);

  // Albedo
  std::vector<float> xalb;
  for (float i = 0.05; i <= 1; i += 0.15) {
    xalb.push_back(i);
  }

  // Find the index where the requested values are.
  int ithetas, iozone, itaucl, ialb;
  float rthetas, rozone, rtaucl, ralb;

  get_indice(xthetas, thetas, ithetas, rthetas, 89.99);
  get_indice(xozone, ozone, iozone, rozone, 549.99);
  get_indice(xtaucl, taucl, itaucl, rtaucl, 63.99);
  get_indice(xalb, alb, ialb, ralb, 0.9499);

  // std::cout << thetas << " " << ithetas << " " << rthetas << std::endl;
  // std::cout << ozone << " " << iozone << " " << rozone << std::endl;
  // std::cout << taucl << " " << itaucl << " " << rtaucl << std::endl;
  // std::cout << alb << " " << ialb << " " << ralb << std::endl;

  // Start interpolation
  int zthetas, zozone, ztaucl;

  // Remove the dimension on Surface Albedo
  for (int i = 0; i <= 1; i++) {

    zthetas = ithetas + i; // Need to fix

    // std::cout << zthetas << std::endl;

    for (int j = 0; j <= 1; j++) {

      zozone = iozone + j; // Need to fix
      // std::cout << zozone << std::endl;

      for (int k = 0; k <= 1; k++) {

        ztaucl = itaucl + k; // Need to fix
        // std::cout << ztaucl << std::endl;

        for (int l = 0; l < nwl; l++) {
          // Line 128
          ed_tmp4[l][i][j][k] =
              ((1 - ralb) * ed_lut[l][zthetas][zozone][ztaucl][ialb]) +
              (ralb * ed_lut[l][zthetas][zozone][ztaucl][ialb + 1]);
        }
      }
    }
  }

  // Remove the dimension on taucl
  for (int i = 0; i <= 1; i++) {
    for (int j = 0; j <= 1; j++) {
      for (int l = 0; l < nwl; l++) {
        ed_tmp3[l][i][j] =
            (1 - rtaucl) * ed_tmp4[l][i][j][0] + rtaucl * ed_tmp4[l][i][j][1];
        // std::cout << ed_tmp3[l][i][j] << std::endl;
      }
    }
  }

  // Remove the dimension on ozone
  for (int i = 0; i <= 1; i++) {
    for (int l = 0; l < nwl; l++) {
      ed_tmp2[l][i] =
          (1 - rozone) * ed_tmp3[l][i][0] + rozone * ed_tmp3[l][i][1];
      // std::cout << ed_tmp2[l][i] << std::endl;
    }
  }

  // Remove the dimention on sunzenith angle
  for (int l = 0; l < nwl; l++) {
    ed[l] = (1 - rthetas) * ed_tmp2[l][0] + rthetas * ed_tmp2[l][1];
    // std::cout << ed[l] << std::endl;
  }

  return (ed);
}




int sub2index(float dim[5], int idx_r, int idx_l, int idx_rho, int idx_alpha,
              int idx_beta) {

  int index =
      (((idx_beta * dim[3] + idx_alpha) * dim[2] + idx_rho) * dim[1] + idx_l) *
          dim[0] +
      idx_r + 1;

  return (index);
}

void ed0moins(int jday, double rtime, double lat, double lon,
                             double o3, double tcl, double cf, 
                             float Ed_pixel[NBWL],
                             float ed_lut[NBWL][NTHETAS][NO3][NTAUCLD][NALB], 
                             double thetas) {

    

  std::vector<float> ed_cloud =
      interpol_ed0moins(ed_lut, thetas, o3, tcl, 0.05);
  std::vector<float> ed_clear =
      interpol_ed0moins(ed_lut, thetas, o3, 0, 0.05);

  std::vector<float> ed_inst;

  const int nwl = ed_cloud.size();

  for (int i = 0; i < nwl; i++) {

    if (thetas < 90) {
      Ed_pixel[i] = (ed_cloud[i] * cf) + (ed_clear[i] * (1 - cf));
    } else {
      Ed_pixel[i] = 0;
    }
  }

}


void read_ed0moins_lut_(const char *filename, float downward_irradiance_table_as_output[NBWL][NTHETAS][NO3][NTAUCLD][NALB]) {


  std::ifstream infile;
  infile.open(filename);
  float tmp;
  int iteration = 0;
  for (int theta = 0; theta < NTHETAS; theta++) {
    for (int ozone = 0; ozone < NO3; ozone++) {
      for (int taucl = 0; taucl < NTAUCLD; taucl++) {
        for (int albedo = 0; albedo < NALB; albedo++) {
          for (int wavelength = 0; wavelength < NBWL; wavelength++) {
            infile >> tmp;
            downward_irradiance_table_as_output[wavelength][theta][ozone][taucl][albedo] = tmp;        
          }
        }
      }
    }
  }

  // Close file
  infile.close();
}

/*
 * Function to get the closest index of the target into the LUT.
 */
void get_indice(std::vector<float> vec, float target, int &ii, float &rr, float overflow_max_value) {

  // std::cout << target << "****" << std::endl;

  // std::cout << target << ":" <<  vec[0] << std::endl;

  if (target < vec[0]) {
    ii = 0;
    rr = 0;
  } else if (target >= vec[vec.size() - 1]) {
    ii = vec.size() - 2;
    rr = (overflow_max_value - vec[ii]) / (vec[ii + 1] - vec[ii]);
  }

  else {

    for (unsigned int i = 0; i < vec.size() - 1; i += 1) {

      if (target >= vec[i] && target < vec[i + 1]) {
        ii = i;
      }
    }

    rr = (target - vec[ii]) / (vec[ii + 1] - vec[ii]);
  }
}
