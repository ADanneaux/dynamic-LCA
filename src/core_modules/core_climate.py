"""

"""
import numpy as np
# =========== Atmospheric decay of CO2 ===========
m_atmosphere= 5.1352e18  #[g/mol]
M_air= 28.97             #[g/mol]

# CO2 Parameters)
alpha_CO2 = 1
A0 = 0.217
A1 = 0.259
A2 = 0.337
A3 = 0.186
tau1 = 172.9     #[year]
tau2 = 18.51     #[year]
tau3 = 1.186     #[year]
RE_CO2=  1.37e-5 #[W/m2/ppbv]
M_CO2= 44        #[g/mol]
af_CO2= 1

# CH4 Parameters)
alpha_CH4 = 1
tau_CH4   = 12.4     #[year]
RE_CH4= 3.63e-4      #[W/m2/ppbv]
M_CH4= 16            #[g/mol]
af_CH4= 1.62

# N2O Parameters)
alpha_N2O = 1
tau_N2O   = 121     #[year] 
RE_N2O= 3e-3        #[W/m2/ppbv]
M_N2O= 44           #[g/mol]
af_N2O= 1.05


def define_rf():
    rf_CO2= RE_CO2* af_CO2*(M_air/M_CO2)*1e9/m_atmosphere #[W/m2/kg] 
    rf_CH4= RE_CH4* af_CH4*(M_air/M_CH4)*1e9/m_atmosphere #[W/m2/kg]
    rf_N2O= RE_N2O* af_N2O*(M_air/M_N2O)*1e9/m_atmosphere #[W/m2/kg]  
    return rf_CO2, rf_CH4, rf_N2O

#%% =========== Global Temperature Change Potential ===========
#Parameters)
c1 = 0.631   #[K(Wm-2)-1]
c2 = 0.429   #[K(Wm-2)-1]
d1 = 8.4     #[year]
d2 = 409.5   #[year]

def define_rt(t_TOD):
    Rt = (c1/d1)*np.exp(-t_TOD/d1)+(c2/d2)*np.exp(-t_TOD/d2)
    return Rt

#%% =========== Convolution function ===========

def decay_function(molecule: str,t) -> list:
    """
    Calculate the decay function for a given gas along a time serie
    """
    if molecule == "CO2":
        y  = [A0+A1*np.exp2(-(x)/tau1)+A2*np.exp2(-(x)/tau2)+A3*np.exp2(-(x)/tau3) for x in t]
    elif molecule == "CH4":
        y = [np.exp(-(x)/tau_CH4) for x in t]
    elif molecule == "N2O":
        y = [np.exp(-(x)/tau_N2O) for x in t]
    else:
        print("ERROR: unsupported molecule")

    return y


#%% =========================================================================================================
# =========================================================================================================
# =========================================================================================================


# =========== Lanfill decay ===========
def EOL_decay_functions(t_TOD,s,dt):
   # Source: EPA (2021) US Inventory (1990-2019) of GHG emissions and sinks
    tau_wood =29                                     #[years]
    k= np.log(2)/tau_wood                            #[years-1]
    # Source: IPCC (2006) Chapter 3 Annex

    # EoL decay function
    EoL_decay_f = np.array([0 if t_TOD[x] < s else dt * k * np.exp(-k * (t_TOD[x] - s)) for x in range(len(t_TOD))])
    
    return EoL_decay_f


def add_dynamic_GWP(f,denomz,rf):
    rf_CO2,_,_ = define_rf()
    GWP = 0           
    for pulse in ['SOL',  'EOL', 'CRE','incineration_pulse']:
        GWP += np.sum(f[pulse])*rf/rf_CO2/denomz[pulse]
    for pulse in ['EOL_bio_emissions','EOL_bio_credit']:   
        GWP += np.sum(f[pulse])*rf/rf_CO2
    return GWP