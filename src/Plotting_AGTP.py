#%% Importing libraries

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
matplotlib.rcParams['font.family'] = 'Times New Roman'


matplotlib.rcParams["legend.frameon"] = True
matplotlib.rcParams["legend.fancybox"] = False
matplotlib.rcParams['axes.unicode_minus'] = True
hfont = {'fontname':'Futura Bk BT'}
from matplotlib import ticker
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-10,10))
import seaborn as sns
import pandas as pd


#%%     Stacked bars function
def get_cumulated_array(data, **kwargs):
    cum = data.clip(**kwargs)
    cum = np.cumsum(cum, axis=0)
    d = np.zeros(np.shape(data))
    d[1:] = cum[:-1]
    return d
#%%

Data = pd.read_csv('output\AGTP_results.csv',header=0,index_col=0)

#%%
Colors =pd.DataFrame({'BAU':sns.color_palette("muted", 9)[3],
                      'ASP':sns.color_palette("muted", 9)[0],
                      'T_1':sns.color_palette("muted", 9)[2],
                      'T_2':sns.color_palette("muted", 9)[1],
                      'T_3':sns.color_palette("muted", 9)[4],
                      'T_4':sns.color_palette("muted", 9)[5],
                      'T_5':sns.color_palette("muted", 9)[6],
                      'T_6':sns.color_palette("muted", 9)[7],
                      'T_7':sns.color_palette("muted", 9)[8],})

# %%
building_types = Colors.columns

fig, ax = plt.subplots()
ax.axhline(y=0,color='black')
for building_type in building_types:
    scenarios = [x for x in Data.columns if x[:3]==building_type]
    ymax = []
    ymin = []
    for t in range(len(Data)):
        ymax.append(max([Data[x][t] for x in scenarios])*1e7)
        ymin.append(min([Data[x][t] for x in scenarios])*1e7)
        
    ax.fill_between(Data['T'].values,ymin,ymax,color=list(Colors[building_type]),alpha=0.3)
    ax.plot(Data['T'].values,ymax,color=list(Colors[building_type]))
    ax.plot(Data['T'].values,ymin,color=list(Colors[building_type]))
    ax.text(305,(ymax[-1]+ymin[-1])/2,building_type.replace("_",""),color=list(Colors[building_type]))
ax.set_xlim([-5,327])
ax.set_ylabel('[1e-7 K]')
ax.set_title('AGTP')

fig.savefig('Output\Figures\AGTP.png',dpi=300,bbox_inches='tight')
# %%
