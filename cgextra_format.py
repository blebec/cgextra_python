import numpy as np
import pandas as pd

# turn .mat to dict
"""
each key is of type: PSTH_STIM_n1_ELEC_n2_TRIAL_n3
#stims of interest: 
#1: ctr_ls, 2:son_ls, 3: stc_ls, 10 = ctr_hs, 11: son_hs; 12: stc_hs, 19: blk
# n1 stim = 7 of interest, n2 electrode = 64, n3 trial = 30
"""
def trials_to_dict(dat, conds, elecs, trials, skey, eleck, trialk):
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
                        reformated_data[cond, elec].append \
                            (dat[skey + str(cond) + eleck + \
                                 str(elec) + trialk + str(trial)])    
                    reformated_data[cond, elec] = np.squeeze \
                        (reformated_data[cond, elec])
                    reformated_data[cond].append \
                        (reformated_data[cond, elec])                                    
    return reformated_data        

#each key is of type: PSTH_STIM_n1_ELEC_n2
def average_to_dict(dat, conds, elecs, skey):
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
                    if (skey + str(int(cond)) + '%d' % (elec) in dat):
                        reformated_data[cond, elec].append \
                            (np.array(dat[skey + str(int(cond))+ '%d' \
                                          % (elec)]).flatten()) 
                          
                    reformated_data[cond, elec] = np.array \
                        (reformated_data[cond, elec])
                    reformated_data[cond].append \
                        (reformated_data[cond, elec])                
            reformated_data = np.array(reformated_data)
            reformated_data = np.squeeze(reformated_data)
    return reformated_data        

#from dict to df
def dict_to_df(dt_dict, condL, condN, elecs, fn, fl):
        meanL = []
        for i in condL:
            tmp_meanL = []
            for j in elecs:
                if (fn in fl[0]) or (fn in fl[3]) or \
                    (fn in fl[3]) or (fn in fl[4]):
                        mean_vec = np.mean(dt_dict[i][j], axis=0)
                elif (fn in fl[1]) or (fn in fl[2]):
                    mean_vec = dt_dict[i][j]
                tmp_meanL.append(mean_vec)
            meanL.append(tmp_meanL)    
        df_tmp = pd.DataFrame(meanL)
        df_tmp = df_tmp.transpose()
        df_tmp.columns = condN
        return df_tmp

#from df to list of matrices
def df_to_matL(df_tmp, condL, condN):
    matL = []
    for n in range(len(condL)):
        mat = df_tmp[condN[n]].tolist()
        dimensions = np.size(mat,1)
        mat = np.reshape(mat, (64, dimensions))                        
        matL.append(mat)
    return matL, dimensions