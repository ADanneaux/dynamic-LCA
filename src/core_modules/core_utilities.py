
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

def place_emissions_in_pulse(Emissions, t_TOD, Life, Dynamic):
    # Initiate the pulse
    Pulse = initiate_pulse_dictionnaries(len(t_TOD))
    # Get the pulse time depending on if it's a dynamic analysis
    if Dynamic:
        pulse_time = [np.where(t_TOD==0),len(t_TOD[t_TOD<Life])-1,len(t_TOD[t_TOD<Life])-1,len(t_TOD[t_TOD<Life])-1]
    else:
        pulse_time = [np.where(t_TOD==0)]*4
    pulses = ['SOL',  'EOL', 'CRE','incineration_pulse']

    #Placing the emission as a pulse at the correct time
    for ind_pulse, pulse in enumerate(pulses):
        Pulse[pulse][pulse_time[ind_pulse]] = Emissions[pulse]

    return Pulse

#================================================================================================================================
def create_basic_convolution(y,Pulse) -> dict:
        # Convolves emission pulse and gas decay function: gives remaining amount of the GHG in the atmosphere
        f = {}
        for pulse in ['SOL',  'EOL', 'CRE','incineration_pulse']:
            f[pulse] = 	np.convolve(y,Pulse[pulse])
        return f



# =========== Convoluting EoL decay ===========
def EOL_bio_convolutions(f: dict,y,Pulse,denom)-> dict:
    """
    Convolution function for delayed continuous emissions
    Returns the remaining share both divided by equivalent CO2 pulse and not 
    """
    for pulse in['EOL_bio_emissions','EOL_bio_credit']:
        f[pulse] = 	np.convolve(y,np.array(Pulse[pulse][:len(denom)])/np.array(denom))
        #Necessary to calculate AGTP
        f[pulse+'_notdivided'] = 	np.convolve(y,np.array(Pulse[pulse][:len(denom)]))

    return f


def calculate_f_net(f:dict,t_TOD) -> dict:
    f['Net'] = 0
    for pulse in ['SOL',  'EOL', 'CRE','incineration_pulse', 'EOL_bio_emissions_notdivided','EOL_bio_credit_notdivided']:
        f['Net'] += f[pulse][:len(t_TOD)]
    return f