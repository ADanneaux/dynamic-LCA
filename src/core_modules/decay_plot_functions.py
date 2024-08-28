import plotly.graph_objects as go
import os

def plot_carbon_decay(building_type,f_C, f_C_Carb_notdivided, f_C_G_notdivided, f_C_G_credit_notdivided, t_TOD):
    f_neg = f_C_G_notdivided[:len(t_TOD)] + f_C_Carb_notdivided[:len(t_TOD)] + f_C['incineration_pulse'][:len(t_TOD)]

    #fontsize
    tfs=22
    ofs=18
    width=550              
    height=500
    fontfamily='helvetica'
    marker_line_color='black'
    marker_line_width=3
    linewidth=1
    gridwidth=1
    title_standoff=17.5
    #margins
    t=0  # Top margin (adjust as needed)
    b=0  # Bottom margin (adjust as needed)
    l=0  # Left margin (adjust as needed)
    r=0  # Right margin (adjust as needed)
    scale=2

    fig = go.Figure()

    # Net
    fig.add_trace(go.Scatter(x=t_TOD, y=1e-6*f_C['Net'][:len(t_TOD)], mode='lines', name='Net', line=dict(color='rgb(240, 74, 0)', dash='dash', width=marker_line_width)))

    # SOL
    fig.add_trace(go.Scatter(x=t_TOD, y=1e-6*f_neg[:len(t_TOD)], mode='lines', name='Biogenic and/or carbonation', line=dict(color='rgba(112, 193, 96, 0.99)', width=marker_line_width), fill='tozeroy',  fillcolor='rgba(112, 193, 96, 0.3)'))

    fig.add_trace(go.Scatter(x=t_TOD, y=1e-6*f_C['SOL'][:len(t_TOD)], mode='lines', name='Start-of-life non-biogenic', line=dict(color='rgba(192, 186, 177, 0.99)', width=marker_line_width), fill='tozeroy',  fillcolor='rgba(192, 186, 177, 0.3)'))

    fig.add_trace(go.Scatter(x=t_TOD, y=1e-6*f_C['EOL'][:len(t_TOD)], mode='lines', name='End-of-life non-biogenic', line=dict(color='rgba(55, 55, 55, 0.99)', width=marker_line_width), fill='tozeroy',  fillcolor='rgba(55, 55, 55, 0.3)'))

    fig.add_trace(go.Scatter(x=t_TOD, y=1e-6*f_C['CRE'][:len(t_TOD)], mode='lines', name='End-of-life substitution non-biogenic', line=dict(color='rgba(180, 96, 224, 0.99)', dash='dot', width=marker_line_width), fill='tozeroy',  fillcolor='rgba(180, 96, 224, 0.3)'))

    fig.add_trace(go.Scatter(x=t_TOD, y=1e-6*f_C_G_credit_notdivided[:len(t_TOD)], mode='lines', name='End-of-life substitution biogenic', line=dict(color='rgba(97, 167, 225, 0.99)', dash='dot', width=marker_line_width), fill='tozeroy',  fillcolor='rgba(97, 167, 225, 0.3)'))

    # Net
    fig.add_trace(go.Scatter(x=t_TOD, y=1e-6*f_C['Net'][:len(t_TOD)], mode='lines', name='Net', line=dict(color='rgb(240, 74, 0)', dash='dash', width=marker_line_width), showlegend=False))


 
    # Configure x-axis
    fig.update_xaxes(
        showline=True,             # Show x-axis line
        mirror=True,               # Mirror x-axis line
        linewidth=linewidth,               # Set x-axis line width
        linecolor='black',         # Set x-axis line color
        title='<b>                                       Years                                          </b>',    # Set x-axis title
        title_font=dict(
            family='Helvetica',
            size=tfs,
            color='black',
        ),
        title_standoff=title_standoff,
        tickfont=dict(
            family='Helvetica',
            size=ofs,
            color='black'
        ),
        #tickangle=-90,
        showgrid=True,             # Show x-axis gridlines
        gridwidth=gridwidth,       # Set x-axis grid line width
        gridcolor='lightgray',     # Set y-axis grid line color
        ticklabelstep=1,           # Set y-axis tick label step
        minor=dict(
            ticklen=0,
            tickcolor="lightgray",
            tickmode='auto',
            nticks=7,
            showgrid=True
        ),      # Set x-axis grid line color
        range=[0,299]
    )

    # Configure y-axis
    fig.update_yaxes(
        showline=True,              # Show y-axis line
        mirror=True,                # Mirror y-axis line
        linewidth=linewidth,        # Set y-axis line width
        linecolor='black',          # Set y-axis line color
        title='<b>CO<sub>2</sub> (Kt)</b>',  # Set y-axis title
        title_font=dict(
            family='Helvetica',
            size=tfs,
            color='black',
        ),
        title_standoff=title_standoff,
        tickfont=dict(
            family='Helvetica',
            size=ofs,
            color='black'
        ),
        showgrid=True,             # Show y-axis gridlines
        gridwidth=gridwidth,       # Set y-axis grid line width
        gridcolor='lightgray',     # Set y-axis grid line color
        ticklabelstep=1,           # Set y-axis tick label step
        minor=dict(
            ticklen=0,
            tickcolor="lightgray",
            tickmode='auto',
            nticks=5,
            showgrid=True
        ),
        range=[-0.500,1.500]
    )

    # Configure trace properties
    fig.update_traces(marker_line_color='black')

    # Configure legend
    fig.update_layout(
        #showlegend=False,
        legend=dict(
            traceorder="normal",
            orientation="h",
            yanchor="bottom",
            y=1.125,
            xanchor="right",
            x=1.125,
            font=dict(
                family=fontfamily,
                size=ofs,
                color="black"
            )
        )
    )

    # Configure the layout of the figure
    fig.update_layout(
        barmode='stack',          
        plot_bgcolor='white',       # Set plot background color
        width=width,                  # Set plot width
        height=height,                 # Set plot height
        margin=dict(
            t=t,  # Top margin (adjust as needed)
            b=b,  # Bottom margin (adjust as needed)
            l=l,  # Left margin (adjust as needed)
            r=r+25   # Right margin (adjust as needed)
        )
    )

    fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = [0, 50, 100, 150, 200, 250, 299,],
        ticktext = ['0', '50', '100', '150', '200', '250', '300']
    )
    )

    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black')

    fig.update_layout(
    title=building_type,
    title_x=0.13,
    title_y=0.6425,
    title_font=dict(size=tfs, color='black', family=f"{fontfamily},bold"))
    
    fig.show()

    directory = "../figures/decay/html"
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = "../figures/decay/img"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the figure as an html file
    fig.write_html("../figures/decay/html/CO2decay-"+building_type+".html")

    # Save the figure as an html file
    fig.write_image("../figures/decay/img/CO2decay-"+building_type+".jpg", scale=scale, engine='orca')

    return fig

def plot_methane_decay(building_type,f_M, t_TOD):

    #fontsize
    tfs=22
    ofs=18
    width=550              
    height=500
    fontfamily='helvetica'
    marker_line_color='black'
    marker_line_width=3
    linewidth=1
    gridwidth=1
    title_standoff=17.5
    #margins
    t=0  # Top margin (adjust as needed)
    b=0  # Bottom margin (adjust as needed)
    l=0  # Left margin (adjust as needed)
    r=0  # Right margin (adjust as needed)
    scale=2

    fig = go.Figure()

    # Net
    fig.add_trace(go.Scatter(x=t_TOD, y=1e-3*f_M['Net'][:len(t_TOD)], mode='lines', name='Net', line=dict(color='rgb(240, 74, 0)', dash='dash', width=marker_line_width)))

    # SOL
    fig.add_trace(go.Scatter(x=t_TOD, y=1e-3*f_M['EOL_bio_emissions_notdivided'][:len(t_TOD)], mode='lines', name='Biogenic', line=dict(color='rgba(112, 193, 96, 0.99)', width=marker_line_width), fill='tozeroy',  fillcolor='rgba(112, 193, 96, 0.3)'))

    fig.add_trace(go.Scatter(x=t_TOD, y=1e-3*f_M['SOL'][:len(t_TOD)], mode='lines', name='Start-of-life non-biogenic', line=dict(color='rgba(192, 186, 177, 0.99)', width=marker_line_width), fill='tozeroy',  fillcolor='rgba(192, 186, 177, 0.3)'))

    fig.add_trace(go.Scatter(x=t_TOD, y=1e-3*f_M['EOL'][:len(t_TOD)], mode='lines', name='End-of-life non-biogenic', line=dict(color='rgba(55, 55, 55, 0.99)', width=marker_line_width), fill='tozeroy',  fillcolor='rgba(55, 55, 55, 0.3)'))

    fig.add_trace(go.Scatter(x=t_TOD, y=1e-3*f_M['CRE'][:len(t_TOD)], mode='lines', name='End-of-life substitution non-biogenic', line=dict(color='rgba(180, 96, 224, 0.99)', dash='dot', width=marker_line_width), fill='tozeroy',  fillcolor='rgba(180, 96, 224, 0.3)'))

    fig.add_trace(go.Scatter(x=t_TOD, y=1e-3*f_M['EOL_bio_credit_notdivided'][:len(t_TOD)], mode='lines', name='End-of-life substitution biogenic', line=dict(color='rgba(97, 167, 225, 0.99)', dash='dot', width=marker_line_width), fill='tozeroy',  fillcolor='rgba(97, 167, 225, 0.3)'))

    # Net
    fig.add_trace(go.Scatter(x=t_TOD, y=1e-3*f_M['Net'][:len(t_TOD)], mode='lines', name='Net', line=dict(color='rgb(240, 74, 0)', dash='dash', width=marker_line_width), showlegend=False))


    # Configure x-axis
    fig.update_xaxes(
        showline=True,             # Show x-axis line
        mirror=True,               # Mirror x-axis line
        linewidth=linewidth,               # Set x-axis line width
        linecolor='black',         # Set x-axis line color
        title='<b>                                       Years                                          </b>',    # Set x-axis title
        title_font=dict(
            family='Helvetica',
            size=tfs,
            color='black',
        ),
        title_standoff=title_standoff,
        tickfont=dict(
            family='Helvetica',
            size=ofs,
            color='black'
        ),
        #tickangle=-90,
        showgrid=True,             # Show x-axis gridlines
        gridwidth=gridwidth,       # Set x-axis grid line width
        gridcolor='lightgray',     # Set y-axis grid line color
        ticklabelstep=1,           # Set y-axis tick label step
        minor=dict(
            ticklen=0,
            tickcolor="lightgray",
            tickmode='auto',
            nticks=7,
            showgrid=True
        ),      # Set x-axis grid line color
        range=[0,299]
    )

    # Configure y-axis
    fig.update_yaxes(
        showline=True,              # Show y-axis line
        mirror=True,                # Mirror y-axis line
        linewidth=linewidth,        # Set y-axis line width
        linecolor='black',          # Set y-axis line color
        title='<b>CH<sub>4</sub> (tonne)</b>',  # Set y-axis title
        title_font=dict(
            family='Helvetica',
            size=tfs,
            color='black',
        ),
        title_standoff=title_standoff,
        tickfont=dict(
            family='Helvetica',
            size=ofs,
            color='black'
        ),
        showgrid=True,             # Show y-axis gridlines
        gridwidth=gridwidth,       # Set y-axis grid line width
        gridcolor='lightgray',     # Set y-axis grid line color
        ticklabelstep=1,           # Set y-axis tick label step
        minor=dict(
            ticklen=0,
            tickcolor="lightgray",
            tickmode='auto',
            nticks=5,
            showgrid=True
        ),
        range=[-2,12]
    )

    # Configure trace properties
    fig.update_traces(marker_line_color='black')

    # Configure legend
    fig.update_layout(
        #showlegend=False,
        legend=dict(
            traceorder="normal",
            orientation="v",
            yanchor="bottom",
            y=1.125,
            xanchor="right",
            x=1.125,
            font=dict(
                family=fontfamily,
                size=ofs,
                color="black"
            )
        )
    )

    # Configure the layout of the figure
    fig.update_layout(
        barmode='stack',          
        plot_bgcolor='white',       # Set plot background color
        width=width,                  # Set plot width
        height=height,                 # Set plot height
        margin=dict(
            t=t,  # Top margin (adjust as needed)
            b=b,  # Bottom margin (adjust as needed)
            l=l,  # Left margin (adjust as needed)
            r=r+25   # Right margin (adjust as needed)
        )
    )

    fig.update_layout(
    xaxis = dict(
        tickmode = 'array',
        tickvals = [0, 50, 100, 150, 200, 250, 299,],
        ticktext = ['0', '50', '100', '150', '200', '250', '300']
    )
    )

    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black')

    fig.update_layout(
    title=building_type,
    title_x=0.1075,
    title_y=0.6425,
    title_font=dict(size=tfs, color='black', family=fontfamily))

    fig.show()

    directory = "../figures/decay/html"
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = "../figures/decay/img"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the figure as an html file
    fig.write_html("../figures/decay/html/CH4decay-"+building_type+".html")

    # Save the figure as an html file
    fig.write_image("../figures/decay/img/CH4decay-"+building_type+".jpg", scale=scale, engine='orca')

    return fig
