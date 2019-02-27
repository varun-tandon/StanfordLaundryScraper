import datetime
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import csv

all_data = []
with open('washer_drier_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the headers
    all_data = list(reader)

wash_type = ['Washer', 'Dryer']

z = []
date_list = []
for i in range(len(wash_type)):
    new_row = []
    for line in all_data:
        if(i == 0):
            date_list.append(line[2])
        new_row.append(line[i])
    z.append(list(new_row))

data = [
    go.Heatmap(
        z=z,
        x=date_list,
        y=wash_type,
        colorscale='Reds',
    )
]

layout = go.Layout(
    title='Washer and Dryer Availability Over Time',
    xaxis = dict(ticks='', nticks=36),
    yaxis = dict(ticks='')
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='datetime-heatmap')