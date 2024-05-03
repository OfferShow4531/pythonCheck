#%%
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

#%%
#Read CSV file in the folder
data = pd.read_csv('chart.csv')

#Change timeStampt to datetime data
date = pd.to_datetime(data['timeStamp'] ,unit='s')

#Add datetime data as new column in the csv file
data['Datetime']=date

#Add the number of days as new column
data['Days'] = np.arange(len(data))

#Re-arrange column order based on the order of columnsTitles list
columnsTitles = ['timeStamp', 'Days', 'Datetime', 'value','clone']
data = data.reindex(columns=columnsTitles)

#Create new csv file and add data
data.to_csv('new_chart.csv', index=False)

#%%
#Get to know header names:
print(list(data))

#Choose x and y axis depending on the headers
time    = input('Choose x axis: ')

#%%
if time == 'Datetime':
    print('Available x axis format: Day/Month/Year, Year.')
    Xaxisformat = input('Choose x axis format: ')
#%%
print(type(len(data['Datetime'])))
#%%
xlabel  = input('Input x axis label: ')

obdata  = input('Choose y data for observation: ')

simdata = input('Choose y data for simulation: ')

asksim  = input('Do you want to display simmulated data also (Yes/No)? ')
    
ylabel  = input('Input y axis label: ')

title = input('Input graph title: ')
#%%
#Choose legend location:
print("Possible legend locations: best, upper left, upper right, lower left, lower right, right, center left, center right, lower center, upper center, center. ")
leglocation = input('Choose legend location: ')

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
    fig, ax = plt.subplots()
    plt.plot(data[time],data[obdata], label = 'Observed data')
    if asksim == 'Yes':
        plt.scatter(data[time],data[simdata], s=2,c='r', marker='*', label = 'Simulated data')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc=leglocation)
    plt.title(title)
    
    #three options for x axis: days or month/year or day/month/year
    if time == 'Days' and len(data[time]) > 730:
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    elif Xaxisformat == 'Day/Month/Year':
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    elif Xaxisformat == 'Year':
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        
    
    #Set x limit by finding first and last date.
    #For pandas, last element accessed by .iloc[-1]
    ax.set_xlim([data[time][0],data[time].iloc[-1]])
    
    #maxvaly=data[[obdata,simdata]].max(axis=1).max(axis=0)
    #minvaly=data[[obdata,simdata]].min(axis=1).min(axis=0)
    #ax.set_ylim([minvaly,maxvaly])               
    #Ensure that the plot is spaced evenly within the figure space.
    plt.tight_layout()
    #Print with grid
    plt.grid(grid)
    
    fig.savefig(name + '.' + filetype, format=filetype, dpi=dpi)
    
make_time_series_graph()
