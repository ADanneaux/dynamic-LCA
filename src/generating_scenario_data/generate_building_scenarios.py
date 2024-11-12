"""
24/08/2024

author : @ADanneaux

This code takes SOL and EOL data and returns the list of scenarios to be tested by Main_dLCA.py

"""
#%% Importing libraries & data
import pandas as pd
import os

raw_data_path = os.path.join("..", "..","raw_data")
treated_data_path = os.path.join("..", "..","generated_data")

LCI_SOL = pd.read_csv(os.path.join(raw_data_path,'LCI_SOL.csv'),index_col=0)
LCI_EOL = pd.read_csv(os.path.join(raw_data_path,'LCI_EOL.csv'),index_col=0)


#%% Default data

C_Pine_Mass = {
    'BAU':12047.04,
    'LC3':12047.04,
    'EST':415416.13,
}

ConcreteVolume = {
    'BAU':1939,
    'LC3':1939,
    'EST':773,
}

Area_in = {
    'BAU':3097.5,
    'LC3':3097.5,
    'EST':0,
}

Cemtype = {
    'BAU':0,
    'LC3':1,
    'EST':0
}

LFD_index = {
    'BAU_C1':0,
    'BAU_C2':1,
    'BAU_C3':2,
    'LC3_C1':3,
    'LC3_C2':4,
    'LC3_C3':5,
}



#%% Defining the dataframe
building_types = [x+'_'+y for x in ['BAU','LC3'] for y in ['C1','C2','C3']] + ['EST_T'+str(x) for x in range(1,8)]

def filling_scenario(Data,scenario,Dynamic,THI,SSP,TexposureEOL):
    SOL = scenario.split('_')[0]
    EOL = scenario.split('_')[1]

    Data.loc['Dynamic',scenario] = int(Dynamic)
    Data.loc['THI',scenario] = int(THI)
    Data.loc['SSP',scenario] = int(SSP)

    Data.loc['C_Pine_Mass',scenario] = C_Pine_Mass[SOL]

    for index in LCI_SOL.index:
        Data.loc[index,scenario] = LCI_SOL.loc[index,SOL]
    for index in LCI_EOL.index:
        Data.loc[index,scenario] = LCI_EOL.loc[index,EOL]

    Data.loc['Area_in',scenario] = Area_in[SOL]
    Data.loc['Area_out',scenario] = 0 #All buildings studied are assumed to be fully cladded

    Data.loc['Cemtype',scenario] = Cemtype[SOL]

    Data.loc['LFD_index',scenario] = 2 if SOL=='EST' else LFD_index[SOL+'_'+EOL]

    Data.loc['ConcreteVolume',scenario] = ConcreteVolume[SOL]

    if EOL in ['T7','C1','C2','C3']:
        # Assume 2018 treatment share of timber in concrete buildings
        Data.loc['landfill_Ashare',scenario]  = 0.48
        Data.loc['landfill_Bshare',scenario]  = 0.13
        Data.loc['landfill_Cshare',scenario]  = 0.12
        Data.loc['recycling_share',scenario]   = 0.09
        Data.loc['incineration_share',scenario]= 0.18
    else:
        Data.loc['landfill_Ashare',scenario]  = 1 if EOL=='T4' else 0
        Data.loc['landfill_Bshare',scenario]  = 1 if EOL=='T5' else 0
        Data.loc['landfill_Cshare',scenario]  = 1 if EOL=='T6' else 0
        Data.loc['recycling_share',scenario]   = 1 if EOL in ['T2','T3']  else 0
        Data.loc['incineration_share',scenario]= 1 if EOL=='T1' else 0

    Data.loc['TexposureEOL',scenario] = TexposureEOL
    return Data
# %% Scenario_LCI
Data = pd.DataFrame()
for Dynamic, method in enumerate(['Static','Dynamic']):
    for ind_SSP, SSP in enumerate(["_SSP1","_SSP2","_SSP3"]):
        for THI in [20,100,200]:
            for ind_building, building in enumerate(building_types):
                scenario = building+'_'+method+'_'+str(THI)+SSP
                print(scenario)
                TexposureEOL = 0.25 # In all default scenarios, concrete is left exposed for 3 months after building demolition
                Data = filling_scenario(Data,scenario,Dynamic,THI,ind_SSP,TexposureEOL)

directory = treated_data_path
if not os.path.exists(directory):
    os.makedirs(directory)

Data.to_csv(os.path.join(treated_data_path,'Scenario_LCI.csv'),index=True)
# %% Input_AGTP
Data = pd.DataFrame()
for ind_SSP, SSP in enumerate(["_SSP1","_SSP2","_SSP3"]):
    for TexposureEOL in [0.25,5,10]:
        for ind_building, building in enumerate(building_types):
            Dynamic = 1
            THI = 300
            scenario = building+'_'+str(TexposureEOL)+SSP
            print(scenario)
            Data = filling_scenario(Data,scenario,Dynamic,THI,ind_SSP,TexposureEOL)

Data.to_csv(os.path.join(treated_data_path,'Input_AGTP.csv'),index=True)
# %%
