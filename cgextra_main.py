"""
load and analyze MUA raw traces
"""
import getpass
import os
import platform
import pickle

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
#import pandas as pd

import cgextra_meta as meta
import cgextra_format as reformat


def go_to_dir():
    """
    to go to the pg and file directory (spyder use)
    """
    osname = platform.system()
    username = getpass.getuser()
    if osname == 'Windows' and username == 'Benoît':
        os.chdir(r'D:\owncloud\cgFiguresSrc\elphyDataExport')        
    elif osname == 'Linux' and username == 'benoit':
        os.chdir(r'/media/benoit/data/travail/sourcecode/developing/'
                 +'paper/centriG')
    elif osname == 'Darwin' and username == 'cdesbois':
        os.chdir('/Users/cdesbois/ownCloud/cgFigures/elphyDataExport')
    return True
go_to_dir()

cwd = os.getcwd()
print(cwd)

#%% operating and save booleans
save_dat = False
save_fig = False
convert_mat = False
#%% const
# trials for each electrode per stim 
#vs no trials, only averages per electrodes per stim elem 1,2
files_list = ['PSTHS_TRIALS_2010_TUN21',             
              'PSTHS_2019_TUN21_with_top_synch',     
              'PSTHS_2019_TUN21_without_top_synch',  
              'psths_trials_2019_TUN_21_V2',         
              '1319_CXLEFT_TUN25_s30psths_trials']   

elecs_input = []
for i in range(65):
    if (i!= 0):
        elecs_input.append(i)
electrodes = [x - 1 for x in elecs_input]

cond_names = ['ctr_ls', 'son_ls',
              'stc_ls', 'ctr_hs', 
              'son_hs', 'stc_hs',
              'blk_ns']
cond_colors = ['black', 'green',
               'red', 'black',
               'green','red',
               'gray']

cond_labels = ['Center only low speed', 'Surround only low speed', 
               'Surround-then-Center low speed',' Center only high speed',
               'Surround only high speed', 'Surround-then-Center high speed',
               'Blank']

#%% get files specifications 
filename ='1319_CXLEFT_TUN25_s30psths_trials'

input_dat = loadmat(filename)
stimkey, eleckey, trialkey = meta.get_keys(filename, files_list)

blk_id = meta.get_condid(filename, files_list)
conditions = [1, 2, 3, 10, 11, 12, blk_id]

trialsn = meta.get_trials(filename, files_list)
trials = []
for j in range(trialsn + 1):
    if j != 0:
        trials.append(j)

layers = []
layer_lims = meta.get_layers(filename, files_list)
layers.append(layer_lims)        

ylims = []
ylims_val =  meta.get_yscale(filename, files_list)
ylims.append(ylims_val)
#%% from .mat to dict

if convert_mat:
    #data_dict = reformat.average_to_dict(input_dat, conditions,
    #                                     elecs_input) 
    data_dict = reformat.trials_to_dict(input_dat, conditions, 
                                        elecs_input, trials,
                                        stimkey, eleckey, trialkey) 
#suppress n-1 sized dimensions
if (filename in files_list[1]) or (filename in files_list[2]):
    for cond in conditions:
        data_dict[cond] = np.squeeze(data_dict[cond])

#load and save dict
pickle_in = open(filename+".pickle","rb")
data_dict = pickle.load(pickle_in)

# export dict as pickle
if save_dat:
    pickle_out = open(filename +".pickle", "wb")
    pickle.dump(data_dict, pickle_out)
    pickle_out.close()

#%% check reformated_dict keys/dimensions
#print(input_dat.keys())
#print(data_dict.keys())

print( 'keys are of type:   ' + stimkey + '   ' + eleckey + '   ' + trialkey)
print ('there are' + '   ' + str(trialsn) + '    ' + 'trials' )

print('Each condition is of type (electrodes, trials, len(vector) in points)')
print(np.shape(data_dict[1]))
print(' ')
print(np.shape(data_dict[1][1]))
# up to trial dimension
if (filename in files_list[0]) or (filename in files_list[3]) or \
    (filename in files_list[4]):
        print(np.shape(data_dict[1][1][1]))

#%% from dict to df
df = reformat.dict_to_df(data_dict, conditions, cond_names, electrodes,
                         filename, files_list)
#%% from df to list of matrices
matlist, dim = reformat.df_to_matL(df, conditions, cond_names)
#%%  
"""
plot 64 electrodes, squeezed over the 30 trial dimension or not 
to replicate average MUA traces
"""
# TODO : load and plot top synchro data

fig, axes = plt.subplots(figsize=(17.6, 12), nrows=len(electrodes), ncols= 1,
                         sharex= True, sharey = True)
axes = axes.flatten()
for j in electrodes:
    axes[j].plot(df[cond_names[6]][j], color=cond_colors[6], alpha=0.8,
                 label=cond_names[6])
   
    axes[j].plot(df[cond_names[0]][j], color=cond_colors[0], alpha=0.8,
                label=cond_names[0])
   
    axes[63].set_xlim(dim/2, dim-1 - dim/6)
    #axes[63].set_xlim(0, 1200)
    #axes[63].set_ylim(0,files_props[file_idx][1])
    
    for ax in fig.get_axes():
        for loc in ['bottom','top', 'left','right']:
            ax.spines[loc].set_visible(False)
        ax.yaxis.set_visible(False)
        ax.xaxis.set_visible(False)
    rect = 0.125, 0.095, 0.775, 0.01
    axesX= fig.add_axes(rect, sharex = axes[63], label='tref')
   
    for loc in ['top', 'left', 'right']:
        axesX.spines[loc].set_visible(False)
        axesX.xaxis.set_visible(False)
        axesX.yaxis.set_visible(False)
    for loc in ['bottom']:
        axesX.spines[loc].set_visible(True)
        axesX.xaxis.set_visible(True)
        axesX.set_xlabel('Time (ms)')
    #plt.axvline(-25, 1, 64 )
    #fig.tight_layout()
    # remove the space between plots
    #fig.subplots_adjust(hspace=0.01)
#%%  matrices plot

fig, axes = plt.subplots(figsize = (14, 7), nrows = 2, ncols = 3, 
                         sharex=True, sharey = True )
axes.flatten()
for n in range(len(conditions)-1):
    if n <= 2:
                
        axes[0,n].matshow(matlist[n], cmap='jet', vmin=0,
                          vmax=ylims[0], interpolation='gaussian')
        
        axes[0,n].set_xlim(dim/1.8, dim-1 - dim/4)    
        #axes[0,n].set_xlim(775, 1000)    
        
        axes[0,n].tick_params(axis ='x', bottom =True, top=False, 
                              labelbottom=True, labeltop =False)
        axes[0,n].tick_params(axis ='y', left=True, right=False, 
                              labelleft=True, labelright =False)
        axes[0,0].set_ylabel(' Depth (electrode)')
        
        axes[0,n].set_title(cond_labels[n], color = cond_colors[n])
        axes[0,n].axhline(layers[0][0], 0,1, color='white')
        axes[0,n].axhline(layers[0][1], 0,1, color='white')
        
    elif n > 2:
        axes[1,n-3].matshow(matlist[n], cmap='jet', vmin=0,
                            vmax= ylims[0], interpolation='gaussian')
        axes[1,n-3].tick_params(axis ='x', bottom=True, top=False,
                                labelbottom=True, labeltop =False)
        axes[1,n-3].tick_params(axis ='y', left=True, right=False, 
                                labelleft=True, labelright =False)
        axes[1,0].set_ylabel(' Depth (electrode)')
        
        axes[1,n-3].set_title(cond_labels[n], color = cond_colors[n])
        axes[1,n-3].axhline(layers[0][0], 0,1,color='white')
        axes[1,n-3].axhline(layers[0][1], 0,1,color='white')
        axes[1,n-3].set_xlabel(' Time (ms)')
        
fig.suptitle(filename)# + ' 1 ms subsampled', size = 16)                       
fig.tight_layout()
