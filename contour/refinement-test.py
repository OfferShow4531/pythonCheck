#https://stackoverflow.com/questions/33719975/how-to-create-a-2d-mesh-with-refinement-python/33720268#33720268
#https://stackoverflow.com/questions/9236926/concatenating-two-one-dimensional-numpy-arrays
#https://stackoverflow.com/questions/50997928/typeerror-only-integer-scalar-arrays-can-be-converted-to-a-scalar-index-with-1d

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

#Change to float32 dtype to make geotiff file
data32 = np.float32(data)

#Change -1 value to 9999 (in case negative elevations in some areas)
data[data == -1] = 9999
print(data[105,100])
print(data[3:5,19:30])
print(data[:,0])

#Find min value in the array to set as min of the color palette
a = np.amin(data)

#Find max value in the array to set as min of the color palette
#Sort array into a list from max to min, disregard to repeating values
#rounded the decimals to 10 digits, choose the second largest value
#as the largest is 9999
b = np.partition(np.unique(data.flatten().round(decimals=10)), -1)[-2]

xmin =  32.45585808775892
xmax =  32.50739565519518
ymax =  34.76665194213551
ymin =  34.73041834971132

#Create x and y axis data based on coordinate
xAxis = np.linspace(32.50739565519518,32.45585808775892,num=np.shape(data)[0])
yAxis = np.linspace(34.76665194213551,34.73041834971132,num=np.shape(data)[1])
#[32.50739565519518, 34.76665194213551] - xmax, ymax
#[32.45585808775892, 34.73041834971132] - xmin, ymin

#Make a grid from xAxis and yAxis arrays
X ,Y = np.meshgrid(xAxis,yAxis)

#%%
refinement = input('Do you want to refine your grid (Yes/No)? ')
if refinement == 'Yes':
    x_refinestart = int(input('Starting cell of x axis: '))
    x_refineend = int(input('Ending cell of x axis: '))
    x_refinestep = int(input('Refining step of x axis: '))
    y_refinestart = int(input('Starting cell of y axis: '))
    y_refineend = int(input('Ending cell of y axis: '))
    y_refinestep = int(input('Refining step of y axis: '))
    i, j, k, l, m = 0
    refinedata = []
    if x_refinestart == 0:
        xAxis_refine = np.concatenate((np.linspace(xAxis[x_refinestart], xAxis[x_refineend], num=x_refinestep),
                                      np.linspace(xAxis[x_refineend], xmax, num=np.shape(data)[0]-x_refineend)))
        if y_refinestart == 0:
            yAxis_refine = np.concatenate((np.linspace(yAxis[y_refinestart], yAxis[y_refineend], num=y_refinestep),
                                           np.linspace(yAxis[y_refineend], ymax, num=np.shape(data)[0]-y_refineend)))
        if y_refinestart > 0 and y_refinestart < np.shape(data)[1]:
            yAxis_refine = np.concatenate((np.linspace(ymin, yAxis[y_refinestart], num= y_refinestart),
                                          np.linspace(yAxis[y_refinestart], yAxis[y_refineend], num= y_refinestep),
                                          np.linspace(yAxis[y_refineend], ymax, num=np.shape(data)[0]-y_refineend)))
        if y_refineend == np.shape(data)[1]:
            yAxis_refine = np.concatenate((np.linspace(ymin, yAxis[y_refinestart], num= y_refinestart),
                                         np.linspace(yAxis[y_refinestart], ymax, num=y_refineend-y_refinestart)))
        X_refine ,Y_refine = np.meshgrid(xAxis_refine,yAxis_refine) 
        
        #xAxis_value = 
        #yAxis_value = 
    elif x_refinestart > 0 and x_refinestart < np.shape(data)[0]:
        xAxis_refine = np.concatenate((np.linspace(xmin, xAxis[x_refinestart], num= x_refinestart),
                                      np.linspace(xAxis[x_refinestart], xAxis[x_refineend], num= x_refinestep),
                                      np.linspace(xAxis[x_refineend], xmax, num=np.shape(data)[0]-x_refineend)))
        if y_refinestart == 0:
            yAxis_refine = np.concatenate((np.linspace(yAxis[y_refinestart], yAxis[y_refineend], num=y_refinestep),
                                           np.linspace(yAxis[y_refineend], ymax, num=np.shape(data)[0]-y_refineend)))
        if y_refinestart > 0 and y_refinestart < np.shape(data)[1]:
            yAxis_refine = np.concatenate((np.linspace(ymin, yAxis[y_refinestart], num= y_refinestart),
                                          np.linspace(yAxis[y_refinestart], yAxis[y_refineend], num= y_refinestep),
                                          np.linspace(yAxis[y_refineend], ymax, num=np.shape(data)[0]-y_refineend)))
        if y_refineend == np.shape(data)[1]:
            yAxis_refine = np.concatenate((np.linspace(ymin, yAxis[y_refinestart], num= y_refinestart),
                                         np.linspace(yAxis[y_refinestart], ymax, num=y_refineend-y_refinestart)))
        X_refine ,Y_refine = np.meshgrid(xAxis_refine,yAxis_refine)
        #xAxis_value = 
        #yAxis_value =  
    elif x_refineend == np.shape(data)[0]:
        xAxis_refine = np.concatenate((np.linspace(xmin, xAxis[refinestart], num=refinestart),
                                      np.linspace(xAxis[refinestart], xmax, num=refineend-refinestart)))
        if y_refinestart == 0:
            yAxis_refine = np.concatenate((np.linspace(yAxis[y_refinestart], yAxis[y_refineend], num=y_refinestep),
                                           np.linspace(yAxis[y_refineend], ymax, num=np.shape(data)[0]-y_refineend)))
        if y_refinestart > 0 and y_refinestart < np.shape(data)[1]:
            yAxis_refine = np.concatenate((np.linspace(ymin, yAxis[y_refinestart], num= y_refinestart),
                                          np.linspace(yAxis[y_refinestart], yAxis[y_refineend], num= y_refinestep),
                                          np.linspace(yAxis[y_refineend], ymax, num=np.shape(data)[0]-y_refineend)))
        if y_refineend == np.shape(data)[1]:
            yAxis_refine = np.concatenate((np.linspace(ymin, yAxis[y_refinestart], num= y_refinestart),
                                         np.linspace(yAxis[y_refinestart], ymax, num=y_refineend-y_refinestart)))
        X_refine ,Y_refine = np.meshgrid(xAxis_refine,yAxis_refine)
        #xAxis_value = 
        #yAxis_value =
    for m in range(x_refinestart, x_refineend):
        m = x_refinestart
        refinedata = np.vstack(data[:,m])
        while data[:,m] == data[:,m+1]:
            refinedata = np.column_stack(data[:,m+1])
            m += 1
            if data[:,m-1] != data[:,m]:
                refinedata = np.vstack(data[:,m+1])
            
            
        #data[:,x_refinestart:x_refineend] = data[:,x_refinestart]
    while j < x_refineend and l < y_refineend:
        i = int(input('Starting cell on x axis of refinement: '))
        j = int(input('Ending cell on x axis of refinement: '))
        #adding_values = 
        k = int(input('Starting cell on y axis of refinement: '))
        l = int(input('Ending cell on y axis of refinement: '))
        
        
    

#%%Refinement_test_1_seems_wrong
if refinestart == 0:
    xAxis_refine = np.concatenate((np.linspace(xAxis[refinestart], xAxis[refineend], num=refinestep),
                                  np.linspace(xAxis[refineend], xmax, num=np.shape(data)[0]-refineend)))
    yAxis_refine = np.concatenate((np.linspace(yAxis[refinestart], yAxis[refineend], num=refinestep),
                                  np.linspace(yAxis[refineend], ymax, num=np.shape(data)[0]-refineend)))
    X_refine ,Y_refine = np.meshgrid(xAxis_refine,yAxis_refine)
    xAxis_value = 
    yAxis_value = 
elif refinestart > 0 and refinestart < 200:
    xAxis_refine = np.concatenate((np.linspace(xmin, xAxis[refinestart], num= refinestart),
                                  np.linspace(xAxis[refinestart], xAxis[refineend], num=refinestep),
                                  np.linspace(xAxis[refineend], xmax, num=np.shape(data)[0]-refineend)))
    yAxis_refine = np.concatenate((np.linspace(xmin, xAxis[refinestart], num= refinestart),
                                  np.linspace(xAxis[refinestart], xAxis[refineend], num=refinestep),
                                  np.linspace(xAxis[refineend], xmax, num=np.shape(data)[0]-refineend)))
    X_refine ,Y_refine = np.meshgrid(xAxis_refine,yAxis_refine)
    xAxis_value = 
    yAxis_value = 
elif refineend == 200:
    xAxis_refine = np.concatenate((np.linspace(xmin, xAxis[refinestart], num=refinestart),
                                  np.linspace(xAxis[refinestart], xmax, num=refineend-refinestart)))
    yAxis_refine = np.concatenate((np.linspace(ymin, yAxis[refinestart], num=refinestart),
                                  np.linspace(yAxis[refinestart], ymax, num=refineend-refinestart)))
    X_refine ,Y_refine = np.meshgrid(xAxis_refine,yAxis_refine)
    xAxis_value = 
    yAxis_value = 

#%%Not_need
def grid_refinement():
    
#%%Not_need_either


if refinement == 'Yes':
    
    grid_refinement()
    
#%%Example_of_concatenate
start = 0
end = 1
bigstep = 0.1

refinedstart = 0.4
refinedend = 0.6
smallstep = 0.01

x = np.concatenate([np.arange(start, refinedstart, bigstep),
                       np.arange(refinedstart, refinedend, smallstep),
                       np.arange(refinedend, end, bigstep)])
print(x)
    