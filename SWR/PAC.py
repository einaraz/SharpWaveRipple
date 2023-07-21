import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
import pandas as pd
from glob import glob
from pprint import pprint
import matplotlib as mpl
import random
import os
import sys
import math

params = {'font.size': 18, 'font.family': 'serif', 'xtick.major.pad': '1'}
mpl.rcParams.update(params)
mpl.rcParams['figure.figsize'] = 8,6
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 14
mpl.rcParams['axes.axisbelow'] = True

"""
There are two files for each recording
    Ex.: nex_773_c_e_dark_e1_theta.mat and nex_773_c_e_dark_e1_gamma.mat

Theta files: Only last column is of interest
Gamma files: Only fourth column is of interest

Combine these two columns in a dataframe
"""

# ---------------------------------------------------------------------
# Edit options below --------------------------------------------------
t_initial     = 210      # s
t_final       = 480      # s
matfiles_path = "Theta_phase_gamma_files/"       # Folder where .mat files are located. ex: "matFiles/files/"
save_plot     = False                            # if True: it will save the figure; if False, it will not create
path_plot     = 'PlotsPAC'                       # Folder where figure will be saved to; make sure to create the folder before running the code

# ---------------------------------------------------------------------
# Checking if folders and files exist ---------------------------------
if save_plot:
    if os.path.isdir(path_plot):
        pass
    else:
        print("Folder path_plot=%s does not exist. Please specify a folder for figures"%path_plot)
        sys.exit()

mats = sorted(glob("%s*.mat"%matfiles_path))   # Read all .mat files
if len(mats) == 0:
    print("No matlab files where found in folder %s. Please check where files are located."%matfiles_path)
    sys.exit()

list_mats = []

for mt in mats:
    if "theta" in mt:
        list_mats.append(mt.replace("theta.mat", ""))

# Separete the data according to type of experiment
drug        = ['Veh', 'CNO' ]
conditionst = ['ytv', 'ytb', 'ztv', 'ztb' ]
all_mats    = []

for dr in drug:
    for cond in conditionst:
        aux_cond = [ ci for ci in list_mats if dr in ci and cond in ci]
        all_mats = all_mats + aux_cond

conditionsu = ['yuv',  'yub',  'zuv', 'zub']
for dr in drug:
    for cond in conditionsu:
        aux_cond = [ ci for ci in list_mats if dr in ci and cond in ci]
        all_mats = all_mats + aux_cond

# Reading data ---------------------------------------------------------

# Create a list of intervals 
lista     = np.linspace(-1, 1, 21)
lista[0]  = lista[0]  - 0.1
lista[-1] = lista[-1] + 0.1

all_amplitude = {}
all_theta     = {}
headers       = []


for jm,matfile0 in enumerate(all_mats):
#    if jm == 62: continue  # veh 587 w 437 3
    print("%d/%d"%(jm,len(list_mats)), matfile0 )
    matfile    = matfile0.split("/")[-1]
    headers.append(matfile)
    
    # prepare file name -------------------------------
    theta_file = "%stheta.mat"%matfile0  # Names of the .mat files
    gamma_file = "%sHgamma.mat"%matfile0  # Names of the .mat files
    theta_name = "%stheta"%matfile       # dictionary key after reading the files
    gamma_name = "%sgamma"%matfile       # dictionary key after reading the files

    # read mats ---------------------------------------
    load_gamma = loadmat(gamma_file)['DATA'].T
    load_theta = loadmat(theta_file)['DATA'].T

    theta      = load_theta[-1]
    gamma      = load_gamma[-2]
    times      = load_gamma[0]
    
    # Create dataframe --------------------------------
    df_aux = pd.DataFrame( {'theta': theta/np.pi,  'gamma': gamma }, index=times)
    del theta, gamma, times
    
    # Select time frame -------------------------------
    df = df_aux[(df_aux.index>=t_initial)&(df_aux.index<=t_final)].copy()
    del df_aux
    
    # Binning data ------------------------------------
    Ts, As        = [], []
    mean_theta    = []
    for i in range(20):
        aux      = df[(df['theta']>=lista[i])&(df['theta']<lista[i+1])]
        aux_mean = aux.mean()
        Ts.append(aux_mean['theta'])
        As.append(aux_mean['gamma'])
        mean_theta.append( aux_mean['theta'] )
        del aux
        
    # Save as array -----------------------------------
    Ts = np.array(Ts); 
    As = np.array(As); As = As/np.sum(As)
    all_amplitude[matfile] = As
    all_theta[matfile]     = Ts
    
    if save_plot:
        # plot --------------------------------------------
        fig = plt.figure()
        ax  = fig.gca()
        ax.fill_between( Ts, As - np.std(As), As + np.std(As), color="blue", alpha=0.5 )
        ax.plot( Ts, As, marker='o', color="black" )
        ax.grid()
        ax.set_title(matfile[:-1])
        ax.set_xlabel(r"Theta phase ($\pi$ radians)")
        ax.set_ylabel("Gamma amplitude")
        plt.savefig("%s/%s.png"%(path_plot,matfile[:-1]))
        # ~ plt.show()
        plt.close(fig)
    del df, As

# Saving data ---------------------------------------------------
final_data_gamma       = pd.DataFrame( all_amplitude )
final_data_gamma.index = mean_theta
cols                   = list(final_data_gamma.columns)

# find maximum and minimums
summary_maxmin = { 'max_gamma': [],
                   'min_gamma': [],
                   'max_theta': [],
                   'min_theta': []}

aux_max = final_data_gamma[final_data_gamma.index>0].copy()
aux_min = final_data_gamma[final_data_gamma.index<0].copy()

for cl in cols:
    max_gamma_value =  aux_max[cl].max()
    min_gamma_value =  aux_min[cl].min()
    max_theta_value =  aux_max[cl].idxmax()
    min_theta_value =  aux_min[cl].idxmin()

    summary_maxmin['max_gamma'].append(max_gamma_value)
    summary_maxmin['min_gamma'].append(min_gamma_value)
    summary_maxmin['max_theta'].append(max_theta_value)
    summary_maxmin['min_theta'].append(min_theta_value)

del aux_max, aux_min
max_min  = pd.DataFrame.from_dict(summary_maxmin, orient='index', columns=cols)

# Compute MI
final_data_gamma_MI = -final_data_gamma * final_data_gamma.applymap(math.log10)
final_data_gamma_MI = final_data_gamma_MI.sum()
DKL                 = np.log10(20) - final_data_gamma_MI
MI                  = DKL / np.log10(20)

# Writing excel file --------------------------------------------------------
writer = pd.ExcelWriter("MSEW_PAC_gamma_divide_sum.xlsx", engine='xlsxwriter')
final_data_gamma = pd.concat([final_data_gamma, max_min])
final_data_gamma.to_excel( writer, sheet_name='BinnedData', columns=headers)
MI.to_excel( writer, sheet_name='MI', header=['MI'], index_label='experiment')
writer.save()
