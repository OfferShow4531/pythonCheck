#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import matplotlib.patches as mpl_patches

#%%
#Read CSV file in the folder
data = pd.read_csv('chart1.csv')

data.to_csv('new_chart.csv', index=False)

print(type(max(data['Observed'])))

#%%
#Get to know header names:
print(list(data))

#Choose x and y axis depending on the headers
xaxis  = input('Choose x axis: ')
xlabel = input('Input x axis label: ')

yaxis = input('Choose y axis: ')
ylabel = input('Input y axis label: ')

#Input title
title = input('Input plots\'s title: ')

#Choose show trendline or not
trendline = input('Do you want to plot the trendline (Yes/No)?: ')

#%%
# Change aspect ratop of graph
width = int(input('Change width aspect of the graph: '))
height = int(input('Change height aspect of the graph: '))

grid = input('With or without grid (True/False): ')

#%%
#Export file name
name = input("Save file as: ")

#Choose file type and dpi values:
print("Available file type: jpg, png, svg.")
filetype= input('Choose export file type: ')

print("Recommended dpi values: 300, 600, 1200.")
dpi     = int(input('Choose desired dpi: '))

#%%
def make_scatter_plot():
    fig, ax = plt.subplots(figsize=(width,height))
    plt.scatter(data[xaxis],data[yaxis], s=2, c='r', marker='*')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.grid(grid)
    
    #Add trendline if Yes
    if trendline == 'Yes':
        z = np.polyfit(data[xaxis], data[yaxis], 1)
        p = np.poly1d(z)
        
        #Calculate linear equation by scipy
        slope, intercept, r_value, p_value, std_err = sp.stats.linregress(data['Observed'], data['Simulated'])
        r = r_value**2
        
        plt.plot(data[xaxis],p(data[xaxis]),"k-")
        if z[1] >= 0: 
            #positioning trendline equation

            # create a list with two empty handles (or more if needed)
            handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", 
                                             lw=0, alpha=0)] * 2

            # create the corresponding number of labels (= the text you want to display)
            labels = []
            labels.append('$y=%.3fx%.3f$'%(z[0],z[1]))
            labels.append('$R^{2}$ = ' + str('%.5f'%(r)))

            # create the legend, supressing the blank space of the empty line symbol and the
            # padding between symbol and label by setting handlelenght and handletextpad
            plt.legend(handles, labels, loc='best', fontsize='small', 
                      fancybox=True, framealpha=0.7, 
                      handlelength=0, handletextpad=0)
        elif z[1] < 0: #just to make the equation "prettier" if b is negative
            #positioning trendline equation

            # create a list with two empty handles (or more if needed)
            handles = [mpl_patches.Rectangle((0, 0), 1, 1, fc="white", ec="white", 
                                             lw=0, alpha=0)] * 2

            # create the corresponding number of labels (= the text you want to display)
            labels = []
            labels.append('$y=%.3fx%.3f$'%(z[0],z[1]))
            labels.append('$R^{2}$ = ' + str('%.5f'%(r)))

            # create the legend, supressing the blank space of the empty line symbol and the
            # padding between symbol and label by setting handlelenght and handletextpad
            plt.legend(handles, labels, loc='best', fontsize='small', 
                      fancybox=True, framealpha=0.7, 
                      handlelength=0, handletextpad=0)
        
    fig.savefig(name + '.' + filetype, format=filetype, dpi=dpi)
    
make_scatter_plot()
