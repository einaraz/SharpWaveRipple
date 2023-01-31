from glob import glob

# Define parameters -------------------------------
begin_time = 180                                         # [in sec] where to start analyzing time series
end_time = 480                                           # [in sec] where to stop analyzing time series
frequency = 1500                                         # [in Hz] frequency of data acquisition (points per second)
window_of_activity = 15                                  # [in mili seconds] duration of window of consecutive values above threshold
npoints_interval = (frequency*window_of_activity/1000)   # [-] number of points sampled in window_of_activity
threshold = 3                                            # [-] cutoff value above which windows of activity will be isolated
combine_groups = False                                   # if True, will combine consecutive windows separated by time_interval_groups seconds
time_interval_groups = 15/1000                           # [seconds] minimun time interval between two groups
outlier_threshold = 100000                               # Value above which measurements are considered outliers - intervals
                                                         #   that contain at least one value above outlier_threshold are deleted
filter_outliers_from_signal = False                      # if True, remove windows where the maximum value is above outlier_threshold, most
                                                         #   likely due to noisy data
plot_groups = False                                      # if True, it will open a figure for each file showing the original signal (z-scored) and all events
                                                         #   identified based on criteria - useful to first inspect the data and to help define the best parameters
# Obtain a list of all recordings ----------------------------   
all_mats = sorted(glob("InputData/*.mat"))     
