/*
Translation of SZA {RAtmosphere} into C code.

This function provide Solar Zenith Angle for a specified time , latitude and
longitude.

*/
double sun_zenithal_angle(int yday, double hour, double minute,
                                        double second, double latitude,
                                        double longitude);

/*
Fortran -> C++
*/

double sun_zenithal_angle_approximation(int yday, double hour, double latitude,
                                        double longitude);