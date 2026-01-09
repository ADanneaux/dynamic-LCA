import pandas as pd
import plotly.graph_objects as go
import os

#figure layout
tfs=22
ofs=18
width=1225                
height=975
fontfamily='helvetica'
marker_line_color='black'
marker_line_width=1.25
linewidth=1.25
gridwidth=1.25
title_standoff=17.5
#margins
t=0  # Top margin (adjust as needed)
b=0  # Bottom margin (adjust as needed)
l=0  # Left margin (adjust as needed)
r=0  # Right margin (adjust as needed)
scale=2

# AGTP results
AGTP = pd.read_csv('../../output/results/AGTP_results_World.csv')
x = [i for i in range(60000)]
x_rev = x[::-1]

# Define the categories and values
buildings = ['BAU_C1', 'BAU_C2', 'BAU_C3', 'LC3_C1', 'LC3_C2', 'LC3_C3', 'EST_T1', 'EST_T2', 'EST_T3', 'EST_T4',
             'EST_T5', 'EST_T6', 'EST_T7']
exposure_values = ['0.25']  # ['0.25', '5', '10']

# Loop through each category and value to compute min and max
for category in buildings:
    # Prepare to compute row-wise min and max for SSP1, SSP2, SSP3
    cols = [f"{category}_{value}_SSP1" for value in exposure_values] + \
           [f"{category}_{value}_SSP2" for value in exposure_values] + \
           [f"{category}_{value}_SSP3" for value in exposure_values]

    cols = [col for col in cols if col in AGTP.columns]

    # Compute the row-wise minimum and maximum
    AGTP[f"{category}_lower"] = AGTP[cols].min(axis=1)
    AGTP[f"{category}_upper"] = AGTP[cols].max(axis=1)

cf = 1

for category in buildings:
    for value in exposure_values:
        clean_value = value.replace('.', '')
        exec(f"{category}_{clean_value}_SSP1 = [i * cf for i in AGTP['{category}_{value}_SSP1'].tolist()]")
        exec(f"{category}_{clean_value}_SSP2 = [i * cf for i in AGTP['{category}_{value}_SSP2'].tolist()]")
        exec(f"{category}_{clean_value}_SSP3 = [i * cf for i in AGTP['{category}_{value}_SSP3'].tolist()]")
        exec(f"{category}_upper = [i * cf for i in AGTP['{category}_upper'].tolist()]")
        exec(f"{category}_lower = [i * cf for i in AGTP['{category}_lower'].tolist()][::-1]")

# color
BAU_C1_color_l = 'rgba(124, 9, 2, 0.9)'
BAU_C1_color_f = 'rgba(124, 9, 2, 0.15)'

BAU_C2_color_l = 'rgba(255, 8, 0, 0.9)'
BAU_C2_color_f = 'rgba(255, 8, 0, 0.15)'

BAU_C3_color_l = 'rgba(191, 79, 81, 0.9)'
BAU_C3_color_f = 'rgba(191, 79, 81, 0.15)'

LC3_C1_color_l = 'rgba(0, 46, 131, 0.9)'
LC3_C1_color_f = 'rgba(0, 46, 131, 0.15)'

LC3_C2_color_l = 'rgba(49, 140, 231, 0.9)'
LC3_C2_color_f = 'rgba(49, 140, 231, 0.15)'

LC3_C3_color_l = 'rgba(175, 219, 245, 0.9)'
LC3_C3_color_f = 'rgba(175, 219, 245, 0.15)'

EST_T1_color_l = 'rgba(133, 176, 154, 0.9)'
EST_T1_color_f = 'rgba(133, 176, 154, 0.15)'

EST_T2_color_l = 'rgba(255, 88, 0, 0.9)'
EST_T2_color_f = 'rgba(255, 88, 0, 0.15)'

EST_T3_color_l = 'rgba(181, 126, 220, 0.9)'
EST_T3_color_f = 'rgba(181, 126, 220, 0.15)'

EST_T4_color_l = 'rgba(179, 155, 110, 0.9)'
EST_T4_color_f = 'rgba(179, 155, 110, 0.15)'

EST_T5_color_l = 'rgba(197, 75, 140, 0.9)'
EST_T5_color_f = 'rgba(197, 75, 140, 0.15)'

EST_T6_color_l = 'rgba(131, 134, 145, 0.9)'
EST_T6_color_f = 'rgba(131, 134, 145, 0.15)'

EST_T7_color_l = 'rgba(240, 180, 0, 0.9)'
EST_T7_color_f = 'rgba(240, 180, 0, 0.15)'

# Data for traces
traces_fill = [
    {'name': 'BAU-C1', 'x': x + x_rev, 'y': BAU_C1_upper + BAU_C1_lower, 'fillcolor': BAU_C1_color_f,
     'line_color': BAU_C1_color_l},
    {'name': 'BAU-C2', 'x': x + x_rev, 'y': BAU_C2_upper + BAU_C2_lower, 'fillcolor': BAU_C2_color_f,
     'line_color': BAU_C2_color_l},
    {'name': 'BAU-C3', 'x': x + x_rev, 'y': BAU_C3_upper + BAU_C3_lower, 'fillcolor': BAU_C3_color_f,
     'line_color': BAU_C3_color_l},
    {'name': 'LC<sup>3</sup>-C1', 'x': x + x_rev, 'y': LC3_C1_upper + LC3_C1_lower, 'fillcolor': LC3_C1_color_f,
     'line_color': LC3_C1_color_l},
    {'name': 'LC<sup>3</sup>-C2', 'x': x + x_rev, 'y': LC3_C2_upper + LC3_C2_lower, 'fillcolor': LC3_C2_color_f,
     'line_color': LC3_C2_color_l},
    {'name': 'LC<sup>3</sup>-C3', 'x': x + x_rev, 'y': LC3_C3_upper + LC3_C3_lower, 'fillcolor': LC3_C3_color_f,
     'line_color': LC3_C3_color_l},
    {'name': 'EST-T1', 'x': x + x_rev, 'y': EST_T1_upper + EST_T1_lower, 'fillcolor': EST_T1_color_f,
     'line_color': EST_T1_color_l},
    {'name': 'EST-T2', 'x': x + x_rev, 'y': EST_T2_upper + EST_T2_lower, 'fillcolor': EST_T2_color_f,
     'line_color': EST_T2_color_l},
    {'name': 'EST-T3', 'x': x + x_rev, 'y': EST_T3_upper + EST_T3_lower, 'fillcolor': EST_T3_color_f,
     'line_color': EST_T3_color_l},
    {'name': 'EST-T4', 'x': x + x_rev, 'y': EST_T4_upper + EST_T4_lower, 'fillcolor': EST_T4_color_f,
     'line_color': EST_T4_color_l},
    {'name': 'EST-T5', 'x': x + x_rev, 'y': EST_T5_upper + EST_T5_lower, 'fillcolor': EST_T5_color_f,
     'line_color': EST_T5_color_l},
    {'name': 'EST-T6', 'x': x + x_rev, 'y': EST_T6_upper + EST_T6_lower, 'fillcolor': EST_T6_color_f,
     'line_color': EST_T6_color_l},
    {'name': 'EST-T7', 'x': x + x_rev, 'y': EST_T7_upper + EST_T7_lower, 'fillcolor': EST_T7_color_f,
     'line_color': EST_T7_color_l},
]

traces_line = [
    {'name': 'BAU-C1', 'x': x, 'y': BAU_C1_025_SSP2, 'fillcolor': BAU_C1_color_f, 'line_color': BAU_C1_color_l},
    {'name': 'BAU-C2', 'x': x, 'y': BAU_C2_025_SSP2, 'fillcolor': BAU_C2_color_f, 'line_color': BAU_C2_color_l},
    {'name': 'BAU-C3', 'x': x, 'y': BAU_C3_025_SSP2, 'fillcolor': BAU_C3_color_f, 'line_color': BAU_C3_color_l},
    {'name': 'LC<sup>3</sup>-C1', 'x': x, 'y': LC3_C1_025_SSP2, 'fillcolor': LC3_C1_color_f,
     'line_color': LC3_C1_color_l},
    {'name': 'LC<sup>3</sup>-C2', 'x': x, 'y': LC3_C2_025_SSP2, 'fillcolor': LC3_C2_color_f,
     'line_color': LC3_C2_color_l},
    {'name': 'LC<sup>3</sup>-C3', 'x': x, 'y': LC3_C3_025_SSP2, 'fillcolor': LC3_C3_color_f,
     'line_color': LC3_C3_color_l},
    {'name': 'EST-T1', 'x': x, 'y': EST_T1_025_SSP2, 'fillcolor': EST_T1_color_f, 'line_color': EST_T1_color_l},
    {'name': 'EST-T2', 'x': x, 'y': EST_T2_025_SSP2, 'fillcolor': EST_T2_color_f, 'line_color': EST_T2_color_l},
    {'name': 'EST-T3', 'x': x, 'y': EST_T3_025_SSP2, 'fillcolor': EST_T3_color_f, 'line_color': EST_T3_color_l},
    {'name': 'EST-T4', 'x': x, 'y': EST_T4_025_SSP2, 'fillcolor': EST_T4_color_f, 'line_color': EST_T4_color_l},
    {'name': 'EST-T5', 'x': x, 'y': EST_T5_025_SSP2, 'fillcolor': EST_T5_color_f, 'line_color': EST_T5_color_l},
    {'name': 'EST-T6', 'x': x, 'y': EST_T6_025_SSP2, 'fillcolor': EST_T6_color_f, 'line_color': EST_T6_color_l},
    {'name': 'EST-T7', 'x': x, 'y': EST_T7_025_SSP2, 'fillcolor': EST_T7_color_f, 'line_color': EST_T7_color_l},
]

traces_line_ssp1 = [
    {'name': 'BAU-C1', 'x': x, 'y': BAU_C1_025_SSP1, 'fillcolor': BAU_C1_color_f, 'line_color': BAU_C1_color_f},
    {'name': 'BAU-C2', 'x': x, 'y': BAU_C2_025_SSP1, 'fillcolor': BAU_C2_color_f, 'line_color': BAU_C2_color_f},
    {'name': 'BAU-C3', 'x': x, 'y': BAU_C3_025_SSP1, 'fillcolor': BAU_C3_color_f, 'line_color': BAU_C3_color_f},
    {'name': 'LC<sup>3</sup>-C1', 'x': x, 'y': LC3_C1_025_SSP1, 'fillcolor': LC3_C1_color_f,
     'line_color': LC3_C1_color_f},
    {'name': 'LC<sup>3</sup>-C2', 'x': x, 'y': LC3_C2_025_SSP1, 'fillcolor': LC3_C2_color_f,
     'line_color': LC3_C2_color_f},
    {'name': 'LC<sup>3</sup>-C3', 'x': x, 'y': LC3_C3_025_SSP1, 'fillcolor': LC3_C3_color_f,
     'line_color': LC3_C3_color_f},
    {'name': 'EST-T1', 'x': x, 'y': EST_T1_025_SSP1, 'fillcolor': EST_T1_color_f, 'line_color': EST_T1_color_f},
    {'name': 'EST-T2', 'x': x, 'y': EST_T2_025_SSP1, 'fillcolor': EST_T2_color_f, 'line_color': EST_T2_color_f},
    {'name': 'EST-T3', 'x': x, 'y': EST_T3_025_SSP1, 'fillcolor': EST_T3_color_f, 'line_color': EST_T3_color_f},
    {'name': 'EST-T4', 'x': x, 'y': EST_T4_025_SSP1, 'fillcolor': EST_T4_color_f, 'line_color': EST_T4_color_f},
    {'name': 'EST-T5', 'x': x, 'y': EST_T5_025_SSP1, 'fillcolor': EST_T5_color_f, 'line_color': EST_T5_color_f},
    {'name': 'EST-T6', 'x': x, 'y': EST_T6_025_SSP1, 'fillcolor': EST_T6_color_f, 'line_color': EST_T6_color_f},
    {'name': 'EST-T7', 'x': x, 'y': EST_T7_025_SSP1, 'fillcolor': EST_T7_color_f, 'line_color': EST_T7_color_f},
]

traces_line_ssp3 = [
    {'name': 'BAU-C1', 'x': x, 'y': BAU_C1_025_SSP3, 'fillcolor': BAU_C1_color_f, 'line_color': BAU_C1_color_f},
    {'name': 'BAU-C2', 'x': x, 'y': BAU_C2_025_SSP3, 'fillcolor': BAU_C2_color_f, 'line_color': BAU_C2_color_f},
    {'name': 'BAU-C3', 'x': x, 'y': BAU_C3_025_SSP3, 'fillcolor': BAU_C3_color_f, 'line_color': BAU_C3_color_f},
    {'name': 'LC<sup>3</sup>-C1', 'x': x, 'y': LC3_C1_025_SSP3, 'fillcolor': LC3_C1_color_f,
     'line_color': LC3_C1_color_f},
    {'name': 'LC<sup>3</sup>-C2', 'x': x, 'y': LC3_C2_025_SSP3, 'fillcolor': LC3_C2_color_f,
     'line_color': LC3_C2_color_f},
    {'name': 'LC<sup>3</sup>-C3', 'x': x, 'y': LC3_C3_025_SSP3, 'fillcolor': LC3_C3_color_f,
     'line_color': LC3_C3_color_f},
    {'name': 'EST-T1', 'x': x, 'y': EST_T1_025_SSP3, 'fillcolor': EST_T1_color_f, 'line_color': EST_T1_color_f},
    {'name': 'EST-T2', 'x': x, 'y': EST_T2_025_SSP3, 'fillcolor': EST_T2_color_f, 'line_color': EST_T2_color_f},
    {'name': 'EST-T3', 'x': x, 'y': EST_T3_025_SSP3, 'fillcolor': EST_T3_color_f, 'line_color': EST_T3_color_f},
    {'name': 'EST-T4', 'x': x, 'y': EST_T4_025_SSP3, 'fillcolor': EST_T4_color_f, 'line_color': EST_T4_color_f},
    {'name': 'EST-T5', 'x': x, 'y': EST_T5_025_SSP3, 'fillcolor': EST_T5_color_f, 'line_color': EST_T5_color_f},
    {'name': 'EST-T6', 'x': x, 'y': EST_T6_025_SSP3, 'fillcolor': EST_T6_color_f, 'line_color': EST_T6_color_f},
    {'name': 'EST-T7', 'x': x, 'y': EST_T7_025_SSP3, 'fillcolor': EST_T7_color_f, 'line_color': EST_T7_color_f},
]

# Data for annotations
annotations = [
    {'x': 1.0825, 'y': 0.510, 'text': '<b>BAU-C1', 'color': BAU_C1_color_l},
    {'x': 1.0825, 'y': 0.550, 'text': '<b>BAU-C2', 'color': BAU_C2_color_l},
    {'x': 1.0825, 'y': 0.530, 'text': '<b>BAU-C3', 'color': BAU_C3_color_l},
    {'x': 1.075, 'y': 0.450, 'text': '<b>LC<sup>3</sup>-C1', 'color': LC3_C1_color_l},
    {'x': 1.075, 'y': 0.490, 'text': '<b>LC<sup>3</sup>-C2', 'color': LC3_C2_color_l},
    {'x': 1.075, 'y': 0.470, 'text': '<b>LC<sup>3</sup>-C3', 'color': LC3_C3_color_l},
    {'x': 1.075, 'y': 0.3885, 'text': '<b>EST-T1', 'color': EST_T1_color_l},
    {'x': 1.075, 'y': 0.36375, 'text': '<b>EST-T2', 'color': EST_T2_color_l},
    {'x': 1.075, 'y': 0.4275, 'text': '<b>EST-T3', 'color': EST_T3_color_l},
    {'x': 1.075, 'y': 0.24905, 'text': '<b>EST-T4', 'color': EST_T4_color_l},
    {'x': 1.075, 'y': 0.220, 'text': '<b>EST-T5', 'color': EST_T5_color_l},
    {'x': 1.075, 'y': 0.180, 'text': '<b>EST-T6', 'color': EST_T6_color_l},
    {'x': 1.075, 'y': 0.2755, 'text': '<b>EST-T7', 'color': EST_T7_color_l},
]

fig = go.Figure()

# Add traces
for trace in traces_fill:
    fig.add_trace(go.Scatter(
        x=trace['x'],
        y=trace['y'],
        fill='toself',
        fillcolor=trace['fillcolor'],
        line_color='rgba(0,0,0,0)',  # 'rgba(0,0,0,0)', trace['line_color'],
        # line_dash='dot',
        showlegend=False,
        name=trace['name']

    ))

for trace in traces_line_ssp1:
    fig.add_trace(go.Scatter(
        x=trace['x'],
        y=trace['y'],
        # fill='tozeroy',
        # fillcolor=trace['fillcolor'],
        line_color=trace['line_color'],
        line_width=linewidth + 0.5,
        line_dash='dash',
        showlegend=False,
        name=trace['name']

    ))

for trace in traces_line_ssp3:
    fig.add_trace(go.Scatter(
        x=trace['x'],
        y=trace['y'],
        # fill='tozeroy',
        # fillcolor=trace['fillcolor'],
        line_color=trace['line_color'],
        line_width=linewidth + 0.5,
        line_dash='dot',
        showlegend=False,
        name=trace['name']

    ))

for trace in traces_line:
    fig.add_trace(go.Scatter(
        x=trace['x'],
        y=trace['y'],
        # fill='tozeroy',
        # fillcolor=trace['fillcolor'],
        line_color=trace['line_color'],
        line_width=linewidth + 1.5,
        showlegend=True,
        name=trace['name']

    ))

# Add annotations
for annotation in annotations:
    fig.add_annotation(
        x=annotation['x'],
        y=annotation['y'],
        text=annotation['text'],
        showarrow=False,
        xref='paper',
        yref='paper',
        align='center',
        font=dict(
            family=fontfamily,
            size=ofs,
            color=annotation['color']
        ),
    )

# Configure x-axis
fig.update_xaxes(
    showline=True,
    mirror=True,
    linewidth=linewidth,
    linecolor='black',
    title='<b>Years</b>',
    title_font=dict(
        family='Helvetica',
        size=tfs + 2,
        color='black',
    ),
    title_standoff=title_standoff,
    tickfont=dict(
        family='Helvetica',
        size=tfs,
        color='black'
    ),
    showgrid=True,
    gridwidth=gridwidth,
    gridcolor='lightgray',
    tickangle=-90,
    ticklabelstep=1,
    minor=dict(
        ticklen=0,
        tickcolor="lightgray",
        tickmode='auto',
        nticks=5,
        showgrid=True
    ),
    range=[0, 60000]
)

# Configure y-axis
fig.update_yaxes(
    showline=True,
    mirror=True,
    linewidth=linewidth,
    linecolor='black',
    title='<b>AGTP (Kelvin)</b>',
    title_font=dict(
        family='Helvetica',
        size=tfs + 2,
        color='black',
    ),
    title_standoff=title_standoff,
    showexponent='all',
    exponentformat='E',
    tickfont=dict(
        family='Helvetica',
        size=tfs,
        color='black'
    ),
    showgrid=True,
    gridwidth=gridwidth,
    gridcolor='lightgray',
    ticklabelstep=1,
    minor=dict(
        ticklen=0,
        tickcolor="lightgray",
        tickmode='auto',
        nticks=2,
        showgrid=True
    ),
    range=[-0.01, 0.06]
)

# Configure trace properties
fig.update_traces(marker_line_color='black')

# Configure legend
fig.update_layout(
    legend=dict(
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
    barmode='stack',
    plot_bgcolor='white',
    width=width,
    height=height + 100,
    margin=dict(
        t=t,
        b=b,
        l=l,
        r=r + 110
    )
)

# # Configure title
# fig.update_layout(
#     title='<b>Global<b>',
#     title_x=0.08,
#     title_y=0.962,
#     title_font=dict(size=tfs+8, color='black', family=fontfamily),
# )


fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=[0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000],
        ticktext=['2025', '2050', '2075', '2100', '2125', '2150', '2175', '2200', '2225', '2250', '2275', '2300',
                  '2325']
    )
)

fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black')

fig.update_traces(mode='lines')
fig.show()

directory = "../../output/figures/agtp/html"
if not os.path.exists(directory):
    os.makedirs(directory)

directory = "../../output/figures/agtp/img"
if not os.path.exists(directory):
    os.makedirs(directory)

# Save the figure as an HTML file
fig.write_html("../../output/figures/agtp/html/agtp.html")

# Save the figure as an HTML file
fig.write_image("../../output/figures/agtp/img/agtp.pdf", scale=scale, engine='orca')
fig.write_image("../../output/figures/agtp/img/agtp.jpg", scale=scale, engine='orca')
