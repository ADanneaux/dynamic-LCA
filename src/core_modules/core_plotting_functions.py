import numpy as np
import matplotlib.pyplot as plt

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

def plot_methane_decay(f_M,t_TOD):
    # Plotting decay
    fix, ax = plt.subplots(1,1,figsize=(6,4))

    #SOL
    sol_line = plot_after_zeros(t_TOD, 1e-3*f_M['SOL'][:len(t_TOD)], 'darkgrey', ax, '-')
    eol_line = plot_after_zeros(t_TOD, 1e-3*f_M['EOL'][:len(t_TOD)], 'black', ax, '-')
    cre_line = plot_after_zeros(t_TOD, 1e-3*f_M['CRE'][:len(t_TOD)], 'red', ax, '-')
    Ebe_line = plot_after_zeros(t_TOD, 1e-3*f_M['EOL_bio_emissions_notdivided'][:len(t_TOD)], 'green', ax, '-')
    Ebc_line = plot_after_zeros(t_TOD, 1e-3*f_M['EOL_bio_credit_notdivided'][:len(t_TOD)], 'green', ax, '--')


    #Net
    ax.plot(t_TOD, 1e-3*f_M['Net'][:len(t_TOD)],label='Net',color='gold')

    ax.set_xlabel('Years since construction')
    ax.set_ylabel('CO2 [kg]')
    ax.set_xlim([-1,200])    
    ax.axhline(0, color='black')
    return fix, ax