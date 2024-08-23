"""
Dynamic life cycle analysis code

Authors: 
- Augustin Danneaux
- Estelle Schurer
- Alperen Yayla

"""

#%% Importing libraries
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import norm
from scipy import signal
import os

matplotlib.rcParams['font.family'] = 'arial'
matplotlib.rcParams["legend.frameon"] = True
matplotlib.rcParams["legend.fancybox"] = False
matplotlib.rcParams['axes.unicode_minus'] = False
hfont = {'fontname':'Futura Bk BT'}
from matplotlib import ticker
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-1,1))
date = datetime.datetime.now()
date = str(date.year)+str(date.month)+str(date.day)

#%% Analysis type

ind_GWP = False
ind_AGTP = not ind_GWP #Set so code does not calculate GWP and AGTP at the same time which would take a long time
ind_plot = True


#%%Importing Data

input_path = os.path.join('..','data')
output_path = os.path.join('..','output')


K119       = pd.read_csv(os.path.join(input_path,'K119.csv')).values
K126       = pd.read_csv(os.path.join(input_path,'K126.csv')).values
K245       = pd.read_csv(os.path.join(input_path,'K245.csv')).values
K370       = pd.read_csv(os.path.join(input_path,'K370.csv')).values
K485       = pd.read_csv(os.path.join(input_path,'K485.csv')).values

Fd_RCA     = pd.read_csv(os.path.join(input_path,'Fd_RCA.csv')).values
Fd_Unb     = pd.read_csv(os.path.join(input_path,'Fd_unbound.csv')).values
Fd_Lan     = [x[0] for x in pd.read_csv(os.path.join(input_path,'Fd_Landfill.csv')).values]
Fd_RCA_LC3 = pd.read_csv(os.path.join(input_path,'Fd_RCA_LC3.csv')).values
Fd_Unb_LC3 = pd.read_csv(os.path.join(input_path,'Fd_unbound_LC3.csv')).values
Fd_Lan_LC3 = [x[0] for x in pd.read_csv(os.path.join(input_path,'Fd_Landfill_LC3.csv')).values]

if ind_GWP:
    LCI_data  = pd.read_csv(os.path.join(input_path,'Scenario_LCI.csv'),index_col=0)
elif ind_AGTP:
    LCI_data  = pd.read_csv(os.path.join(input_path,'Input_AGTP.csv'),index_col=0)
else:
    print('Error: No analysis type selected')
#%%
Fd_EOL = [Fd_RCA[x][0]*0.23+Fd_Unb[x][0]*0.77 for x in range(0,len(Fd_RCA))]
Fd_EOL_LC3 = [Fd_RCA_LC3[x][0]*0.23+Fd_Unb_LC3[x][0]*0.77 for x in range(0,len(Fd_RCA_LC3))]

Fd_EOL3 = [Fd_Lan[x]*0.213+Fd_EOL[x]*0.787 for x in range(0,len(Fd_RCA))]
Fd_EOL3_LC3 = [Fd_Lan_LC3[x]*0.213+Fd_EOL_LC3[x]*0.787 for x in range(0,len(Fd_RCA))]

#%% Scenario dependent Parameters
# =========== Amount of raw pine ===========




Cemtype =[0         ,0          ,0          ,1          ,1          ,1]
LFD     =[Fd_EOL    ,Fd_Lan     ,Fd_EOL3    ,Fd_EOL_LC3 ,Fd_Lan_LC3 ,Fd_EOL3_LC3 ]
#EOLcarbonation = [0,0.25,0.4,0.5,1,5,10,25,50,100]
EOLcarbonation = [0.25]

#TimeHorizon = [20,100,200,300]
TimeHorizon = [20]#,100,200]

#%%Constant parameters
MCar2  = [130.6/0.8,71.82088/0.8]
ConcreteVolume = 1169.456 #[m3]
demolA = 220             #[-]  - factor by which the exposed area is increased at demolition
kSCM = [1,1.7]


TOD = 500           #[years]

r = 100            #[years]
s = 100            #[years]
Life = 100         #[years]

n = TOD*200+1
t_TOD = np.linspace(0,TOD,n) 
dt = t_TOD[1]-t_TOD[0]

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

rf_CO2= RE_CO2* af_CO2*(M_air/M_CO2)*1e9/m_atmosphere #[W/m2/kg] 
# CH4 Parameters)
alpha_CH4 = 1
tau_CH4   = 12.4     #[year]
RE_CH4= 3.63e-4      #[W/m2/ppbv]
M_CH4= 16            #[g/mol]
af_CH4= 1.62
rf_CH4= RE_CH4* af_CH4*(M_air/M_CH4)*1e9/m_atmosphere #[W/m2/kg] 



# N2O Parameters)
alpha_N2O = 1
tau_N2O   = 121     #[year] 
RE_N2O= 3e-3        #[W/m2/ppbv]
M_N2O= 44           #[g/mol]
af_N2O= 1.05
rf_N2O= RE_N2O* af_N2O*(M_air/M_N2O)*1e9/m_atmosphere #[W/m2/kg] 


#%% =========== Global Temperature Change Potential ===========
#Parameters)
c1 = 0.631   #[K(Wm-2)-1]
c2 = 0.429   #[K(Wm-2)-1]
d1 = 8.4     #[year]
d2 = 409.5   #[year]

Rt = (c1/d1)*np.exp(-t_TOD/d1)+(c2/d2)*np.exp(-t_TOD/d2)


#%% =========== Convolution functions ===========
yCO2_TOD = [A0+A1*np.exp2(-(x)/tau1)+A2*np.exp2(-(x)/tau2)+A3*np.exp2(-(x)/tau3) for x in t_TOD]

Empty_pulse = 0*t_TOD

SSPn = ['1-19','2-45','4-85']
name_array = []
#%% =========== Function to plot carbon decays ===========
def plot_after_zeros(x, y, col, ax, style):
    x = np.array(x)
    y = np.array(y)
    xs = x[y!=0]
    ys = y[y!=0]
    line = ax.plot(xs, ys, col, linestyle=style)
    fill = ax.fill_between(xs, ys, 0, color=col, alpha=0.2)
    return line, fill

def plot_carbon_decay(f_C,f_C_Carb_notdivided,f_C_G_notdivided,f_C_G_credit_notdivided,t_TOD):
    f_neg = f_C_G_notdivided[:len(t_TOD)]+f_C_Carb_notdivided[:len(t_TOD)]+f_C['incineration_pulse'][:len(t_TOD)]
    
    # Plotting decay
    fix, ax = plt.subplots(1,1,figsize=(6,4))

    #SOL
    sol_line = plot_after_zeros(t_TOD, 1e-3*f_C['SOL'][:len(t_TOD)], 'darkgrey', ax, '-')
    eol_line = plot_after_zeros(t_TOD, 1e-3*f_C['EOL'][:len(t_TOD)], 'black', ax, '-')
    cre_line = plot_after_zeros(t_TOD, 1e-3*f_C['CRE'][:len(t_TOD)], 'red', ax, '-')
    sin_line = plot_after_zeros(t_TOD, 1e-3*f_neg[:len(t_TOD)], 'green', ax, '-')
    Gcr_line = plot_after_zeros(t_TOD, 1e-3*f_C_G_credit_notdivided[:len(t_TOD)], 'red', ax, '--')
    
    #Net
    ax.plot(t_TOD, 1e-3*f_C['Net'][:len(t_TOD)],label='Net',color='gold')

    ax.set_xlabel('Years since construction')
    ax.set_ylabel('CO2 [kg]')
    ax.set_xlim([-1,200])    
    ax.axhline(0, color='black')
    return fix, ax

def plot_methane_decay(f_M,t_TOD):#,f_C_Carb_notdivided,f_C_G_notdivided,f_C_G_credit_notdivided,t_TOD):
    # f_neg = f_C_G_notdivided[:len(t_TOD)]+f_C_Carb_notdivided[:len(t_TOD)]+f_C['incineration_pulse'][:len(t_TOD)]
    
    # Plotting decay
    fix, ax = plt.subplots(1,1,figsize=(6,4))

    #SOL
    sol_line = plot_after_zeros(t_TOD, 1e-3*f_M['SOL'][:len(t_TOD)], 'darkgrey', ax, '-')
    eol_line = plot_after_zeros(t_TOD, 1e-3*f_M['EOL'][:len(t_TOD)], 'black', ax, '-')
    cre_line = plot_after_zeros(t_TOD, 1e-3*f_M['CRE'][:len(t_TOD)], 'red', ax, '-')
    Ebe_line = plot_after_zeros(t_TOD, 1e-3*f_M['EOL_bio_emissions_notdivided'][:len(t_TOD)], 'green', ax, '-')
    Ebc_line = plot_after_zeros(t_TOD, 1e-3*f_M['EOL_bio_credit_notdivided'][:len(t_TOD)], 'green', ax, '--')

    # sin_line = plot_after_zeros(t_TOD, 1e-3*f_neg[:len(t_TOD)], 'green', ax, '-')
    # Gcr_line = plot_after_zeros(t_TOD, 1e-3*f_C_G_credit_notdivided[:len(t_TOD)], 'red', ax, '--')
    
    #Net
    ax.plot(t_TOD, 1e-3*f_M['Net'][:len(t_TOD)],label='Net',color='gold')

    ax.set_xlabel('Years since construction')
    ax.set_ylabel('CO2 [kg]')
    ax.set_xlim([-1,200])    
    ax.axhline(0, color='black')
    return fix, ax



#%% Looping through buildings
GWP_C_net_array = []
GWP_M_array = []
GWP_N_array = []
GWP_L_carb_array = []
GWP_EOL_carb_array = []
GWP_MN_array = []
GWP_Net_array = []
AGTP_results = pd.DataFrame()



building_types = list(LCI_data.columns)




for building_type in building_types[25:35]:#[25:38]:
    print(building_type)
    Dynamic = bool(LCI_data[building_type]['Dynamic'])
    SSP = int(LCI_data[building_type]['SSP'])
    THI = float(LCI_data[building_type]['THI'])
    
    #Get data
    
    incineration_share = float(LCI_data[building_type]['incineration_share']  )       #[-]

    pine_mass= float(LCI_data[building_type]['C_Pine_Mass'])          #[kg] Version 1 (CLT building)

    degradable_carbon = pine_mass*0.5*0.23   #tons of C (max 23% of wood subject to decay)

    Data_C ={}
    Data_C['Biopulse'] = pine_mass*0.5*3.67#[kg] C & CO2 conversion

    Data_C['SOL']= float(LCI_data[building_type]['C_SOL'])  #[kg]
    Data_C['EOL']= float(LCI_data[building_type]['C_EOL'])#-incineration_share*Data_C['Biopulse']  #[kg]
    Data_C['CRE']= float(LCI_data[building_type]['C_CRE'])  #[kg]

    print(Data_C['Biopulse']-Data_C['EOL'])

    Data_M ={}
    Data_M['SOL']= float(LCI_data[building_type]['M_SOL'])  #[kg]
    Data_M['EOL']= float(LCI_data[building_type]['M_EOL'])  #[kg]
    Data_M['CRE']= float(LCI_data[building_type]['M_CRE'])  #[kg]


    Data_N ={}
    Data_N['SOL']= float(LCI_data[building_type]['N_SOL'])  #[kg]
    Data_N['EOL']= float(LCI_data[building_type]['N_EOL'])  #[kg]
    Data_N['CRE']= float(LCI_data[building_type]['N_CRE'])  #[kg]

    ConcreteVolume= float(LCI_data[building_type]['ConcreteVolume'])   #[m3]
    Area_in= float(LCI_data[building_type]['Area_in'])                 #[m2]
    Area_out= float(LCI_data[building_type]['Area_out'])              #[m2]

    Cemtype= int(LCI_data[building_type]['Cemtype'])           #[-]
    LFD_index= int(LCI_data[building_type]['LFD_index'] )      #[-]

    landfill_Ashare = float(LCI_data[building_type]['landfill_Ashare'])         #[-]
    landfill_Bshare = float(LCI_data[building_type]['landfill_Bshare'])         #[-]
    landfill_Cshare = float(LCI_data[building_type]['landfill_Cshare'])         #[-]

    recycling_share = float(LCI_data[building_type]['recycling_share'] )        #[-]

    TexposureEOL = float(LCI_data[building_type]['TexposureEOL'] )       #[years]

    #Loop dependent parameters
    MCar  = MCar2[Cemtype]
    k_out = 2.25*1e-3 *kSCM[Cemtype]        #[m/year1/2]
    k_in = 6.3*1e-3   *kSCM[Cemtype]        #[m/year1/2]
    K = k_out*1e3
    Mmax = MCar*ConcreteVolume

    Fd = [x for x in LFD[LFD_index]]
    


    #Loop dependent Time parameters
    t = t_TOD[t_TOD<=THI]
    Rtt = Rt[t_TOD<=THI]

    #Convolution 
    denom = [yCO2_TOD[0]]
    for x in range(1,len(yCO2_TOD)):
        denom.append(denom[x-1]+yCO2_TOD[x])
    denom = np.array(denom)

    denom0   = float(denom[t_TOD==0+THI])


    denomz = {}
    denomz['SOL'] = denom0
    denomz['EOL'] = float(denom[t_TOD==Life+THI])
    denomz['incineration_pulse'] = float(denom[t_TOD==Life+THI])
    denomz['CRE'] = float(denom[int((Life+TexposureEOL)/dt)])
    denomz['EOL_bio_emissions'] = 1 # Denominator is included when calculating fv
    denomz['EOL_bio_credit']    = 1 # Denominator is included when calculating f
    denom    = denom[t_TOD>=THI]


    yCO2 = [A0+A1*np.exp2(-(x)/tau1)+A2*np.exp2(-(x)/tau2)+A3*np.exp2(-(x)/tau3) for x in t]
    yCH4 = [np.exp(-(x)/tau_CH4) for x in t]
    yN2O = [np.exp(-(x)/tau_N2O) for x in t]


    #

    Emissions_C = {}
    Emissions_M = {}
    Emissions_N = {}
    for pulse in ['SOL',  'EOL', 'CRE']:
        Emissions_C[pulse]=Data_C[pulse]
        Emissions_M[pulse]=Data_M[pulse]
        Emissions_N[pulse]=Data_N[pulse]

    Emissions_C['incineration_pulse'] = Data_C['Biopulse'] * incineration_share
    Emissions_M['incineration_pulse'] = 0
    Emissions_N['incineration_pulse'] = 0

    Pulse_C = {}
    Pulse_M = {}
    Pulse_N = {}
    for pulse in ['SOL', 'EOL', 'CRE','incineration_pulse']:
        Pulse_C[pulse]=np.zeros(len(t_TOD))
        Pulse_M[pulse]=np.zeros(len(t_TOD))
        Pulse_N[pulse]=np.zeros(len(t_TOD))


    #

    if Dynamic:

        pulse_time = [np.where(t_TOD==0),len(t_TOD[t_TOD<Life])-1,len(t_TOD[t_TOD<Life])-1,len(t_TOD[t_TOD<Life])-1]
        pulse = ['SOL',  'EOL', 'CRE','incineration_pulse']

        for ind_pulse in range(0,len(pulse)):
            Pulse_C[pulse[ind_pulse]][pulse_time[ind_pulse]] = Emissions_C[pulse[ind_pulse]]
            Pulse_M[pulse[ind_pulse]][pulse_time[ind_pulse]] = Emissions_M[pulse[ind_pulse]]
            Pulse_N[pulse[ind_pulse]][pulse_time[ind_pulse]] = Emissions_N[pulse[ind_pulse]]

    else:
        for pulse in ['SOL', 'EOL', 'CRE','incineration_pulse']:
            Pulse_C[pulse][t_TOD==0] = Emissions_C[pulse]
            Pulse_M[pulse][t_TOD==0] = Emissions_M[pulse]
            Pulse_N[pulse][t_TOD==0] = Emissions_N[pulse]





    # =========== Carbonation ===========
    M = (Area_in*k_in+Area_out*k_out)*np.sqrt(t_TOD)*MCar
    M[t_TOD>=Life]=M[t_TOD<Life][-1]
    ML= (Area_in*k_in+Area_out*k_out)*np.sqrt(Life)*MCar
    McarEOL = (Mmax-ML)*np.array(Fd)
    McarEOL[t_TOD[:-1]>=Life+TexposureEOL] = McarEOL[t_TOD[:-1]<Life+TexposureEOL][-1]

    M = [M[x]+McarEOL[x] for x in range(0,len(M)-1)]
    M = np.array(M)
    M[M>Mmax] = Mmax
    dMdt = []
    dMdtSSP = []
    dMdt_for_GWP = []

    K = [K119,K245,K485][SSP]

    for j in range(0,len(denom)):
        dMdt.append((M[j+1]-M[j]))
        dMdt_for_GWP.append(-dMdt[-1]/denom[j])
        dMdtSSP.append(dMdt[j]*K[j])

    MSSP = [0]
    for j in range(0,len(denom)):
        MSSP.append(float(MSSP[-1]+dMdtSSP[j]))

    MSSP = np.array(MSSP)

    MSSP[MSSP>Mmax]=Mmax

    dMdtSSP = []
    dMdtSSP_for_GWP = []
        
    for j in range(0,len(denom)):
        dMdtSSP.append((MSSP[j+1]-MSSP[j]))
        dMdtSSP_for_GWP.append(-dMdtSSP[-1]/denom[j])

    dMdtSSP_for_GWP_L   = [0 if t_TOD[x]>Life-2*dt else dMdtSSP_for_GWP[x] for x in range(len(dMdtSSP_for_GWP)) ]
    dMdtSSP_for_GWP_EOL = [0 if t_TOD[x]<=Life-2*dt else dMdtSSP_for_GWP[x] for x in range(len(dMdtSSP_for_GWP)) ]
    
 
    # =========== Biomass Sink = Gaussian ===========
    mu, sigma = r/2, r/4
    g = - dt*Data_C['Biopulse']*norm.pdf(t_TOD,mu,sigma)
    g_credit = dt*Data_C['Biopulse']*norm.pdf(t_TOD-Life,mu,sigma)*recycling_share
    g_credit[t_TOD<s]=0


    g_for_GWP = np.array(g[:len(denom)])/np.array(denom)
    g_credit_for_GWP  = np.array(g_credit[:len(denom)])/np.array(denom)
    # =========== Lanfill decay ===========

    # Source: EPA (2021) US Inventory (1990-2019) of GHG emissions and sinks
    tau_wood =29                                     #[years]
    k= np.log(2)/tau_wood                            #[years-1]
    # Source: IPCC (2006) Chapter 3 Annex



    # EoL decay function
    EoL_decay_f = np.array([0 if t_TOD[x] < s else dt * k * np.exp(-k * (t_TOD[x] - s)) for x in range(len(t_TOD))])




    #Methane heat + electricity co-production (EcoInvent): 
    # 0.249 m3 of natural gas= 3.6 MJ elec + 1.63 MJ heat
    CH4_burning = 0.249*0.657e-3/(3.6+1.63) # tonnes of CH4/MJ of energy

    Data_C['EOL_bio_credit']=-6.30E-05   #tonnes of CO2/MJ of energy (69/31 split elec/heat)
    Data_M['EOL_bio_credit']=-1.37E-06   #tonnes of CH4/MJ of energy
    Data_N['EOL_bio_credit']=-4.27E-09  #tonnes of N2O/MJ of energy


    Emissions_C['EOL_bio_emissions'] = degradable_carbon*(3.67) * (landfill_Ashare*10/100+ landfill_Bshare*99.7/100+ landfill_Cshare*99.995/100)
    Emissions_M['EOL_bio_emissions'] = degradable_carbon*(1.33) * (landfill_Ashare*90/100+ landfill_Bshare*0.03/100+ landfill_Cshare*0.005/100)
    Emissions_N['EOL_bio_emissions'] = 0

    Emissions_C['EOL_bio_credit'] = degradable_carbon*(1.33)/CH4_burning*Data_C['EOL_bio_credit']*landfill_Cshare
    Emissions_M['EOL_bio_credit'] = degradable_carbon*(1.33)/CH4_burning*Data_M['EOL_bio_credit']*landfill_Cshare
    Emissions_N['EOL_bio_credit'] = degradable_carbon*(1.33)/CH4_burning*Data_N['EOL_bio_credit']*landfill_Cshare


    for pulse in ['EOL_bio_emissions','EOL_bio_credit']:
        Pulse_C[pulse]=Emissions_C[pulse]*EoL_decay_f
        Pulse_M[pulse]=Emissions_M[pulse]*EoL_decay_f
        Pulse_N[pulse]=Emissions_N[pulse]*EoL_decay_f


    

    # =========== Emission Decay ===========

    f_C ={}
    f_M ={}
    f_N ={}

    for pulse in ['SOL',  'EOL', 'CRE','incineration_pulse']:
        f_C[pulse] = 	np.convolve(yCO2,Pulse_C[pulse])
        f_M[pulse] = 	np.convolve(yCH4,Pulse_M[pulse])
        f_N[pulse] = 	np.convolve(yN2O,Pulse_N[pulse])






    if Dynamic:
        # =========== Convoluting the carbonation sink===========
        f_C_Carb_L = np.convolve(yCO2,dMdtSSP_for_GWP_L)
        
        f_C_Carb_EOL = np.convolve(yCO2,dMdtSSP_for_GWP_EOL)
        f_C_Carb_notdivided = np.convolve(yCO2,[-x for x in dMdtSSP])
        # =========== Convoluting forestry sink===========
        f_C_G = np.convolve(yCO2,g_for_GWP)
        f_C_G_credit = np.convolve(yCO2,g_credit_for_GWP)

        f_C_G_notdivided = np.convolve(yCO2,g)
        f_C_G_credit_notdivided = np.convolve(yCO2,g_credit)

        # =========== Convoluting EoL decay ===========
        for pulse in['EOL_bio_emissions','EOL_bio_credit']:
            f_C[pulse] = 	np.convolve(yCO2,np.array(Pulse_C[pulse][:len(denom)])/np.array(denom))
            f_M[pulse] = 	np.convolve(yCH4,np.array(Pulse_M[pulse][:len(denom)])/np.array(denom))
            f_N[pulse] = 	np.convolve(yN2O,np.array(Pulse_N[pulse][:len(denom)])/np.array(denom))

            #Necessary to calculate AGTP
            f_C[pulse+'_notdivided'] = 	np.convolve(yCO2,np.array(Pulse_C[pulse][:len(denom)]))
            f_M[pulse+'_notdivided'] = 	np.convolve(yCH4,np.array(Pulse_M[pulse][:len(denom)]))
            f_N[pulse+'_notdivided'] = 	np.convolve(yN2O,np.array(Pulse_N[pulse][:len(denom)]))
        
        # =========== GWP composition ===========
        GWP_Carb_L = np.sum(f_C_Carb_L)
        GWP_Carb_EOL = np.sum(f_C_Carb_EOL)
        GWP_G   = np.sum(f_C_G)+np.sum(f_C_G_credit)
        GWP_C =0
        GWP_M =0
        GWP_N =0


        for pulse in ['SOL',  'EOL', 'CRE','incineration_pulse']:
            GWP_C += np.sum(f_C[pulse])/denomz[pulse]
            GWP_M += np.sum(f_M[pulse])*rf_CH4/rf_CO2/denomz[pulse]
            GWP_N += np.sum(f_N[pulse])*rf_N2O/rf_CO2/denomz[pulse]
        
        
        for pulse in ['EOL_bio_emissions','EOL_bio_credit']:
            GWP_C += np.sum(f_C[pulse])
            GWP_M += np.sum(f_M[pulse])*rf_CH4
            GWP_N += np.sum(f_N[pulse])*rf_N2O/rf_CO2

        
        GWP = GWP_Carb_L + GWP_Carb_EOL + GWP_C + GWP_M +  GWP_N  + GWP_G 


        f_C['Net'] = 0
        f_M['Net'] = 0
        f_N['Net'] = 0

        for pulse in ['SOL',  'EOL', 'CRE','incineration_pulse', 'EOL_bio_emissions_notdivided','EOL_bio_credit_notdivided']:
            f_C['Net'] += f_C[pulse][:len(t_TOD)]
            f_M['Net'] += f_M[pulse][:len(t_TOD)]
            f_N['Net'] += f_N[pulse][:len(t_TOD)]
        f_C['Net'] += f_C_Carb_notdivided[:len(t_TOD)] + f_C_G_notdivided[:len(t_TOD)] + f_C_G_credit_notdivided[:len(t_TOD)]


    else:
        # =========== Convoluting the carbonation sink===========
        P_C_carb_L = np.zeros(len(t_TOD))
        P_C_carb_EOL = np.zeros(len(t_TOD))
        P_C_carb_L[t_TOD==0] = -MSSP[np.where(t_TOD==Life)]
        P_C_carb_EOL[t_TOD==0] = -MSSP[-1]+MSSP[np.where(t_TOD==Life)]
            
        f_C_Carb_L = 	np.convolve(yCO2,P_C_carb_L)
        f_C_Carb_EOL = 	np.convolve(yCO2,P_C_carb_EOL)

        # =========== Convoluting forestry sink===========
        P_C_G = np.zeros(len(t_TOD))
        P_C_G[t_TOD==0] = np.sum(g)
        P_C_G_credit = np.zeros(len(t_TOD))
        P_C_G_credit[t_TOD==0] = np.sum(g_credit)

        f_C_G = np.convolve(yCO2,P_C_G)
        f_C_G_credit = np.convolve(yCO2,P_C_G_credit)

        f_C_G_notdivided = np.convolve(yCO2,P_C_G)
        f_C_G_credit_notdivided = np.convolve(yCO2,P_C_G_credit)

        # =========== Convoluting EoL decay ===========
        for pulse in['EOL_bio_emissions','EOL_bio_credit']:
            P_C = np.sum(Pulse_C[pulse])
            P_M = np.sum(Pulse_M[pulse])
            P_N = np.sum(Pulse_N[pulse])

            Pulse_C[pulse] = np.zeros(len(t_TOD))
            Pulse_M[pulse] = np.zeros(len(t_TOD))
            Pulse_N[pulse] = np.zeros(len(t_TOD))

            Pulse_C[pulse][t_TOD==0] = P_C
            Pulse_M[pulse][t_TOD==0] = P_M
            Pulse_N[pulse][t_TOD==0] = P_N

            
            f_C[pulse] = 	np.convolve(yCO2,Pulse_C[pulse])
            f_M[pulse] = 	np.convolve(yCH4,Pulse_M[pulse])
            f_N[pulse] = 	np.convolve(yN2O,Pulse_N[pulse])

        # =========== GWP composition ===========
        GWP_Carb_L = np.sum(f_C_Carb_L)/denom0
        GWP_Carb_EOL = np.sum(f_C_Carb_EOL)/denom0
        GWP_G   = np.sum(f_C_G)/denom0+np.sum(f_C_G_credit)/denom0

        GWP_C =0
        GWP_M =0
        GWP_N =0

        f_C['Net'] = 0
        f_M['Net'] = 0
        f_N['Net'] = 0

        for pulse in ['SOL',  'EOL', 'CRE', 'EOL_bio_emissions','EOL_bio_credit']:
            f_C['Net'] += f_C[pulse][:len(t_TOD)]
            f_M['Net'] += f_M[pulse][:len(t_TOD)]
            f_N['Net'] += f_N[pulse][:len(t_TOD)]

            GWP_C += np.sum(f_C[pulse])/denom0
            GWP_M += np.sum(f_M[pulse])*rf_CH4/rf_CO2/denom0
            GWP_N += np.sum(f_N[pulse])*rf_N2O/rf_CO2/denom0

        f_C['Net'] += f_C_Carb_notdivided[:len(t_TOD)] + f_C_G_notdivided[:len(t_TOD)] + f_C_G_credit_notdivided[:len(t_TOD)]

        GWP = GWP_Carb_L + GWP_Carb_EOL + GWP_C + GWP_M +  GWP_N + GWP_G

        
    if ind_AGTP:
        RF_net = f_C['Net']*rf_CO2 + f_M['Net']*rf_CH4 + f_N['Net']*rf_N2O
        AGTP = np.convolve(Rt,RF_net)
        AGTP_results[building_type] = AGTP[0:len(t_TOD[t_TOD<300])]

    if ind_GWP:
        GWP_C_net_array.append(GWP_C+ GWP_G + GWP_Carb_L + GWP_Carb_EOL)
        GWP_M_array.append(GWP_M)
        GWP_N_array.append(GWP_N)
        GWP_L_carb_array.append(GWP_Carb_L)
        GWP_EOL_carb_array.append(GWP_Carb_EOL)
        GWP_MN_array.append(GWP_M +  GWP_N)
        GWP_Net_array.append(GWP)

    
    # =========== Plotting Carbon decay ===========
    if ind_plot:
        plot_carbon_decay(f_C,f_C_Carb_notdivided,f_C_G_notdivided,f_C_G_credit_notdivided,t_TOD)
        # plot_methane_decay(f_M,t_TOD)    


if ind_GWP:
    Results = pd.DataFrame({'CO2_net':GWP_C_net_array,
                            'CH4':GWP_M_array,
                            'N2O':GWP_N_array,
                            'Life_carbonation':GWP_L_carb_array,
                            'EOL_carbonation':GWP_EOL_carb_array,
                            'MN':GWP_MN_array,
                            'Net':GWP_Net_array},
                            index=building_types)

    Low_Error = []
    High_Error = []

    Cbuildings = np.array([[[[x+'_'+v+'_'+y+'_'+z for x in ['BAU','ASP'] for y in ['Dynamic','Static']] for z in ['100','200']]] for v in ['1','2','3']]).flatten()

    for building_type in Cbuildings:
        SSP1 =building_type+'_SSP1'
        SSP4 =building_type+'_SSP4'
        Low_Error.append(Results['Net'][building_type]-Results['Net'][SSP4])
        High_Error.append(-Results['Net'][building_type]+Results['Net'][SSP1])

    Errors = pd.DataFrame({'Low_Error':Low_Error,
                            'High_Error':High_Error},
                            index=Cbuildings)

    Results=Results.merge(Errors, how='left', left_index=True, right_index=True)
    Results = Results.fillna(0)

    Results.to_csv(os.path.join(output_path+'GWP_results.csv'))

if ind_AGTP:
    AGTP_results['T']=t_TOD[t_TOD<300]
    AGTP_results.to_csv(os.path.join(output_path+'AGTP_results.csv'))
#%%
Results = np.array([building_types,GWP_C_net_array,GWP_M_array,GWP_N_array,GWP_L_carb_array,GWP_EOL_carb_array,GWP_MN_array,GWP_Net_array])
np.savetxt(os.path.join(output_path+'Results.csv', Results, delimiter=',', fmt='%s'))
# %%
