"""
set of file specific variables metadata combination
"""
def get_keys(filen, flist):
    """
    load file specific keys
    """    
    if (filen in flist[0]):
        key1 = 'PSTH_STIM'
        key2 = 'ELEC_'
        key3 = '_TRIAL_'
    elif (filen in flist[1]) or (filen in flist[2]):
        key1 = 'PSTH'
        key2 = ''
        key3 = '_'
    elif (filen in flist[3]) or (filen in flist[4]):
        key1 = 'Stim'
        key2 = 'Elec'
        key3 = 'Repet'
    return key1, key2, key3    

def get_condid(filen, flist):
    """
    # load file specific condition idx
    """
    if (filen in flist[0]) or (filen in flist[1]) or \
        (filen in flist[2]) or (filen in flist[3]):
        blk_target = 19
    elif (filen in flist[4]):
        blk_target = 16
    return blk_target

def get_trials(filen, flist):
    """
    # load file specific trials number
    """
    if (filen in flist[0]) or (filen in flist[1]) or \
        (filen in flist[2]) or (filen in flist[3]):
        trialsn = 30
    elif (filen in flist[4]):
        trialsn = 20
    return trialsn

def get_yscale(filen, flist):
    """
    # load file specific yscale
    """
    if (filen in flist[0]) or (filen in flist[3]) or (filen in flist[4]): 
        yscale = 0.3
    elif (filen in flist[1]) or (filen in flist[2]):
        yscale = 60
    return yscale

def get_layers(filen, flist):
    """
    # load file specific layers
    """
    lay_lim =()
    if (filen in flist[0]) or (filen in flist[1]) or \
        (filen in flist[2]) or (filen in flist[3]):
        lay_lim = (24,45)
    elif (filen in flist[4]):
        lay_lim = (29,50)
    return lay_lim
