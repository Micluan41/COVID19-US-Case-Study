import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def state_df(df, state):
    
    #select the time-series covid data for a certain state as df_state
    #df is the time-series covid dataframe with columns ['submission_date','state','tot_cases','new_cases','tot_death','new_death']
    #state is the state abbreviation to be extracted
    #return df_state with only data from state and drop 'state' column, reset 'submission_date' as index and sort by the date
    
    df_state=df[df['state']==state]
    df_state=df_state.drop(columns=['state'])
    df_state=df_state.set_index('submission_date')
    df_state=df_state.sort_index()
    
    return df_state

def moving_avg(data, window):
    
    #calculate the mean value in a backward window as the current value
    #data is np.array; window is the window size for average
    #return the moving average as data_avg
    
    data_avg=[]
    for i in range(len(data)):
        if i>len(data)-window:
            data_avg.append(np.mean(data[i:]))
        else:
            data_avg.append(np.mean(data[i:i+window]))
            
    return np.array(data_avg)

def moving_avg_df(df, window):
    
    #calculate the mean value in a backward window for each column in a dataframe
    #df is a dataframe; window is the window size for average
    #return the moving average as df_avg
    df_avg=df.copy()
    for col in df.columns.values:
        df_avg[col]=moving_avg(df[col],window)
        
    return df_avg
    
def Comb_neighbor(df_list, var, neighbor):
    
    #combine the 'var' column of each dataframe from df_list, rename the var with respective state in neighbor
    #df_list is a list of dataframe,i.e [covid_sc,covid_nc]
    #var is the column name of covid dataframe to combine
    #neighbor is a list of state abbreviation, has the same size as df_list
    #return dataframe neighbor_var
    series=[]
    for df in df_list:
        series.append(df[var])
        
    covid_var=pd.concat(series, axis=1)
    covid_var.columns=neighbor
    
    return covid_var

def plot_multiple(x, Y, var):
    
    #plot multiple lines in one plot
    #x is the common time-series
    #Y is the dataframe that contains information of a list of states
    #var is the covid-related variable to plot 
    
    plt.figure(figsize=(8, 5))
    for i in range(len(Y.columns.values)):
        plt.plot(x, Y.iloc[:,i])

    plt.title('%s for a few states' %var, size=12)
    plt.xlabel('Days Since 1/22/2020', size=10)
    plt.ylabel('# of %s' %var, size=10)
    plt.xticks(size=10)
    plt.yticks(size=10)
    
def plot_fit(x, y, X, Fit, legends):
    
    #plot the actual time-series data with fitting (multi-stage)
    #x is the full time span, y is the actual data
    #X is a list of the time segment, Fit is the list of fitting results of each stage
    #var is the content of data; legend contains legend for original data, fitting method and future prediction  
    
    var=legends[0]
    plt.figure(figsize=(12, 8))
    lines=[]
    lines+=plt.plot(x,y)
    for i in range(len(X)-1):
        lines+=plt.plot(X[i], Fit[i], 'r--')
    lines+=plt.plot(X[-1], Fit[-1], 'k--', label=legends[-1])
    plt.title('US COVID %s Over Time' %var, size=20)
    plt.xlabel('Days Since 1/22/2020', size=15)
    plt.ylabel( '# of %s' %var, size=15)
    plt.legend([lines[0], lines[1], lines[-1]], legends, prop={'size':10})
    plt.xticks(size=10)
    plt.yticks(size=10)
    
    