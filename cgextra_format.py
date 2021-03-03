"""
reformat datas into dict, df or mat list
"""
import numpy as np
import pandas as pd

# turn .mat to dict
# each key is of type: PSTH_STIM_n1_ELEC_n2_TRIAL_n3
#stims of interest: 
#1: ctr_ls, 2:son_ls, 3: stc_ls, 10 = ctr_hs, 11: son_hs; 12: stc_hs, 19: blk
# n1 stim = 7 of interest, n2 electrode = 64, n3 trial = 30

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
def average_to_dict(dat, conds, elecs, skey, eleck):
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
                    if (skey + str(int(cond)) + eleck + '%d' % (elec) in dat):
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
def dict_to_df(dt_dict, condl, condn, elecs, filen, flist):
    """
    turns dict to df
    """
    meanl = []
    for i in condl:
        tmp_meanl = []
        for j in elecs:
            if (filen in flist[0]) or (filen in flist[3]) or \
                (filen in flist[3]) or (filen in flist[4]):
                mean_vec = np.mean(dt_dict[i][j], axis=0)
            elif (filen in flist[1]) or (filen in flist[2]):
                mean_vec = dt_dict[i][j]
            tmp_meanl.append(mean_vec)
        meanl.append(tmp_meanl)    
    df_tmp = pd.DataFrame(meanl)
    df_tmp = df_tmp.transpose()
    df_tmp.columns = condn
    return df_tmp

#from df to list of matrices
def df_to_matl(df_tmp, condl, condn):
    """
    turns df to matrices list
    """
    matl = []
    for ind in range(len(condl)):
        mat = df_tmp[condn[ind]].tolist()
        dimensions = np.size(mat,1)
        mat = np.reshape(mat, (64, dimensions))                        
        matl.append(mat)
    return matl, dimensions
