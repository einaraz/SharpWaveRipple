# SharpWaveRipple

How to cite:

[![DOI](https://zenodo.org/badge/459619241.svg)](https://zenodo.org/badge/latestdoi/459619241)


# Overview
The provided code is used to detect sharp wave-ripple (SWR) events from in vivo electrophysiological recordings. The code enables detection of SWR time of initiation and culmination, total number, peak amplitude, and integral. The code requires a single MATLAB file for each individual recording. Local field potential (LFP) signal must be prefiltered depending on desired SWR frequency (i.e., 140-250 Hz). The code enables users to select specific timepoints of their recordings to focus their analyses (begin_time; end_time). 


Users must supply the appropriate parameters of their recordings and desired experimental design to ensure successful SWR detection. Parameters include sampling frequency of the LFP recording (frequency), the desired SWR minimum duration (window_of_activity), the desired z-score cutoff for a detected event (threshold), and an optional z-score outlier threshold (outlier_threshold). 


Upon completion, detected events are saved to two excel sheets titled 'SWRsummary.xlsx' and 'DetailedSWRsummary.xlsx'. 'SWRsummary.xlsx' contains averaged values for each recording (SWR number, duration, etc). 'DetailedSWRsummary.xlsx' provides information regarding each detected SWR event.

# System requirements

The script SharpWaveRipple requires only a standard computer with enough RAM to support the operations defined by a user and enough hard-drive space to store the input datasets.

## OS Requirements
SharpWaveRipple is supported for Linux, macOS, and Windows.

## Python dependencies
SharpWaveRipple was written and tested with Python 3.9.7. It requires the following packages 
```
- Numpy 1.22.4
- Scipy 1.7.1
- Pandas 1.3.4
- Matplotlib 3.4.3
```
# Installation guide
SharpWaveRipple does not need to be installed in the use's machine.

# Demo 

The only required input data to run the code can be found in the folder InputData. It contains four matlab files containing hippocampus recordings. 
To run this example, first download the entire package. Open and run the main script SWRdetect.py in any python interface, such as Spyder, or call the application in the command lines as
```
python3 SWRdetect.py
```
This example should run in a few seconds in most machines. There will be two output files
- DetailedSWRsummary.xlsx: contains a description of all events detected in each recording 
- SWRsummary.xlsx: contains a summary (averages) over all events for each recording

# Instructions for use

To run the script on your own data, first replace your own matlab files in InputData or create a new folder. The main parameters of your analyses need to be modified in the script.
