import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
import pandas as pd
from glob import glob
from pprint import pprint
import matplotlib as mpl
import time

pd.options.mode.chained_assignment = None  # default='warn'

def DetectIntervalsSWR(data, threshold, number_points, time_consec_groups, outlier, plot_groups=False):
    """
    """
    # Z-score the data and create a copy of the dataframe -----------------------------
    data['signal_zscore'] = (data['signal'] - data['signal'].mean())/data['signal'].std()
    data_original         = data.copy()
    data_original['id']   = np.arange(data.index.size)
    size_data             = data_original.index.size
    # Identify periods when the signal is above the threshold -------------------------
    data['above']   = data['signal_zscore'] > threshold
    # Count how many values there are in windows above threshold ----------------------
    data['consecu'] = data['above'].groupby(( data['above'] != data['above'].shift()).cumsum()).transform('size') * data['above']
    # Give an individual ID for all windows of consecutive points ---------------------
    data['above'] = 1 - data['above']
    data['groups'] = data['above'].cumsum()
    # Remove groups with few elements -------------------------------------------------
    data['consec_new'] = data['groups'].copy()
    data['consec_new'][data['consecu']<number_points] = 0  
    data['id'] = data_original['id'].copy()
    data = data[data['consec_new']>0]
    groups = data.groupby(data['groups']) #.agg(['mean', 'count'])

    # Plot figure ------------------------------------------------------
    # ------------------------------------------------------------------
    if plot_groups:
        fig = plt.figure(figsize=(8, 4))
        ax = fig.gca()
        ax.plot( data_original.index, data_original['signal_zscore'], color='black', linewidth=1.0)
        ax.axhline(threshold, color='blue', linestyle='--')
        ax.axhline(0,         color='blue', linestyle='--')
        ax.set_ylabel("Z-scored signal")
        ax.set_xlabel("Time (seconds)")
        ax.set_axisbelow(True)
        ax.yaxis.grid(color='gray', linestyle='dashed')
        ax.xaxis.grid(color='gray', linestyle='dashed')

    # ------------------------------------------------------------------
    # Check all groups -------------------------------------------------
    # Find first and last values crossing zero
    # Compute statistics for all windows
    # Check if windows overlap
    # Plot if plot_groups = True
    
    df_windows = []
    last_included_index = 0

    for k,v in groups:
        i0 = v['id'].values[0]   # First index of group (from original dataframe)
        i1 = v['id'].values[-1]  # Last  index of group (from original dataframe)
        i00, i11 = 'none','none'
        
        # Check to see if this group was accounted for (included in las group)
        if last_included_index >= i0:
            continue

        # Loop backwards: find last time step when a value below zero was reported
        for i in range(i0, -1, -1):
           if data_original['signal_zscore'].iloc[i] >= 0: i00 = i
           else: break
        
        # Find next time a negative value was observed
        for i in range(i1, size_data):
            if data_original['signal_zscore'].iloc[i] >=0: i11 = i
            else: break
                
        if i00=='none' and i11=='none': continue
        if i00=='none' or i11=='none':
            print("Just one index is none: ii1 = %s, ii2 = %s"%(ii0, ii1))
        
        # Define new group, new including values before and after crossing zero
        new_v = data_original.iloc[i00:(i11+1)]
        if new_v['signal_zscore'].max() > outlier:
            continue

        # Save the last index for next iteration ------------------------------
        last_included_index  = i11
        last_time_stamp      = new_v.index[-1]
        # Compute the time interval between this window and the previous ------
        #  If time window is smaller than time_consec_groups
        time_from_last_event = 0
        if len(df_windows) > 0:
            time_from_last_event = last_time_stamp - df_windows[-1]['final_time']

        # ---------------------------------------------------------------------
        # Computing statistics ------------------------------------------------

        # Integral under the curve
        integrated_signal = np.trapz(y=new_v['signal_zscore'].values, x=new_v['signal_zscore'].index)
        # Maximum value of interval
        max_value_window  = new_v['signal_zscore'].max()
        # first and last time step
        t0, tf = new_v.index[0], new_v.index[-1]
        # duration of interval
        time_interval = tf - t0
        # Check if intervals overlap
        stats_window = { 'integral': integrated_signal,
                         'peak_of_interval': max_value_window,
                         'initial_time': t0,
                         'final_time': tf,
                         'duration_seconds': time_interval }
        if (time_from_last_event > time_consec_groups) or (len(df_windows)==0):
            df_windows.append(stats_window)
            new_v_plot = new_v.copy()
        else:
            df_windows[-1]['integral']         += stats_window['integral']
            df_windows[-1]['peak_of_interval']  = max( df_windows[-1]['peak_of_interval'], stats_window['peak_of_interval'] )
            df_windows[-1]['final_time']        = stats_window['final_time']
            df_windows[-1]['duration_seconds']  = stats_window['final_time'] - df_windows[-1]['initial_time']
            new_v_plot = data_original.iloc[df_windows[-1]['initial_time']:stats_window['final_time']]
    
        if plot_groups: ax.plot(new_v_plot.index, new_v_plot['signal_zscore'], marker='x', markersize=2)
    if plot_groups: plt.show()
    return pd.DataFrame(df_windows, index=(np.arange(len(df_windows))+1) )

# Define parameters -------------------------------
begin_time = 180                                         # [in sec] where to start analyzing time series
end_time = 480                                           # [in sec] where to stop analyzing time series
frequency = 1500                                         # [in Hz] frequency of data acquisition (points per second)
window_of_activity = 15                                  # [in mili seconds] duration of window of consecutive values above threshold
npoints_interval = (frequency*window_of_activity/1000)   # [-] number of points sampled in window_of_activity
threshold = 3                                            # [-] cutoff value above which windows of activity will be isolated
time_interval_groups = 15/1000                           # [in mili seconds] min time interval between two groups
outlier_threshold = 100000                               # Value above which measurements are considered outliers - intervals
                                                         #   that contain at least one value above outlier_threshold are deleted

# Open files and lists ----------------------------
all_mats0 = sorted(glob("SWR_all/*.mat"))     
print(len(all_mats0))

# Organize files ----------------------------------
drug       = ['Sal', 'CNO']
conditions = ['ytv', 'yuv', 'ytb', 'yub', 'ztv', 'zuv', 'ztb', 'zub']
all_mats   = []

for dr in drug:
    for cond in conditions:
        aux_cond = [ ci for ci in all_mats0 if dr in ci and cond in ci]
        all_mats = all_mats + aux_cond

                                 # read all files from folder
stats_all_excel = pd.ExcelWriter('DetailedSWRsummary.xlsx')
SWR_averages = {'number_SWR': [], 'average_integral': [], 'average_peak': [], 'average_duration': []}
tests_list = []

# Find all .mat files -----------------------------
for tt,swr_file in enumerate(all_mats):
    # read mats ---------------------------------------
    # time is the first column [index 0 in python]
    # signal of interest is the fourth column [index 3 in python]
    print("File %s, %d/%d"%(swr_file, tt+1, len(all_mats) ))
    test = swr_file.split("/")[-1].split(".")[0].replace('rerecord', 're')
    data = loadmat(swr_file)['DATA'].T
    df = pd.DataFrame({'signal': data[3]}, index=data[0])          # Create a pandas dataframe
    df = df[(df.index>=begin_time)&(df.index<=end_time)]           # Select only time interval of interest
    del data

    # Find intervals ----------------------------------
    # Steps
    #    1 - z-score the data
    #    2 - identify all windows with a duration of time in seconds miliseconds defined by window_of_activity above a threshold defined by threshold
    #    3 - for each window, find first an last values when the z-scored signal was above zero
    #        3a - consecutive flagged windows separated by less than 'window_of_activity' will be combined 
    #    4 - compute statistics for these windows
    SWR = DetectIntervalsSWR( data=df, threshold=threshold, number_points = npoints_interval, time_consec_groups = time_interval_groups, outlier = outlier_threshold, plot_groups=False)  

    # Average of events ------------------------------------------------
    SWR_averages['number_SWR'].append(SWR.index.size)
    if SWR.index.size > 0:
        SWR_means = SWR.mean()
        SWR_averages['average_integral'].append(SWR_means['integral'])
        SWR_averages['average_peak'].append(SWR_means['peak_of_interval'])
        SWR_averages['average_duration'].append(SWR_means['duration_seconds'])
    else:
        SWR_averages['average_integral'].append(0)
        SWR_averages['average_peak'].append(0)
        SWR_averages['average_duration'].append(0)
    tests_list.append(test)
    # Write statistics of test to excel ---------------
    SWR.to_excel( stats_all_excel, test)
    
# Close excel spreadsheet
stats_all_excel.save()

# Write the averages ---------------------------------------------------
SWR_averages = pd.DataFrame( SWR_averages, index=tests_list)
average_series = pd.ExcelWriter('SWRsummary.xlsx')
SWR_averages.to_excel( average_series, "SWR summary")
average_series.save()