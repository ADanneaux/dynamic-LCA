"""
Uncarbonated share

@ADanneaux
2024-09-22 based on code from 2022-05-11

This code creates csv files containing the share of remaining uncarbonated concrete at building EOL  
This is calculated for different cement type and different EOL method

"""
#%% Import libraries
import numpy as np

# ============ Time parameters ===========
TH = 500            #[years]
r = 200             #[years]
storage = 0         #[years]
Life = 100          #[years]
TexposureEOL = 0.25 #[years]
n = TH*200+1
t = np.linspace(0,TH,n) 

k_out = 2.25*1e-3   *1.1     #[m/year1/2]
k_in = 6.3*1e-3     *1.1     #[m/year1/2]
K = k_out*1e3

#%%

S = {
    'RCA':[29.4, 13.8, 39.2, 17.6], #RCA
    'Unbound':[15.7, 27.5, 39.2, 17.6],
    'Landfill':[17.8, 27.1, 17.3, 37.8], #Landfill
}

A1 = {
    'RCA':0,
    'Unbound':0,
    'Landfill':0,
}

B = {
    'RCA':[5, 10, 20, 32],
    'Unbound':[1, 10, 30, 50],
    'Landfill':[10, 30, 50, 8500],
}


kSCM = [1,1.7]


def uncarbonated(Fdn,a,b,Do):
    """
    Calculates part-wise integration of uncarbonated concrete. (model from Xi et al (2016))
    Concrete is assumed to be crushed into spherical particles
    This function calculates the carbonation progress of the share of particles with diameters ranging from a to b.
    """
    if a>=Do[j]:
        Fdn.append(1-(b**4-a**4-4*Do[j]*(b**3-a**3)+6*Do[j]**2*(b**2-a**2)-4*Do[j]**3*(b-a))/(b**4-a**4))
    elif a<Do[j] and b>Do[j]:
        Fdn.append(1-(b**4-Do[j]**4-4*Do[j]*(b**3-Do[j]**3)+6*Do[j]**2*(b**2-Do[j]**2)-4*Do[j]**3*(b-Do[j]))/(b**4-a**4))
    else:
        Fdn.append(1)
    return Fdn

for ind_type, type in enumerate(['RCA','Unbound','Landfill']):
    for ind_cem, cem_type in enumerate(['BAU','LC3']): 
        s1=S[type][0]*1e-2
        s2=S[type][1]*1e-2
        s3=S[type][2]*1e-2
        s4=S[type][3]*1e-2

        a1 = 0
        b1 = B[type][0]
        b2 = B[type][1]
        b3 = B[type][2]
        b4 = B[type][3]

        Do = []
        Fd = []
        Fd1 = []
        Fd2 = []
        Fd3 = []
        Fd4 = []
        Fd5 = []

        for j in range(0,len(t)):
            if t[j]<Life:
                Do.append(0)
            else:
                Do.append(2*K*kSCM[ind_cem]*np.sqrt(t[j]-Life))

            Fd1 = uncarbonated(Fd1,a1,b1,Do)
            Fd2 = uncarbonated(Fd2,b1,b2,Do)
            Fd3 = uncarbonated(Fd3,b2,b3,Do)
            Fd4 = uncarbonated(Fd4,b3,b4,Do)
            Fd5 = uncarbonated(Fd5,b4,a1,Do)

            Fd.append(s1*Fd1[-1]+s2*Fd2[-1]+s3*Fd3[-1]+s4*Fd4[-1])

        np.savetxt('..\..\generated_data\Fd_'+type+'_'+cem_type+'.csv',np.array(Fd),delimiter=',')
        
        print (len(t))
        print(len(Fd))

# %%
