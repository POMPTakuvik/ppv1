/*
 * See comments in the header Color.h.
 */
#include <stdio.h>
#include <stdlib.h>

#include "Color.h"

/* ------------------------------------------------------------------ */

int get_itime(float time){
  if(time < 0. || time > 24.){
    printf("Error in Color.c, get_itime(float time).\n time: %.3f should be between -180 and 180 degrees East.\n",
	   time);
    exit(-1);
  }
  int itime = -1;
  float itimef = time / 3.;
  itime = (int)(itimef + 0.5);
  return itime;
}
/* ------------------------------------------------------------------ */
