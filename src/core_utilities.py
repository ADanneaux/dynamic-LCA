
import numpy as np


#================================================================================================================================
def get_LCI_data(LCI_data,building_type,molecule):
    """
    Fetches LCI data and return in more easily usable dictionnary for each molecules
    """
    
    if molecule not in ['C','M','N']:
        print('ERROR: unknown molecule')

    Data = {}
    for step in ['EOL','SOL','CRE']:
        Data[step]= float(LCI_data.loc[molecule+'_'+step,building_type])  #[kg]
    
    return Data


def set_emissions(Data):
    """
    Initiating emissions dictionnary for a given molecule, contains each pulse from LCI data and the incineration pulse
    """
    Emissions = {}
    for pulse in ['SOL',  'EOL', 'CRE']:
        Emissions[pulse]=Data[pulse]
    Emissions['incineration_pulse'] = 0 #Initiated as 0 by default: is not 0 for C: set outside the function
    return Emissions

def initiate_pulse_dictionnaries(time_length):
    """
    """
    Pulse={}
    
    for pulse in ['SOL', 'EOL', 'CRE','incineration_pulse']:
        Pulse[pulse]=np.zeros(time_length)
    return Pulse

#================================================================================================================================

def place_emissions_in_pulse(Pulse, Emissions, t_TOD, Life, Dynamic):
    """
    """
    if Dynamic:
        pulse_time = [np.where(t_TOD==0),len(t_TOD[t_TOD<Life])-1,len(t_TOD[t_TOD<Life])-1,len(t_TOD[t_TOD<Life])-1]
    else:
        pulse_time = [np.where(t_TOD==0)]*4
    pulses = ['SOL',  'EOL', 'CRE','incineration_pulse']

    for ind_pulse, pulse in enumerate(pulses):
        Pulse[pulse][pulse_time[ind_pulse]] = Emissions[pulse]

    return Pulse


