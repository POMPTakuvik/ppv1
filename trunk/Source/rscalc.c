// C++ program calculating the sunrise and sunset for
// the current date and a fixed location(latitude,longitude)
// Jarmo Lammi 1999 - 2000
// Last update January 6th, 2000
// Modifie par Maxime Benoit-Gagne
// 27 fevrier 2012
// C'est maintenant un programme C.

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define pi 3.14159265
#define tpi (2 * pi)
#define degs (180.0/pi)
#define rads (pi/180.0)

float L,g,daylen;
#define SunDia 0.53     // Sunradius degree

#define AirRefr (34.0/60.0) // athmospheric refraction degrees //

//   Get the days to J2000
//   h is UT in decimal hours
//   FNday only works between 1901 to 2099 - see Meeus chapter 7

float FNday (int y, int m, int d) {
  int luku = - 7 * (y + (m + 9)/12)/4 + 275*m/9 + d;
  // type casting necessary on PC DOS and TClite to avoid overflow
  luku+= (long int)y*367;
  return (float)luku - 730531.5 + 0.5;
};

//   the function below returns an angle in the range
//   0 to 2*pi

float FNrange (float x) {
  float b = x / tpi;
  float a = tpi * (b - (long)(b));
  if (a < 0) a = tpi + a;
  return a;
};

// Calculating the hourangle
//
float f0(float lat, float declin) {
  float fo,dfo;
  // Correction: different sign at S HS
  dfo = rads*(0.5*SunDia + AirRefr); if (lat < 0.0) dfo = -dfo;
  fo = tan(declin + dfo) * tan(lat*rads);
  if (fo>0.99999) fo=1.0; // to avoid overflow //
  if (fo<-0.99999) fo=-1.0; // to avoid overflow //
  fo = asin(fo) + pi/2.0;
  return fo;
};

//   Find the ecliptic longitude of the Sun
float FNsun (float d) {
  //   mean longitude of the Sun
  L = FNrange(280.461 * rads + .9856474 * rads * d);
  //   mean anomaly of the Sun
  g = FNrange(357.528 * rads + .9856003 * rads * d);
  //   Ecliptic longitude of the Sun
  return FNrange(L + 1.915 * rads * sin(g) + .02 * rads * sin(2 * g));
};

float daylength(int y, int m, int day, float latit){
  float d = FNday(y, m, day);
  //   Use FNsun to find the ecliptic longitude of the Sun
  float lambda = FNsun(d);
  //   Obliquity of the ecliptic
  float obliq = 23.439 * rads - .0000004 * rads * d;
  //   Find the RA and DEC of the Sun
  float alpha = atan2(cos(obliq) * sin(lambda), cos(lambda));
  float delta = asin(sin(obliq) * sin(lambda));
  // Find the Equation of Time in minutes
  // Correction suggested by David Smith
  float LL = L - alpha;
  if (L < pi) LL += tpi;
  float ha = f0(latit,delta);
  // Conversion of angle to hours and minutes //
  daylen = degs*ha/7.5;
  if (daylen<0.0001) {daylen = 0.0;}
  // arctic winter     //
  daylen *= 3600.;
  return daylen;
}

