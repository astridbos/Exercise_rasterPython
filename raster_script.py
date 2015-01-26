## AD-scripting
## Friday 23 January 2015
## Exercise for lesson 15, on "Raster data handling with Python"

##########################
##### Initialization ##### 
##########################

import os
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
import numpy as np

gdal.AllRegister()

os.chdir("/home/user/Git/Python_raster")

##########################
###### Import data ####### 
##########################
driver = gdal.GetDriverByName('GTiff')

filename4 = 'data/LC81980242014260LGN00_sr_band4.tif'
filename5 = 'data/LC81980242014260LGN00_sr_band5.tif'

dataSource4 = gdal.Open(filename4, GA_ReadOnly)
dataSource5 = gdal.Open(filename5, GA_ReadOnly)

##########################
#### Generate arrays ##### 
##########################
band4 = dataSource4.GetRasterBand(1)
band5 = dataSource5.GetRasterBand(1)

band4Arr = band4.ReadAsArray(0,0,dataSource4.RasterXSize, dataSource4.RasterYSize)
band5Arr = band5.ReadAsArray(0,0,dataSource5.RasterXSize, dataSource5.RasterYSize)

##########################
#### Calculate NDWI ###### 
##########################
NDWI = (band4Arr - band5Arr) / (band4Arr + band5Arr)

band4Arr = band4Arr.astype(np.float32)
band5Arr = band5Arr.astype(np.float32)

mask = np.greater(band4Arr+band5Arr,0)
NDWI = np.choose(mask,(-99,NDWI))

##########################
###### Export NDWI #######
##########################

outDataSet=driver.Create('data/NDWI.tif', dataSource4.RasterXSize, dataSource4.RasterYSize, 1, GDT_Float32)
outBand = outDataSet.GetRasterBand(1)
outBand.WriteArray(NDWI,0,0)
outBand.SetNoDataValue(-99)
outDataSet.SetProjection(dataSource4.GetProjection())
outBand.FlushCache()
outDataSet.FlushCache()
