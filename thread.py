#!/usr/bin/env python3
from netCDF4 import Dataset
from wrf import getvar
import os 
import sys 
import numpy as np
from datetime import datetime, timedelta

eventday = datetime(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
print(eventday)
if datetime(2015,12,31,0) <= eventday <= datetime(2016,12,30,12):
    t_bottom = 0.           # Tempmerature of cloud botton in C
    t_top = -38.            # Temperature of cloud top in C   
    nlat,nlon = 180,360     # Resolution of WRF data
    data_type = 'DS083.3'   # GDAS data
    timeoffset, timeduration = 0, 49
    mainpath = os.path.join(os.getenv('HOME'),'wrfmain', 'global-1.0', 'RDA_' + data_type)  
    resultpath = os.path.join(os.getenv('PWD'),'data')  
    c_top      = np.zeros([timeduration, nlat, nlon],dtype=int)
    c_bottom   = np.zeros([timeduration, nlat, nlon],dtype=int)
    timeindex  = range(timeoffset, timeoffset + timeduration)

    savefile = eventday.strftime('-%Y-%m-%d-%H')    
    wrffile = os.path.join(mainpath, eventday.strftime('%Y%m%d%H'), eventday.strftime('wrfout_d01_%Y-%m-%d_%H:00:00'))
    ncfile = Dataset(wrffile)
    rainc = getvar(ncfile, 'RAINC', timeidx = timeindex, meta=False)
    pw = getvar(ncfile, 'pw', timeidx = timeindex, meta=False)
    maskcape = getvar(ncfile, 'cape_2d',  timeidx=timeindex, meta=False)
    maskcape = maskcape.filled(fill_value=0)
    cape = np.array(maskcape[0,:,:,:])      
    z = getvar(ncfile, 'z', units='m', meta=False)
    tk = getvar(ncfile, 'tk', timeidx=timeindex, meta=False)
    tc_bot = tk - (273.15 + t_bottom)
    tc_top = tk - (273.15 + t_top)
    for i in range(tk.shape[0]):
        t0_b = np.sign(tc_bot[i])
        t0_bix = np.argmax(t0_b < 0, axis=0)
        h_b = z.reshape(z.shape[0]*nlat*nlon)[t0_bix.reshape(nlat*nlon)*nlat*nlon + np.arange(nlat*nlon)]
        c_bottom[i] = h_b.reshape(nlat,nlon) 
               
        t0_t = np.sign(tc_top[i])
        t0_tix = np.argmax(t0_t < 0, axis=0 )
        h_t = z.reshape(z.shape[0]*nlat*nlon)[t0_tix.reshape(nlat*nlon)*nlat*nlon + np.arange(nlat*nlon)]
        c_top[i] = h_t.reshape(nlat,nlon) 

    np.savez_compressed(os.path.join(resultpath, 'CAPE'+ savefile), cape)
    np.savez_compressed(os.path.join(resultpath, 'RAIN'+ savefile), rainc)
    np.savez_compressed(os.path.join(resultpath, 'PRWA'+ savefile), pw)
    np.savez_compressed(os.path.join(resultpath, 'CTOP'+ savefile), c_top)
    np.savez_compressed(os.path.join(resultpath, 'CBOT'+ savefile), c_bottom)
