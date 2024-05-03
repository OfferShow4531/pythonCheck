#%%
import matplotlib.pyplot as plt
import numpy as np
import json

from osgeo import gdal
from osgeo import osr

#%%
#Read JSON file
with open('41de94ea9d135d78636a4bf0739551064dab697f.json') as f:
    d = json.load(f)
 
#Change JSON file type (list) to numpy array
data = np.asarray(d)

#Change to float32 dtype to make geotiff file
data32 = np.float32(data)

#Change -1 value to 9999 (in case negative elevations in some areas)
data[data == -1] = 9999

#Find min value in the array to set as min of the color palette
a = np.amin(data)

#Find max value in the array to set as min of the color palette
#Sort array into a list from max to min, disregard to repeating values
#rounded the decimals to 10 digits, choose the second largest value
#as the largest is 9999
b = np.partition(np.unique(data.flatten().round(decimals=10)), -1)[-2]


#%%
#Insert coordinates
xmin =  float(input('Insert xmin: '))
xmax =  float(input('Insert xmax: '))
ymax =  float(input('Insert ymin: '))
ymin =  float(input('Insert ymax: '))
#Total Rows: np.shape(data)[0]
#Total Columns: np.shape(data)[1]

title = input('Input graph title: ')

#Create x and y axis data based on coordinate
xAxis = np.linspace(xmax,xmin,num=np.shape(data)[0])
yAxis = np.linspace(ymax,ymin,num=np.shape(data)[1])
#[32.50739565519518, 34.76665194213551] - xmax, ymax
#[32.45585808775892, 34.73041834971132] - xmin, ymin

#Make a grid from xAxis and yAxis arrays
X ,Y = np.meshgrid(xAxis,yAxis)

#Change to float32 dtype to make geotiff file
X32 = np.float32(X)
Y32 = np.float32(Y)

#Map resolution (by editting intervals on scale bar)
c = int(input('Insert a number to edit scale bar levels: '))

#%%
#Export file name
name = input("Save file as: ")

#Choose file type and dpi values:
print("Available file type: jpg, png, svg.")
filetype = input('Choose export file type: ')
print("Recommended dpi values: 300, 600, 1200.")
dpi = int(input('Choose desired dpi: '))

#%%
#Insert scale bar label
clblabel = input('Insert scale bar label: ')

#Adjust label orientation
rotation = int(input('Adjust label orientation: '))

#Adjust label distance from scale bar
distance = int(input('Adjust label distance from scale bar: '))

#Change contour map color, try 'Green'
cmap = input('Change contour map color: ')

#%%
invert_x = input('Rotate x axis (Yes/No): ')
invert_y = input('Rotate y axis (Yes/No): ')

#%%
#https://gis.stackexchange.com/questions/37238/writing-numpy-array-to-raster-file
def export_geotiff_from_array():
    array = data32
    # My image array      
    lat = Y32
    lon = X32
    # For each pixel I know it's latitude and longitude.
    # As you'll see below you only really need the coordinates of
    # one corner, and the resolution of the file.
    xmin,ymin,xmax,ymax = [lon.min(),lat.min(),lon.max(),lat.max()]
    nrows,ncols = np.shape(array)
    xres = (xmax-xmin)/float(ncols)
    yres = (ymax-ymin)/float(nrows)
    geotransform=(xmin,xres,0,ymax,0, -yres)   
    # That's (top left x, w-e pixel resolution, rotation (0 if North is up), 
    #         top left y, rotation (0 if North is up), n-s pixel resolution)
    # I don't know why rotation is in twice???
    output_raster = gdal.GetDriverByName('GTiff').Create(tifname + '.tif',ncols, nrows, 1 ,gdal.GDT_Float32)  # Open the file
    output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
    srs = osr.SpatialReference()                 # Establish its coordinate encoding
    srs.ImportFromEPSG(4326)                     # This one specifies WGS84 lat long.
    output_raster.SetProjection(srs.ExportToWkt() )   # Exports the coordinate system to the file
    output_raster.GetRasterBand(1).WriteArray(array)   # Writes my array to the raster
    output_raster.FlushCache()
    
#%%
#Export contour as raster
ask = input('Do you want to export an raster (Yes/No)? ')
if ask == 'Yes':
    tifname = input('Input export file name: ')
    export_geotiff_from_array()


#%%
#Plotting contour map
def make_contour_map():
    fig, ax = plt.subplots()
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title(title)
    levels = np.linspace(a, b, c)
    plt.contourf(X,Y,data, corner_mask = False, levels=levels, cmap=cmap)
    if invert_x == 'Yes':
        plt.gca().invert_xaxis()
    if invert_y == 'Yes':    
        plt.gca().invert_yaxis()
    clb = plt.colorbar(ticks=levels)
    clb.set_label(label = clblabel, rotation=rotation, labelpad=distance)
    fig.savefig(name + '.' + filetype, format=filetype, dpi=dpi)
make_contour_map()
