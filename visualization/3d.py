#%%
import matplotlib.pyplot as plt
import numpy as np
import json

#%%
#Read JSON file
with open('41de94ea9d135d78636a4bf0739551064dab697f.json') as f:
    d = json.load(f)
 
#Change JSON file type (list) to numpy array
data = np.asarray(d)

#Change 9999 value to -1 (in case json file was used to create contour map first)
data[data == 9999] = 1

#Find min value in the array to set as min of the color palette
a = np.amin(data)

#Find max value in the array to set as min of the color palette
#Sort array into a list from max to min, disregard to repeating values
#rounded the decimals to 10 digits, choose the second largest value
#as the largest is 99999
b = np.partition(np.unique(data.flatten().round(decimals=10)), -1)[-2]

#%%
#Insert coordinates
xmin =  float(input('Insert xmin: '))
xmax =  float(input('Insert xmax: '))
ymax =  float(input('Insert ymin: '))
ymin =  float(input('Insert ymax: '))

#Create x and y axis data based on coordinate
xAxis = np.linspace(xmax,xmin,num=np.shape(data)[0])
yAxis = np.linspace(ymax,ymin,num=np.shape(data)[1])
#[32.50739565519518, 34.76665194213551]
#[32.45585808775892, 34.73041834971132]

title = input('Input graph title: ')

#Make a grid from xAxis and yAxis arrays
X ,Y = np.meshgrid(xAxis,yAxis)

#Map resolution (by editting intervals on scale bar)
c = int(input('Insert a number to edit scale bar levels: '))

#%%
#Insert scale bar label
clblabel = input('Insert z axis label: ')

#Choose map color:
cmap = input('Choose map color: ') #try Greens_r

#Ratio of long to short dimensions of scale bar
clbwidth = int(input('Changing aspect: ')) #try 30

#Set cbar label
cbarlabel = input('Change scale bar label: ')

#%%Text size
axislabelsize = int(input('Axis text size: '))
ticklabelsize = int(input('Tick text size: '))
scalebarsize = int(input('Scale bar text size: '))

#%%Change in viewing angle
azim = int(input('Change azimuthal viewing angle: '))
elev = int(input('Change elevation viewing angle: '))

#%%
#Export file name
name = input("Save file as: ")
#Choose file type and dpi values:
print("Available file type: jpg, png, svg.")
filetype = input('Choose export file type: ')
print("Recommended dpi values: 300, 600, 1200.")
dpi = int(input('Choose desired dpi: '))

#%%
#Plotting 3D 
def make_3D_visualization():
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    levels = np.linspace(a, b, c)
    d = ax.plot_surface(X, Y, data, cmap = cmap, vmin = a, vmax = b)
    #plt.gca().invert_xaxis()
    #plt.colorbar(ticks=levels)
    cbar = fig.colorbar(d, shrink=0.5, aspect=clbwidth, location = 'bottom', pad = 0.05, anchor = (0.5, 0.5))
    #Font size for color bar
    cbar.ax.tick_params(labelsize=ticklabelsize)
    cbar.set_label(cbarlabel,size=scalebarsize)
    ax.set_xlabel('Latitude', size=axislabelsize)
    ax.set_ylabel('Longitude', size=axislabelsize)
    ax.set_zlabel(clblabel, size=axislabelsize)
    plt.title(title)
    ax.azim = azim
    ax.elev = elev
    #Font size for x y z axes
    ax.tick_params(axis='both', which='major', labelsize=ticklabelsize)
    ax.tick_params(axis='both', which='minor', labelsize=ticklabelsize)
    fig.savefig(name + '.' + filetype, format=filetype, dpi=dpi)

make_3D_visualization()


