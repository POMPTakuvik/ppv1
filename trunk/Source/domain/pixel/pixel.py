import numpy as np
from datetime import datetime

import get_array1d_idepth_pp
from domain.constants import *

class Pixel(object):
    NDEPTHS = 101
    NBANDS = 6
    NB_TIME_INTERVAL = 8
    DEFAULT_FLOAT = -999
    CHL_COLUMN = 1
    CHL_SURFACE = 0

    def __init__(self, lat, lon, year, month, day, doy, ibin45N=0):

        self.lat = np.float32(lat)
        self.lon = np.float32(lon)
        self.year = np.int32(year)
        self.month = np.int32(month)
        self.day = np.int32(day)
        self.doy = np.int32(doy)
        self.ibin45N = np.int32(ibin45N)
        if doy < 0:
            self.doy = datetime.date(year, month, day).timetuple().tm_yday
        if month < 0 or day < 0:
            date = datetime.datetime.strptime(str(year) + str(doy), '%Y%j')
            self.month = date.month
            self.day = date.day

        self.pp = None

    def load_rrs(self, rrs_by_bands):
        self.array1d_iband_Rrs = np.array(rrs_by_bands, dtype=np.float32)

    def load_rrs_type(self, rrs_type):
        self.rrs_type = str(rrs_type)

    def load_chl(self, chlorophyll_type, chl_by_pixel):
        if chlorophyll_type == "surface":
            self.array1d_idepth_chl = np.full(self.NDEPTHS, chl_by_pixel[0], dtype=np.float32)
            # Passe Passe, on creer un vecteur tout le temps parce que, meme si on veut juste la chrolophyl de surface
            # Le code en C s'attend d'avoir deux valeurs pour interpoler la valeur dans le centre de la premiere couche d'eau.
        elif chlorophyll_type == "vertical_profile":
            self.array1d_idepth_chl = np.array(chl_by_pixel, dtype=np.float32)
        else:
            raise ValueError("Chlorphyl type {} is unknown".format(chlorophyll_type))

    def load_cloud_fraction(self, cloud_fraction_by_pixel):
        self.array1d_itime_cf = np.array(cloud_fraction_by_pixel, dtype=np.float32)

    def load_ozone(self, ozone_by_pixel):
        self.array1d_itime_o3 = np.array(ozone_by_pixel, dtype=np.float32)

    def load_taucl(self, taucl_by_pixel):
        self.array1d_itime_taucld = np.array(taucl_by_pixel, dtype=np.float32)

    def load_depth(self, depth_by_pixel):
        self.depth = np.float32(-depth_by_pixel)

    def load_province(self, province_by_pixel):
        self.province = np.uint8(province_by_pixel)


    def calculate_pp(self, primary_production_integration, downward_irradiance_table):
        self.array1d_idepth_pp = np.zeros(shape=get_array1d_idepth_pp.NBDEPTHS - 1, dtype=np.float32)
        # Type verifications and conversions pour passer ca au C
        if(type(self.lat) == np.float32):
            self.lat = self.lat.item()
        if(type(self.lon) == np.float32):
            self.lon = self.lon.item()
        if(type(self.year) == np.int32):
            self.year = self.year.item()
        if(type(self.month) == np.int32):
            self.month = self.month.item()
        if(type(self.day) == np.int32):
            self.day = self.day.item()
        if(type(self.doy) == np.int32):
            self.doy = self.doy.item()
        if (type(self.depth) == np.float32):
            self.depth = self.depth.item()


        get_array1d_idepth_pp.get_array1d_idepth_pp_from_atm(
            self.lat, self.lon, self.year, self.month,
            self.day, self.doy, self.depth,
            self.rrs_type, self.array1d_iband_Rrs, self.array1d_idepth_chl,
            self._propagate_value_for_times(self.array1d_itime_cf),
            self._propagate_value_for_times(self.array1d_itime_o3),
            self._propagate_value_for_times(self.array1d_itime_taucld),downward_irradiance_table,self.array1d_idepth_pp)

        pp = self._calculate_output_pp(primary_production_integration, self.array1d_idepth_pp)
        self.pp = pp

    def _calculate_output_pp(self, primary_production_integration, primary_production_by_depth):
        if primary_production_integration:
            primary_production = np.sum(primary_production_by_depth)
        else:
            primary_production = primary_production_by_depth[0]

        return primary_production

    def _propagate_value_for_times(self, value):
        value_for_each_time_of_the_day = np.zeros(NUMBER_OF_TIMESTEP_IN_DAYS, dtype=np.float32)
        value_for_each_time_of_the_day.fill(value)

        return value_for_each_time_of_the_day



    def dump(self):
        print("{},{},{},{},{},{},{},{},{},{},{},{},{}".format(self.lat,self.lon,self.year,self.month,
            self.day,self.doy,self.depth,
            self.rrs_type,self.array1d_iband_Rrs,self.array1d_idepth_chl[0],
            self.array1d_itime_cf,self.array1d_itime_o3,self.array1d_itime_taucld))