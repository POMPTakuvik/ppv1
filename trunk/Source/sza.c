#include "sza.h"
#include "math.h"
#include <stdio.h>

double sun_zenithal_angle(int yday, double hour, double minute, double second,
           double latitude, double longitude) {

  double solar_zenith_angle = 0;

  double d2r = M_PI / 180;
  double r2d = 1 / d2r;

  double d = 23.45 * d2r * sin(d2r * 360 * (284 + yday) / 365);

  double E_qt = 0;

  if (yday <= 106) {
    E_qt = -14.2 * sin(M_PI * (yday + 7) / 111);
  } else {

    if (yday <= 166) {
      E_qt = 4 * sin(M_PI * (yday - 106) / 59);
    } else {

      if (yday <= 246) {
        E_qt = -6.5 * sin(M_PI * (yday - 166) / 80);
      } else {
        E_qt = 16.4 * sin(M_PI * (yday - 247) / 113);
      }
    }
  }

  double T = hour + minute / 60 + second / 3600;

  double T_solar = T + longitude / 15 + E_qt / 60;
  double w = M_PI * (12 - T_solar) / 12;
  double l = latitude * d2r;

  solar_zenith_angle =
      90 - asin(sin(l) * sin(d) + cos(l) * cos(d) * cos(w)) * r2d;

  return (solar_zenith_angle);
}

double sun_zenithal_angle_approximation(int yday, double hour, double latitude,
                                        double longitude) {

  int ltm = 0;
  int hr = (int)hour;
  int min = (int)( (hour - (float)(hr)) * 60);

  double const pi = 3.14159265358979;
  double const d2r = pi / 180.0;
  double const r2d = 1 / d2r;
  double lsn = 12.0 + (((ltm)-longitude) / 15.0);
  double latrad = latitude * d2r;
  double decrad = 23.45 * d2r * sin(d2r * 360. * (284. + (yday)) / 365);
  //double decdeg = decrad * r2d;

  double ha = hr + ((min) / 60.0);
  double hangle = (lsn - ha) * 60.0; // solrad is given for the hour preceeding the time given
  double harad = hangle * 0.0043633; // convert hangle (in minutes) into radians
  // This is the same as multiplying the #hrs by 15 (deg./hr),
  // and convert d2r (*0.017453292)

  double saltrad = asin((sin(latrad) * sin(decrad)) +
                        (cos(latrad) * cos(decrad) * cos(harad)));

  double saltdeg = saltrad * r2d;
  //double sazirad = asin(cos(decrad) * sin(harad) / cos(saltrad));
  //double sazideg = sazirad * r2d;
  double szendeg;
  
  if ((saltdeg < 0) | (saltrad > 180)) {
    saltdeg = 0.0;
    saltrad = 0.0;
    szendeg = 90.0;
    //szenrad = 90.0 * d2r;
  } else {
    szendeg = 90 - saltdeg;
    //szenrad = szendeg * d2r;
  } // sun is below horizon
    // if solaralt=0 -> sin(0)=0

    return(szendeg);
}