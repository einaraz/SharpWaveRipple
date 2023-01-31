# SharpWaveRipple

How to cite:

[![DOI](https://zenodo.org/badge/459619241.svg)](https://zenodo.org/badge/latestdoi/459619241)


# Overview
The provided script is used to detect sharp wave-ripple (SWR) events from in vivo electrophysiological recordings. The script enables detection of SWR time of initiation and culmination, total event number, peak amplitude, and integral. The script requires a single MATLAB file for each recording channel. Local field potential (LFP) recordings must be prefiltered depending on desired SWR frequency (i.e., 140-250 Hz). 

Users must supply the appropriate parameters of their recordings and desired experimental design to ensure successful SWR detection. Parameters include sampling frequency of the LFP recording (frequency), the desired SWR minimum duration (window_of_activity), the desired z-score cutoff for a detected event (threshold), and an optional z-score outlier threshold (outlier_threshold). The script enables users to select specific timepoints of their recordings to focus their analyses (begin_time; end_time). 

Upon completion, detected events are saved to two excel sheets titled 'SWRsummary.xlsx' and 'DetailedSWRsummary.xlsx'. 'SWRsummary.xlsx' contains averaged values for each recording (SWR number, duration, etc). 'DetailedSWRsummary.xlsx' provides information regarding each detected SWR event.

# System requirements

The SharpWaveRipple script requires a standard computer with enough RAM to support the operations defined by a user and enough hard-drive space to store the input datasets.

## OS Requirements
SharpWaveRipple is supported for Linux, macOS, and Windows. It was tested on the following systems:
- macOS: Monterey Version 12.0
- macOS: Catalina Version 10.15.5

## Python dependencies
SharpWaveRipple was written and tested with Python 3.9.7. It requires the following packages: 
```
- Numpy 1.22.4
- Scipy 1.7.1
- Pandas 1.3.4
- Matplotlib 3.4.3
```
# Installation guide
SharpWaveRipple does not need to be installed on the user's machine.

# Demo 

Sample data can be found in the folder InputData. The folder contains four MATLAB files containing recordings from mouse hippocampus. 
To run sample data, the user must first download the entire package. Open and run the main script SWRdetect.py in any python interface, such as Spyder, or call the application in the command lines as
```
python3 SWRdetect.py
```
This example should run in a few seconds on most machines. There will be two output files:
- DetailedSWRsummary.xlsx: contains a description of all events detected in each recording 
- SWRsummary.xlsx: contains a summary (averages) over all events for each recording

# Instructions for use

To run the script on your own data, first replace your own MATLAB files in InputData or create a new folder. All parameters needed for your analyses, including where your filed are located, should be editted in the file inputparameters.py. The main parameters are the following:

| Variable | Description |
| --- | ----------- |
| begin_time| [in sec] where to start analyzing time series |
| end_time | [in sec] where to stop analyzing time series |
| frequency | [in Hz] frequency of data acquisition (points per second) |
| window_of_activity| [in mili seconds] duration of window of consecutive values above threshold|
| threshold | [-] cutoff value above which windows of activity will be isolated |

Additional options are available and described in inputparameters.py. In addition, to help select the best parameters, the option plot_groups can be used. Enabling this feature opens a window showing the input time series. All detected events will be shown as demonstrated in the graphs belowbelow. Note that each MATLAB file will open its own window, and that windows will have to be closed manually.

![SWR](Fig1.png)
![SWR](Fig2.png)


