import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

#figure layout
tfs=18
ofs=16
width=900               
height=600
fontfamily='helvetica'
marker_line_color='black'
marker_line_width=0.5
linewidth=1
gridwidth=1
title_standoff=17.5
#margins
t=0  # Top margin (adjust as needed)
b=0  # Bottom margin (adjust as needed)
l=0  # Left margin (adjust as needed)
r=0  # Right margin (adjust as needed)
scale=2

#GWP results
cf = 1e-6 #conversion factor from t to Kt

df = pd.read_csv('..\output\GWP_Results.csv', index_col=0)
df100stack = cf* df[104:117]
df100stacksta = cf* df [26:39]
df200stack = cf* df[117:130]
df200stacksta = cf* df[39:52]

df100errors = df100stack.iloc[:, -2:]
df100errorssta = df100stacksta.iloc[:, -2:]
df200errors = df200stack.iloc[:, -2:]
df200errorssta = df200stacksta.iloc[:, -2:]

#GWP100 dynamic
variables100 = df100stack.index.tolist()
CO2_100_nonbio = df100stack ['CO2_nonbio'].tolist()
CO2_100_bio = df100stack ['CO2_bio'].tolist()
CH4100 = df100stack ['CH4'].tolist()
N2O100 = df100stack ['N2O'].tolist()
Life_carbonation100 = df100stack ['Life_carbonation'].tolist()
EOL_carbonation100 = df100stack ['EOL_carbonation'].tolist()
MN100 = df100stack ['MN'].tolist()
Net100 = df100stack ['Net'].tolist()
Low_Error100 = df100errors ['Low_Error'].tolist()
High_Error100 = df100errors ['High_Error'].tolist()

#GWP100 static
variablessta100 = df100stacksta.index.tolist()
CO2_sta100_nonbio = df100stacksta ['CO2_nonbio'].tolist()
CO2_sta100_bio = df100stacksta ['CO2_bio'].tolist()
CH4sta100 = df100stacksta ['CH4'].tolist()
N2Osta100 = df100stacksta ['N2O'].tolist()
Life_carbonationsta100 = df100stacksta ['Life_carbonation'].tolist()
EOL_carbonationsta100 = df100stacksta ['EOL_carbonation'].tolist()
MNsta100 = df100stacksta ['MN'].tolist()
Netsta100 = df100stacksta ['Net'].tolist()
Low_Errorsta100 = df100errorssta ['Low_Error'].tolist()
High_Errorsta100 = df100errorssta ['High_Error'].tolist()

#GWP200 dynamic
variables200 = df200stack.index.tolist()
CO2_200_nonbio = df200stack ['CO2_nonbio'].tolist()
CO2_200_bio = df200stack ['CO2_bio'].tolist()
CH4200 = df200stack ['CH4'].tolist()
N2O200 = df200stack ['N2O'].tolist()
Life_carbonation200 = df200stack ['Life_carbonation'].tolist()
EOL_carbonation200 = df200stack ['EOL_carbonation'].tolist()
MN200 = df200stack ['MN'].tolist()
Net200 = df200stack ['Net'].tolist()
Low_Error200 = df200errors ['Low_Error'].tolist()
High_Error200 = df200errors ['High_Error'].tolist()

#GWP200 static
variablessta200 = df200stacksta.index.tolist()
CO2_sta200_nonbio = df200stacksta ['CO2_nonbio'].tolist()
CO2_sta200_bio = df200stacksta ['CO2_bio'].tolist()
CH4sta200 = df200stacksta ['CH4'].tolist()
N2Osta200 = df200stacksta ['N2O'].tolist()
Life_carbonationsta200 = df200stacksta ['Life_carbonation'].tolist()
EOL_carbonationsta200 = df200stacksta ['EOL_carbonation'].tolist()
MNsta200 = df200stacksta ['MN'].tolist()
Netsta200 = df200stacksta ['Net'].tolist()
Low_Errorsta200 = df200errorssta ['Low_Error'].tolist()
High_Errorsta200 = df200errorssta ['High_Error'].tolist()

#colors
CO2nonbiodyn_color='rgb(227, 218, 201)'
CO2biodyn_color='rgb(172, 225, 175)'
CO2nonbiosta_color='rgba(227, 218, 201, 0.5)'
CO2biosta_color='rgba(172, 225, 175, 0.5)'
CH4dyn_color='rgb(255, 127, 80)'
CH4sta_color='rgba(255, 127, 80, 0.5)'
N2Odyn_color='rgb(255, 204, 51)' 
N2Osta_color='rgba(255, 204, 51, 0.5)'
Lifecdyn_color='rgb(241, 156, 187)'
Lifecsta_color='rgba(241, 156, 187, 0.5)'
Eolcdyn_color='rgb(178, 132, 190)'
Eolcsta_color='rgba(178, 132, 190, 0.5)'
Netgwpdyn_color='rgb(237, 41, 57)'
Netgwpsta_color='rgba(237, 41, 57, 0.5)'

# Plot GWP 100
# Define your configuration for traces
trace_configs = [
    {
        'type': 'scatter',
        'x': variables100,
        'y': Net100,
        'name': 'Net',
        'mode': 'markers',
        'marker_symbol': 'circle',
        'marker_color': Netgwpdyn_color,
        'marker_size': 5,
        'error_y': dict(
            type='data',
            array=High_Error100,
            arrayminus=Low_Error100,
            visible=True
        )
    },
    {
        'type': 'scatter',
        'x': variablessta100,
        'y': Netsta100,
        'name': 'Net',
        'mode': 'markers',
        'marker_symbol': 'circle',
        'marker_color': Netgwpsta_color,
        'marker_size': 5,
        'error_y': dict(
            type='data',
            array=High_Errorsta100,
            arrayminus=Low_Errorsta100,
            visible=True
        )
    },
    {
        'type': 'bar',
        'x': variables100,
        'y': CO2_100_nonbio,
        'name': 'Non-biogenic CO<sub>2</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CO2nonbiodyn_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variablessta100,
        'y': CO2_sta100_nonbio,
        'name': 'Non-biogenic CO<sub>2</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CO2nonbiosta_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variables100,
        'y': CO2_100_bio,
        'name': 'Biogenic CO<sub>2</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CO2biodyn_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variablessta100,
        'y': CO2_sta100_bio,
        'name': 'Biogenic CO<sub>2</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CO2biosta_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variables100,
        'y': Life_carbonation100,
        'name': 'Life carbonation',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': Lifecdyn_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variablessta100,
        'y': Life_carbonationsta100,
        'name': 'Life carbonation',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': Lifecsta_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variables100,
        'y': EOL_carbonation100,
        'name': 'End-of-life carbonation',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': Eolcdyn_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variablessta100,
        'y': EOL_carbonationsta100,
        'name': 'End-of-life carbonation',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': Eolcsta_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variables100,
        'y': CH4100,
        'name': 'CH<sub>4</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CH4dyn_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variablessta100,
        'y': CH4sta100,
        'name': 'CH<sub>4</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CH4sta_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variables100,
        'y': N2O100,
        'name': 'N<sub>2</sub>O',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': N2Odyn_color,
        'marker_line_width': marker_line_width
    },
    {
        'type': 'bar',
        'x': variablessta100,
        'y': N2Osta100,
        'name': 'N<sub>2</sub>O',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': N2Osta_color,
        'marker_line_width': marker_line_width
    }
]

# Create the figure
fig = go.Figure()

# Add traces to the figure using the configurations
for trace in trace_configs:
    if trace['type'] == 'scatter':
        fig.add_trace(go.Scatter(
            x=trace['x'],
            y=trace['y'],
            name=trace['name'],
            mode=trace['mode'],
            marker_symbol=trace['marker_symbol'],
            marker_color=trace['marker_color'],
            marker_size=trace['marker_size'],
            opacity=1,
            error_y=trace.get('error_y')
        ))
    elif trace['type'] == 'bar':
        fig.add_trace(go.Bar(
            x=trace['x'],
            y=trace['y'],
            name=trace['name'],
            textposition=trace['textposition'],
            textfont_color=trace['textfont_color'],
            textfont_size=trace['textfont_size'],
            marker_color=trace['marker_color'],
            marker_line_width=trace['marker_line_width'],
            opacity=1
        ))

# Configure x-axis
fig.update_xaxes(
    showline=True,
    mirror=True,
    linewidth=linewidth,
    linecolor='black',
    title='<b>                                       Scenarios                                       </b>',
    title_font=dict(family='Helvetica', size=tfs, color='black'),
    title_standoff=title_standoff,
    tickfont=dict(family='Helvetica', size=ofs, color='black'),
    tickangle=-90,
    showgrid=False,
    gridwidth=gridwidth,
    gridcolor='lightgray',
    ticklabelstep=1,
    minor=dict(
        ticklen=0,
        tickcolor="lightgray",
        tickmode='auto',
        nticks=3,
        showgrid=False
    )
)

# Configure y-axis
fig.update_yaxes(
    showline=True,
    mirror=True,
    linewidth=linewidth,
    linecolor='black',
    title='<b>CO<sub>2</sub>-eq. (Kt)</b>',
    title_font=dict(family='Helvetica', size=tfs, color='black'),
    title_standoff=title_standoff,
    tickfont=dict(family='Helvetica', size=ofs, color='black'),
    showgrid=True,
    gridwidth=gridwidth,
    gridcolor='lightgray',
    ticklabelstep=1,
    minor=dict(
        ticklen=0,
        tickcolor="gray",
        tickmode='auto',
        nticks=19,
        showgrid=True
    ),
    range=[-1, 3]
)

# Configure trace properties
fig.update_traces(marker_line_color=marker_line_color)

# Configure legend
fig.update_layout(
    legend=dict(
        entrywidth=0.35,
        entrywidthmode='fraction',
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(family=fontfamily, size=tfs, color="black")
    )
)

# Configure layout of the figure
fig.update_layout(
    barmode='relative',
    bargap=0,
    plot_bgcolor='white',
    width=width + 25,
    height=height,
    margin=dict(t=t + 225, b=b, l=l, r=r)
)

# Add annotation
fig.add_annotation(
    x=0.5285, y=1.80,
    text='<b>     GWP100<sub>dynamic</sub>           <sub>   </sub>                       GWP100<sub>static</sub>',
    showarrow=False,
    xref='paper',
    yref='paper',
    align='left',
    font=dict(family=fontfamily, size=tfs, color="black")
)

# Configure title
fig.update_layout(
    title='<b>(a) GWP 100 years<b>',
    title_x=0.06,
    title_y=0.655,
    title_font=dict(size=tfs, color='black', family=fontfamily),
)

# Update x-axis categories
fig.update_xaxes(categoryorder='array', categoryarray=[
    'BAU_C1_Dynamic_100', 'BAU_C1_Static_100', 'f1',
    'BAU_C2_Dynamic_100', 'BAU_C2_Static_100', 'f2',
    'BAU_C3_Dynamic_100', 'BAU_C3_Static_100', 'f3',
    'LC3_C1_Dynamic_100', 'LC3_C1_Static_100', 'f4',
    'LC3_C2_Dynamic_100', 'LC3_C2_Static_100', 'f5',
    'LC3_C3_Dynamic_100', 'LC3_C3_Static_100', 'f6',
    'EST_T1_Dynamic_100', 'EST_T1_Static_100', 'f7',
    'EST_T2_Dynamic_100', 'EST_T2_Static_100', 'f8',
    'EST_T3_Dynamic_100', 'EST_T3_Static_100', 'f9',
    'EST_T4_Dynamic_100', 'EST_T4_Static_100', 'f10',
    'EST_T5_Dynamic_100', 'EST_T5_Static_100', 'f11',
    'EST_T6_Dynamic_100', 'EST_T6_Static_100', 'f12',
    'EST_T7_Dynamic_100', 'EST_T7_Static_100'
])

fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=[
            'BAU_C1_Dynamic_100', 'BAU_C2_Dynamic_100', 'BAU_C3_Dynamic_100',
            'LC3_C1_Dynamic_100', 'LC3_C2_Dynamic_100', 'LC3_C3_Dynamic_100',
            'EST_T1_Dynamic_100', 'EST_T2_Dynamic_100', 'EST_T3_Dynamic_100',
            'EST_T4_Dynamic_100', 'EST_T5_Dynamic_100', 'EST_T6_Dynamic_100',
            'EST_T7_Dynamic_100'
        ],
        ticktext=[
            'BAU-C1', 'BAU-C2', 'BAU-C3', 'LC<sup>3</sup>-C1', 'LC<sup>3</sup>-C2',
            'LC<sup>3</sup>-C3', 'EST-T1', 'EST-T2', 'EST-T3', 'EST-T4',
            'EST-T5', 'EST-T6', 'EST-T7'
        ]
    )
)

fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black')

# Show the figure
fig.show()

directory = "../figures/html"
if not os.path.exists(directory):
    os.makedirs(directory)

directory = "../figures/img"
if not os.path.exists(directory):
    os.makedirs(directory)

# Save the figure as an HTML file
fig.write_html("../figures/html/gwp100.html")

# Save the figure as an HTML file
fig.write_image("../figures/img/gwp100.jpg", scale=scale, engine='orca')

# Plot GWP 200
# Define trace configurations
trace_configs = [
    {
        'type': 'scatter',
        'x': variables200,
        'y': Net200,
        'name': 'Net',
        'mode': 'markers',
        'marker_symbol': 'circle',
        'marker_color': Netgwpdyn_color,
        'marker_size': 5,
        'opacity': 1,
        'error_y': dict(
            type='data',
            array=High_Error200,
            arrayminus=Low_Error200,
            visible=True
        )
    },
    {
        'type': 'scatter',
        'x': variablessta200,
        'y': Netsta200,
        'name': 'Net',
        'mode': 'markers',
        'marker_symbol': 'circle',
        'marker_color': Netgwpsta_color,
        'marker_size': 5,
        'opacity': 1,
        'error_y': dict(
            type='data',
            array=High_Error200,
            arrayminus=Low_Error200,
            visible=True
        )
    },
    {
        'type': 'bar',
        'x': variables200,
        'y': CO2_200_nonbio,
        'name': 'Non-biogenic CO<sub>2</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CO2nonbiodyn_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variablessta200,
        'y': CO2_sta200_nonbio,
        'name': 'Non-biogenic CO<sub>2</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CO2nonbiosta_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variables200,
        'y': CO2_200_bio,
        'name': 'Biogenic CO<sub>2</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CO2biodyn_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variablessta200,
        'y': CO2_sta200_bio,
        'name': 'Biogenic CO<sub>2</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CO2biosta_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variables200,
        'y': Life_carbonation200,
        'name': 'Life carbonation',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': Lifecdyn_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variablessta200,
        'y': Life_carbonationsta200,
        'name': 'Life carbonation',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': Lifecsta_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variables200,
        'y': EOL_carbonation200,
        'name': 'End-of-life carbonation',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': Eolcdyn_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variablessta200,
        'y': EOL_carbonationsta200,
        'name': 'End-of-life carbonation',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': Eolcsta_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variables200,
        'y': CH4200,
        'name': 'CH<sub>4</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CH4dyn_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variablessta200,
        'y': CH4sta200,
        'name': 'CH<sub>4</sub>',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': CH4sta_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variables200,
        'y': N2O200,
        'name': 'N<sub>2</sub>O',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': N2Odyn_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    },
    {
        'type': 'bar',
        'x': variablessta200,
        'y': N2Osta200,
        'name': 'N<sub>2</sub>O',
        'textposition': 'inside',
        'textfont_color': 'black',
        'textfont_size': ofs,
        'marker_color': N2Osta_color,
        'marker_line_width': marker_line_width,
        'opacity': 1
    }
]

# Create figure
fig = go.Figure()

# Add traces
for trace in trace_configs:
    if trace['type'] == 'scatter':
        fig.add_trace(go.Scatter(
            x=trace['x'],
            y=trace['y'],
            name=trace['name'],
            mode=trace['mode'],
            marker_symbol=trace['marker_symbol'],
            marker_color=trace['marker_color'],
            marker_size=trace['marker_size'],
            opacity=trace['opacity'],
            error_y=trace['error_y']
        ))
    elif trace['type'] == 'bar':
        fig.add_trace(go.Bar(
            x=trace['x'],
            y=trace['y'],
            name=trace['name'],
            textposition=trace['textposition'],
            textfont_color=trace['textfont_color'],
            textfont_size=trace['textfont_size'],
            marker_color=trace['marker_color'],
            marker_line_width=trace['marker_line_width'],
            opacity=trace['opacity']
        ))

# Configure x-axis
fig.update_xaxes(
    showline=True,
    mirror=True,
    linewidth=linewidth,
    linecolor='black',
    title='<b>                                       Scenarios                                       </b>',
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
    tickangle=-90,
    showgrid=False,
    gridwidth=gridwidth,
    gridcolor='lightgray',
    ticklabelstep=1,
    minor=dict(
        ticklen=0,
        tickcolor="lightgray",
        tickmode='auto',
        nticks=3,
        showgrid=False
    )
)

# Configure y-axis
fig.update_yaxes(
    showline=True,
    mirror=True,
    linewidth=linewidth,
    linecolor='black',
    title='<b>CO<sub>2</sub>-eq. (Kt)</b>',
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
    showgrid=True,
    gridwidth=gridwidth,
    gridcolor='lightgray',
    ticklabelstep=1,
    minor=dict(
        ticklen=0,
        tickcolor="gray",
        tickmode='auto',
        nticks=19,
        showgrid=True
    ),
    range=[-1,3]
)

# Configure trace properties
fig.update_traces(marker_line_color=marker_line_color)

# Configure legend
fig.update_layout(
    legend=dict(
        entrywidth=0.35,
        entrywidthmode='fraction',
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(
            family=fontfamily,
            size=tfs,
            color="black"
        )
    )
)

# Configure the layout of the figure
fig.update_layout(
    barmode='relative',
    bargap=0,
    plot_bgcolor='white',
    width=width+25,
    height=height,
    margin=dict(
        t=t+225,
        b=b,
        l=l,
        r=r
    )
)

# Add annotation
fig.add_annotation(
    x=0.5265, y=1.80,
    text='<b>      GWP200<sub>dynamic</sub>           <sub>    </sub>                      GWP200<sub>static</sub>',
    showarrow=False,
    xref='paper',
    yref='paper',
    align='left',
    font=dict(
        family=fontfamily,
        size=tfs,
        color="black"
    ),
)

# Update title and x-axis categories
fig.update_layout(
    title='<b>(b) GWP 200 years<b>',
    title_x=0.06,
    title_y=0.655,
    title_font=dict(size=tfs, color='black', family=fontfamily),
)

fig.update_xaxes(categoryorder='array', categoryarray=[
    'BAU_C1_Dynamic_200', 'BAU_C1_Static_200', 'f1',
    'BAU_C2_Dynamic_200', 'BAU_C2_Static_200', 'f2',
    'BAU_C3_Dynamic_200', 'BAU_C3_Static_200', 'f3',
    'LC3_C1_Dynamic_200', 'LC3_C1_Static_200', 'f4',
    'LC3_C2_Dynamic_200', 'LC3_C2_Static_200', 'f5',
    'LC3_C3_Dynamic_200', 'LC3_C3_Static_200', 'f6',
    'EST_T1_Dynamic_200', 'EST_T1_Static_200', 'f7',
    'EST_T2_Dynamic_200', 'EST_T2_Static_200', 'f8',
    'EST_T3_Dynamic_200', 'EST_T3_Static_200', 'f9',
    'EST_T4_Dynamic_200', 'EST_T4_Static_200', 'f10',
    'EST_T5_Dynamic_200', 'EST_T5_Static_200', 'f11',
    'EST_T6_Dynamic_200', 'EST_T6_Static_200', 'f12',
    'EST_T7_Dynamic_200', 'EST_T7_Static_200'
])

fig.update_xaxes(
    tickmode='array',
    tickvals=[
        'BAU_C1_Dynamic_200', 'BAU_C2_Dynamic_200', 'BAU_C3_Dynamic_200',
        'LC3_C1_Dynamic_200', 'LC3_C2_Dynamic_200', 'LC3_C3_Dynamic_200',
        'EST_T1_Dynamic_200', 'EST_T2_Dynamic_200', 'EST_T3_Dynamic_200',
        'EST_T4_Dynamic_200', 'EST_T5_Dynamic_200', 'EST_T6_Dynamic_200',
        'EST_T7_Dynamic_200'
    ],
    ticktext=[
        'BAU-C1', 'BAU-C2', 'BAU-C3', 'LC<sup>3</sup>-C1', 'LC<sup>3</sup>-C2', 'LC<sup>3</sup>-C3',
        'EST-T1', 'EST-T2', 'EST-T3', 'EST-T4', 'EST-T5', 'EST-T6', 'EST-T7'
    ]
)

fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black')

# Show the figure
fig.show()

directory = "../figures/html"
if not os.path.exists(directory):
    os.makedirs(directory)

directory = "../figures/img"
if not os.path.exists(directory):
    os.makedirs(directory)

# Save the figure as an HTML file
fig.write_html("../figures/html/gwp200.html")

# Save the figure as an HTML file
fig.write_image("../figures/img/gwp200.jpg", scale=scale, engine='orca')
