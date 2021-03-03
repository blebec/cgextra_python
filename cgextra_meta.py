#%% set of metadata

def get_keys(fn, fl):
    """
    load file specific keys
    """    
    if (fn in fl[0]):
        key1 = 'PSTH_STIM'
        key2 = 'ELEC_'
        key3 = '_TRIAL_'
    elif (fn in fl[1]) or (fn in fl[2]):
        key1 = 'PSTH'
        key2 = ''
        key3 = '_'
    elif (fn in fl[3]) or (fn in fl[4]):
        key1 = 'Stim'
        key2 = 'Elec'
        key3 = 'Repet'
    return key1, key2, key3    

def get_condid(fn, fl):
    """
    # load file specific condition idx
    """
    if (fn in fl[0]) or (fn in fl[1]) or (fn in fl[2]) or (fn in fl[3]):
        blk_target = 19
    elif (fn in fl[4]):
        blk_target = 16
    return blk_target

def get_trials(fn, fl):
    """
    # load file specific trials number
    """
    if (fn in fl[0]) or (fn in fl[1]) or (fn in fl[2]) or (fn in fl[3]):
        trialsn = 30
    elif (fn in fl[4]):
        trialsn = 20
    return trialsn

def get_yscale(fn, fl):
    """
    # load file specific yscale
    """
    if (fn in fl[0]) or (fn in fl[3]) or (fn in fl[4]): 
        yscale = 0.3
    elif (fn in fl[1]) or (fn in fl[2]):
        yscale = 60
    return yscale

def get_layers(fn, fl):
    """
    # load file specific layers
    """
    lay_lim =()
    if (fn in fl[0]) or (fn in fl[1]) or (fn in fl[2]) or (fn in fl[3]):
        lay_lim = (24,45)
    elif (fn in fl[4]):
        lay_lim = (29,50)
    return lay_lim