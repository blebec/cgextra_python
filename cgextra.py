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
import pandas as pd
#import humps

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

#%% turn .mat to dict
"""
each key is of type: PSTH_STIM_n1_ELEC_n2_TRIAL_n3
#stims of interest: 
#1: ctr_ls, 2:son_ls, 3: stc_ls, 10 = ctr_hs, 11: son_hs; 12: stc_hs, 19: blk
# n1 stim = 7 of interest, n2 electrode = 64, n3 trial = 30
"""
def trials_to_dict(dat, conds, elecs, trials):
    """
    returns a dictionary with keys corresponding to [conditions,electrodes]
    At the level of [conditions], each element in an array of array where
    each element is of of shape [nelec][ntrials][npoints]
    At the level of [conditions][elec], each element is an array where 
    each elecment is of shape [ntrials][npoints]
    """
    
    for key in dat:
        if (key not in ['__header__', '__version__', 
                        '__globals__', 'DataFile']):
            reformated_data = {}
            
            for cond in conds:
                reformated_data[cond] = []
                for elec in elecs:
                    reformated_data[cond, elec] = []
                    for trial in trials:
                        
                        if ('Stim' + str(cond) +'Elec%dRepet%d' % (elec, trial) in dat):
                            reformated_data[cond, elec].append(np.array(dat['Stim' + str(cond) + 'Elec%dRepet%d' % (elec,trial)]).flatten())                 
                        #if ('PSTH_STIM_' + str(int(cond)) +'_ELEC_%d_TRIAL_%d' #    % (elec, trial) in dat):
                            #(np.array(dat['PSTH_STIM_' + str(int(cond)) + '_ELEC_%d_TRIAL_%d' % (elec,trial)]).flatten()) 
                                                                          
                    reformated_data[cond, elec] = np.array(reformated_data[cond, elec])
                    reformated_data[cond].append(reformated_data[cond, elec])                
                    
                    
                #reformated_data[cond] = np.array(reformated_data[cond])
            reformated_data[cond] = np.array(reformated_data[cond])
    return reformated_data        


#each key is of type: PSTH_STIM_n1_ELEC_n2
def average_to_dict(dat, conds, elecs):
    """
    returns a dictionary with keys corresponding to [conditions,electrodes]
    At the level of [conditions], each element in an array where
    each element is of of shape [nelec][npoints]
    At the level of [conditions][elec], each element is a 1d array where 
    each elecment is of shape [npoints]
    """
    
    for key in dat:
        if (key not in ['__header__', '__version__',
                        '__globals__', 'DataFile']):
            reformated_data = {}
            
            for cond in conds:
                reformated_data[cond] = []
                for elec in elecs:
                    reformated_data[cond, elec] = []
                    if ('PSTH_' + str(int(cond)) + '_%d' % (elec) in dat):
                        reformated_data[cond, elec].append(np.array(dat['PSTH_' + str(int(cond))+ '_%d' % (elec)]).flatten()) 
                          
                    reformated_data[cond, elec] = np.array(reformated_data[cond, elec])
                    reformated_data[cond].append(reformated_data[cond, elec])                
            reformated_data = np.array(reformated_data)
            reformated_data = np.squeeze(reformated_data)
    return reformated_data        
 
#%% variables and filenames settings dt = 1/10E3

# no trials, only averages per electrodes per stim
#filename ='PSTHS_2019_TUN21_without_top_synch'
##filename ='PSTHS_2019_TUN21_with_top_synch'
filename ='psths_trials_2019_TUN_21_V2'

# trials for each electrode per stim
#filename ='PSTHS_TRIALS_2010_TUN21'

input_dat = loadmat(filename+ '_list')

conditions = [1, 2, 3, 10, 11, 12, 19]
elecs_input = []
for i in range(65):
    if (i!= 0):
        elecs_input.append(i)
electrodes = [x - 1 for x in elecs_input]
trials = []
for j in range(31):
    if j != 0:
        trials.append(j)
        
#data = average_to_dict(input_dat, conditions, elecs_input) 
#data = trials_to_dict(input_dat, conditions, elecs_input, trials)

#%% import dict as pickle

pickle_in = open(filename+"_list.pickle","rb")
data = pickle.load(pickle_in)
#%% export dict as pickle

pickle_out = open(filename +"_list.pickle", "wb")
pickle.dump(data, pickle_out)
pickle_out.close()
#%% files specifications 
   
files_list = ['PSTHS_TRIALS_2010_TUN21',
              'PSTHS_2019_TUN21_with_top_synch',
              'PSTHS_2019_TUN21_without_top_synch',
              'psths_trials_2019_TUN_21_V2',
              'psths_trials_2019_TUN_21_V2_list']

ylims = [0.3, 60, 60, 0.3, 0.3]
# layers
# 2/3: 12 - 28, 4: 35 - 45, 5/6: 50 - 64 on github
# 2/3: 24, 4: 45 on cloud 
layers = [(24,45), (24,45), (24,45), (24,45), (24,45)]
files_props = list(zip(files_list, ylims, layers))

for n in range(len(files_props)):
    if filename in files_props[n]:
        file_idx = n

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

#suppress n=1 sized dimension
if (filename in files_list[1]) or (filename in files_list[2]):
    for cond in conditions:
        data[cond] = np.squeeze(data[cond])
#%% check original .mat keys/dimensions
#print(input_dat.keys())

if filename in files_list[0]:
    print(len(input_dat['PSTH_STIM_1_ELEC_1_TRIAL_1']))
    print(len(input_dat['PSTH_STIM_12_ELEC_1_TRIAL_1']))
elif (filename in files_list[1]): 
    print(np.shape(input_dat['Top_Synchro_2']))
    print(len(input_dat['Top_Synchro_2']))
    print('     ')
    print('     ')
    print('     ')
    print(input_dat['Top_Synchro_10'][0])
    print(input_dat['Top_Synchro_10'][1])
    print(np.shape(input_dat['Top_Synchro_10']))
    print(len(input_dat['Top_Synchro_10']))
elif (filename in files_list[3]) or (filename in files_list[4]): 
    print(np.shape(input_dat['Stim19Elec51Repet30']))
#%% check reformated_dict keys/dimensions
#print(data.keys())

print(np.shape(data[1]))
print(np.shape(data[2]))
print(np.shape(data[12]))
print(' ')
print(np.shape(data[1][63]))
print(np.shape(data[12][0]))
print(' ')
# up to trial dimension
if (filename in files_list[0]) or (filename in files_list[3]) or (
        filename in files_list[4]):
    print(np.shape(data[1][63][0]))
#%% from dict to df

meanL = []
for i in conditions:
    tmp_meanL = []
    for j in electrodes:
        if (filename in files_list[0]) or (filename in files_list[3]) or (filename in files_list[4]):
            vec = np.mean(data[i][j], axis=0)
        elif (filename in files_list[1]) or (filename in files_list[2]):
            vec = data[i][j]
        tmp_meanL.append(vec)
    meanL.append(tmp_meanL)    
df = pd.DataFrame(meanL)
df = df.transpose()
df.columns = cond_names
#%% from df to list of matrices

matL = []
for n in range(len(conditions)):
    mat = df[cond_names[n]].tolist()
    dim = np.size(mat,1)
    mat = np.reshape(mat, (64, dim))                        
    matL.append(mat)
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
   
    #axes[63].set_xlim(dim/2, dim-1 - dim/4)
    axes[63].set_xlim(0, 1200)
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
                
        axes[0,n].matshow(matL[n], cmap='jet', vmin=0, vmax=
                          files_props[file_idx][1], interpolation='gaussian')
        #axes[0,n].set_xlim(dim/2, dim-1 - dim/4)    
        axes[0,n].set_xlim(900, 1050)    
        
        axes[0,n].tick_params(axis ='x', bottom =True, top=False, 
                              labelbottom=True, labeltop =False)
        axes[0,n].tick_params(axis ='y', left=True, right=False, 
                              labelleft=True, labelright =False)
        axes[0,0].set_ylabel(' Depth (electrode)')
        
        axes[0,n].set_title(cond_labels[n], color = cond_colors[n])
        axes[0,n].axhline(files_props[file_idx][2][0], 0,1,color='white')
        axes[0,n].axhline(files_props[file_idx][2][1], 0,1,color='white')
        
    elif n > 2:
        axes[1,n-3].matshow(matL[n], cmap='jet', vmin=0, vmax=
                          files_props[file_idx][1], interpolation='gaussian')
        axes[1,n-3].tick_params(axis ='x', bottom=True, top=False,
                                labelbottom=True, labeltop =False)
        axes[1,n-3].tick_params(axis ='y', left=True, right=False, 
                                labelleft=True, labelright =False)
        axes[1,0].set_ylabel(' Depth (electrode)')
        
        axes[1,n-3].set_title(cond_labels[n], color = cond_colors[n])
        axes[1,n-3].axhline(files_props[file_idx][2][0], 0,1,color='white')
        axes[1,n-3].axhline(files_props[file_idx][2][1], 0,1,color='white')
        axes[1,n-3].set_xlabel(' Time (ms)')
        
#fig.suptitle(filename + ' 1 ms subsampled', size = 16)                       
#fig.suptitle(filename + ' 5 ms subsampled', size = 16)                        
fig.tight_layout()
