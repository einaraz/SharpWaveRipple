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
# Input data information --------------------------
path_to_data  = "InputData"                              # path to the matlab files
all_mats      = sorted(glob("%s/*.mat"%path_to_data))    # creates a list of all available matlab files (requires extension *.mat)
ncol_time     = 0                                        # column where the timestamp is located in the matlab file 
                                                         #   notice that python indexing starts at zero; thus, first and second column are numbers 0 and 1, respectively
ncol_sinal    = 3                                        # column where filtered signal is located in the matlab file (notice that python indexing starts at zero)

# Optional (example) ---------------------------------------------------

# Organize files in specific order for ease of analysis
# Use the code below to organize the order in which files will be processed (useful to group results following a pattern)
# The script permits three coded letters to be added at the end of a matlab file name (First letter: "y" or "z", Second letter: "t" or "u", Third letter: "v" or "b")
# The the code can be used to represent different groups.
# For example, a matlab file ending in ytv could represent genotype "y", virus "t", and sex "v".
# See file names in InputData for an example of how to name files.
# Using this code will organize all of your data in the output excel file to ease data analysis

"""
drug        = ['Veh', 'CNO']
conditionst = ['ytv', 'ytb', 'ztv', 'ztb' ]
all_mats0   = list(all_mats)
all_mats    = []
for dr in drug:
    for cond in conditionst:
        aux_cond = [ ci for ci in all_mats0 if dr in ci and cond in ci]
        all_mats = all_mats + aux_cond

conditionsu = ['yuv',  'yub',  'zuv', 'zub']
for dr in drug:
    for cond in conditionsu:
        aux_cond = [ ci for ci in all_mats0 if dr in ci and cond in ci]
        all_mats = all_mats + aux_cond
"""
