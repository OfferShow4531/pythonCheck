#%%
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

#%%
#Read CSV file in the folder
data = pd.read_csv('multipledata.csv')

#Change timeStampt to datetime data
date = pd.to_datetime(data['timeStamp'] ,unit='s')

#Add datetime data as new column in the csv file
data['Datetime']=date

#Add the number of days as new column
data['Days'] = np.arange(len(data))

#Re-arrange column order based on the order of columnsTitles list
cols = list(data.columns)
cols = [cols[0]] + [cols[-1]] + [cols[-2]] + cols[1:len(cols)-2]
data = data[cols]

#columnsTitles = ['timeStamp', 'Days', 'Datetime', 'value','clone']
#data = data.reindex(columns=columnsTitles)

#Create new csv file and add data
data.to_csv('new_chart_multi.csv', index=False)

#%%
#Get to know header names:
print(list(data))

#Choose x and y axis depending on the headers
time    = input('Choose x axis: ')
if time == 'Datetime':
    print('Available x axis format: Day/Month/Year, Year.')
    Xaxisformat = input('Choose x axis format: ')
#%%
xlabel  = input('Input x axis label: ')

obdata  = input('Choose y data for observation: ')

simdata = input('Choose y data for simulation: ')

asksim  = input('Do you want to display simmulated data also (Yes/No)? ')
    
ylabel  = input('Input y axis label: ')

title = input('Input graph title: ')

#%% Ask for plotting many observed data
listmulti = []
listmultilabel =[]
multi = input('Do you want to plot more observed data (Yes/No)? ')
while multi == 'Yes':
    print(list(data))
    addline = input('Choose which data to be plotted: ')
    listmulti.append(addline)
    addlinelabel = input('Input data label: ')
    listmultilabel.append(addlinelabel)
    print(listmulti)
    multi = input('Do you want to add more (Yes/No)? ')

#%% Ask for plotting many simulated data
listmultiSI = []
listmultilabelSI =[]
multiSI = input('Do you want to plot more simulated data (Yes/No)? ')
while multiSI == 'Yes':
    print(list(data))
    addlineSI = input('Choose which data to be plotted: ')
    listmultiSI.append(addlineSI)
    addlinelabelSI = input('Input data label: ')
    listmultilabelSI.append(addlinelabelSI)
    multiSI = input('Do you want to add more (Yes/No)? ')
    
#%%
# Change aspect ratop of graph
width = int(input('Change width aspect of the graph: '))
height = int(input('Change height aspect of the graph: '))

#%%
#Choose legend location:
print("Possible legend locations: best, upper left, upper right, lower left, lower right, right, center left, center right, lower center, upper center, center. ")
leglocation = input('Choose legend location: ')

legsize = int(input('Adjust legend box\'s size: ' ))

#Grid or not
grid = input('With or without grid (True/False): ')

#%%
#Export file name
name = input("Save file as: ")

#Choose file type and dpi values:
print("Available file type: jpg, png, svg.")
filetype = input('Choose export file type: ')
print("Recommended dpi values: 300, 600, 1200.")
dpi     = int(input('Choose desired dpi: '))

#%%
def make_time_series_graph():
    fig, ax = plt.subplots(figsize=(width,height))
    plt.plot(data[time],data[obdata], label = 'Observed data')
    if asksim == 'Yes':
        plt.scatter(data[time],data[simdata], s=2,c='r', marker='*',label = 'Simulated data')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.title(title)
    
    #plot more observed data
    for i,j in zip(listmulti, listmultilabel):
        plt.plot(data[time],data[i], label = j)
    
    #plot more simulated data
    for i,j in zip(listmultiSI, listmultilabelSI):
        plt.scatter(data[time],data[i], label = j, s=2, marker='*' )
    
    #three options for x axis: days or month/year or day/month/year
    if time == 'Days' and (len(data['Days']) > 730) == True:
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    if time == 'Datetime':    
        if Xaxisformat == 'Day/Month/Year':
            ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
            ax.xaxis.set_minor_locator(mdates.MonthLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        elif Xaxisformat == 'Year':
            ax.xaxis.set_major_locator(mdates.YearLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        
    
    #Set x limit by finding first and last date.
    #For pandas, last element accessed by .iloc[-1]
    ax.set_xlim([data[time][0],data[time].iloc[-1]])
             
    #Ensure that the plot is spaced evenly within the figure space.
    plt.tight_layout()
    #Print with grid
    plt.grid(grid)
    plt.legend(loc=leglocation, prop={'size':legsize})
    
    fig.savefig(name + '.' + filetype, format=filetype, dpi=dpi)
    
make_time_series_graph()


