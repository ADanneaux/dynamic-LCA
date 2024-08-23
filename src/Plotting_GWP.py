#%% Importing libraries

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

plt.style.use('seaborn-white')
matplotlib.rcParams['font.family'] = 'arial'
matplotlib.rcParams["legend.frameon"] = True
matplotlib.rcParams["legend.fancybox"] = False
matplotlib.rcParams['axes.unicode_minus'] = False
hfont = {'fontname':'Futura Bk BT'}
from matplotlib import ticker
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True) 
formatter.set_powerlimits((-1,1))


import seaborn as sns
import pandas as pd

#%%
output_path = os.path.join('..','output')
figures_path = os.path.join('..','figures')

#%%     Stacked bars function
def get_cumulated_array(data, **kwargs):
    cum = data.clip(**kwargs)
    cum = np.cumsum(cum, axis=0)
    d = np.zeros(np.shape(data))
    d[1:] = cum[:-1]
    return d
#%%

Data = pd.read_csv(os.path.join(output_path,'GWP_Results.csv'),header=0,index_col=0)

#%%
buildings = ['BAU_1','BAU_2','BAU_3','ASP_1','ASP_2','ASP_3','T_1','T_2','T_3','T_4','T_5','T_6','T_7']


xs = np.arange(len(buildings))


Variables = ['N2O','CH4','Life_carbonation','EOL_carbonation','CO2_net']
Var_names = ['N$_2$O','CH$_4$','Life carbonation','EOL carbonation','CO$_{2}$ net']
Colors = pd.DataFrame({'N2O': [sns.color_palette(x)[6] for x in ['muted','pastel']],
                       'Life_carbonation': [sns.color_palette('YlGn')[x] for x in [2,1]],
                       'EOL_carbonation': [sns.color_palette('BuGn')[x] for x in [3,2]],
                       'CH4': [sns.color_palette(x)[1] for x in ['muted','pastel']],
                       'CO2_net':[sns.color_palette(x)[0] for x in ['muted','pastel']]})

fig,axs = plt.subplots(2,1,figsize=(15/2.54,10/2.54))

for ind_THI in range(2):
    THI = ['100','200'][ind_THI]
    ax = axs[ind_THI]
    for ind_building in range(len(buildings)):

        for ind_dynamic in [0,1]:
            scenario = buildings[ind_building]+'_'+['Dynamic','Static'][ind_dynamic]+'_'+THI

            # Colors = [list(sns.color_palette(['muted','pastel'][ind_dynamic],5))[x] for x in [2,3,4,1,0]]

            data = []
            for var in Variables:
                data.append(Data.loc[scenario,var])
            
            data = np.array(data)*1e-6
            data_shape = np.shape(data)
            cumulated_data = get_cumulated_array(data, min=0)
            cumulated_data_neg = get_cumulated_array(data, max=0)

            # Re-merge negative and positive data.
            row_mask = (data < 0)
            cumulated_data[row_mask] = cumulated_data_neg[row_mask]
            data_stack = cumulated_data

            alines = []
            for i in np.arange(0, data_shape[0]):
                alines.append([
                    ax.bar(xs[ind_building]+[-0.15,0.15][ind_dynamic],
                            data[i],
                            bottom=data_stack[i],
                            color=Colors[Variables[i]][ind_dynamic],
                            alpha=0.8,
                            width=0.3,
                            label=Var_names[i])
                ])

            ax.errorbar(xs[ind_building]+[-0.15,0.15][ind_dynamic],
                        Data.loc[scenario,'Net']*1e-6,
                        # yerr=[[1e6],[1e6]],
                        yerr=[[Data.loc[scenario,'Low_Error']*1e-6],[Data.loc[scenario,'High_Error']*1e-6]],
                        ecolor='k',
                        capsize=3,
                        capthick=0.52,
                        elinewidth=0.52)
            
            if (ind_THI == 1 and ind_building==len(buildings)-1):
                ax.annotate(
                    ['Dynamic','Static'][ind_dynamic],
                    xy=(xs[ind_building]+[-0.15,0.15][ind_dynamic], Data.loc[scenario,'Net']*1e-6), xycoords='data',
                    xytext=([-60,-53][ind_dynamic], 10), textcoords='offset points',
                    horizontalalignment='left',
                    arrowprops=dict(arrowstyle="->",
                                    connectionstyle="arc,angleA=0,armA=50,rad=10"))

            if (ind_THI == 1 and ind_dynamic ==0):
                handles = [a[0] for a in alines]
                labels = [a[0].get_label() for a in alines]
            
    ax.set_title('GWP '+THI,fontsize=10)
    ax.set_ylabel('thousand tonnes CO$_2$.eq',fontsize=9)
    ax.set_xticks(xs)
    ax.set_xticklabels([x.replace('_','') for x in buildings],fontsize=8)
    ax.set_ylim([-0.5,2])
    ax.axhline(y=0,color='k',linestyle='-',linewidth=0.8)

fig.subplots_adjust(hspace=0.4, wspace=0.23)
fig.legend(handles=handles,
            labels=labels,
            loc='lower center',
            ncol=3,
            bbox_to_anchor=(0.5, -0.09),
            frameon=False,
            fontsize = 9)

fig.savefig(os.path.join(figures_path,'GWP.png'),dpi=300,bbox_inches='tight')
# %%
