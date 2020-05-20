from django.shortcuts import render, redirect
from django.contrib import messages

from bokeh.models import ColumnDataSource, Plot, Grid, HoverTool
from bokeh.models.widgets import Select, Slider
from bokeh.models.callbacks import CustomJS
from bokeh.plotting import figure
from bokeh.layouts import column, gridplot
from bokeh.embed import components
from bokeh.transform import cumsum
from bokeh.palettes import inferno, viridis, cividis

import pandas as pd
import numpy as np
from numpy.random import random
from datetime import date
import timeit
from math import pi
from .mgcharts import mg_bar


def index(request):
    # Check that the request is POST type
    if request.method == 'POST':
        start = timeit.default_timer()

        # Declare variables
        count = 0
        df_csv = pd.DataFrame()

        # Declare template
        template = 'pages/index.html'
        # Check that is compare charts
        if 'compare_charts' in request.POST:
            _list = []
            csv_files_compare = request.FILES.getlist('compareCharts')
            for csv in csv_files_compare:
                _list.append(csv.name)
            return redirect('graph_2', csv=_list[0], csv_2=_list[1])

        # Get csv coordenate file
        csv_coordenates = pd.read_csv(request.FILES['csvCoordenates'])

        # Loop through all file list
        csv_files = request.FILES.getlist('csvFile')
        for csv in csv_files:
            # Check if it is a csv file
            if not csv.name.endswith('.csv'):
                messages.error(
                    request,
                    'One of the file uploaded is not a cvs file: ' +
                    csv.name)
                continue

            # DataFrame csv
            df = pd.read_csv(csv)

            # Add row total
            col_list = list(df)
            col_list.remove('Time')
            df['sumTime'] = df[col_list].sum(axis=1)

            # Add csv id
            df.insert(0, 'id', count)

            # Add csv name
            df.insert(1, 'csvName', csv.name)

            # Add coordenates
            df.insert(1, 'coordX', csv_coordenates.iat[count, 0])
            df.insert(1, 'coordY', csv_coordenates.iat[count, 1])

            # Append csv to csvList
            df_csv = df_csv.append(df)

            count = count + 1

        # export csvList
        csv_name = request.POST.get(
            'experiment') + '_' + str(date.today()) + '.csv'
        df_csv.to_csv(csv_name)

        stop = timeit.default_timer()
        print('Time: ', stop - start)

        return redirect('graph', csv=csv_name)

    return render(request, template)


def graph(request, csv):

    start = timeit.default_timer()

    # Get csv
    df = pd.read_csv(csv)

    # Get Data
    # Coordenates
    x = df['coordX'].unique()
    y = df['coordY'].unique()

    # csvList
    csvList = list(df['csvName'].unique())

    # Get csv Count
    sumtime = df.loc[df['Time'] == 1]
    countList = list(sumtime['sumTime'])

    # Get time Count
    time = df.loc[df['id'] == 1]

    # Get cvs time values in x Time
    timeList = []
    for i in range((len(time))):
        aux = i
        l = df.loc[df['Time'] == aux]
        lList = list(l['sumTime'])
        timeList.append(lList)

    # Slider
    slider = Slider(start=1, end=len(time), value=1, step=1, title="Time")

    # Scatter Graphic:
    # Colors
    N = len(sumtime['sumTime'])
    _x = random(size=N) * 100
    color_count = np.asarray(countList)
    colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(
        50 + 2 * _x, (30 + 2 * (color_count / 100)))]

    # Data Source
    source = ColumnDataSource(dict(
        x=x,
        y=y,
        csv=csvList,
        t_hover=countList,
        colors=colors,
        aux_color=_x,
        color_values=color_count))

    # Hover
    hover = HoverTool(tooltips=[
        ('csv', '@csv'),
        ('Total', '@t_hover')
    ])

    scatter = figure(tools=[hover])

    scatter.scatter(x='x', y='y', size=15, source=source,
              fill_color='colors', fill_alpha=0.6,
              line_color=None)

    # Bar Graph
    # Get Column List
    col_list = list(df)
    col_list.remove('id')
    col_list.remove('coordY')
    col_list.remove('coordX')
    col_list.remove('csvName')
    col_list.remove('Time')
    col_list.remove('sumTime')
    col_list.remove('Unnamed: 0')

    # Get df for first csv
    bar_initial = df.loc[df['id'] == 0]
    bar_initial = bar_initial[col_list]

    gene_list = []
    # Get list of gene values
    count_csv = len(df['id'].unique())
    for i in range(count_csv):

        # Get gene values for a single csv
        bar_initial = df.loc[df['id'] == i]
        bar_initial = bar_initial[col_list]
        aux_gene = []
        for rows in bar_initial.itertuples(index=False):
            x = list(rows)
            aux_gene.append(x)

        gene_list.append(aux_gene)

    csv_selected = gene_list[0]

    # Get data for graph
    counts = csv_selected[0]
    print(counts)

    # Get colors
    bar_colors = cividis(len(col_list))
    print(bar_colors)

    bar_source = ColumnDataSource(data=dict(
        col_list=col_list,
        counts=counts,
        bar_colors=bar_colors,
        gene_list=gene_list,
        selected_csv=[0, 0],
        selected_time=[1, 0]))

    # Hover
    hover = HoverTool(tooltips=[
        ('gene', '@col_list'),
        ('Total', '@counts')
    ])

    bar = mg_bar(col_list, bar_source, hover)

    with open('./charts/slider.js', 'r') as slider_file:
        slider_code = slider_file.read()

    callback = CustomJS(
        args=dict(
            source=source,
            slider=slider,
            timeList=timeList,
            _x=_x,
            bar_source=bar_source),
        code=slider_code)
    slider.js_on_change('value', callback)

    # Select
    select = Select(title="csv File:", value=csvList[0], options=csvList)
    # Select Code
    with open('./charts/select.js', 'r') as select_file:
        select_code = select_file.read()

    select_callback = CustomJS(
        args=dict(select=select, bar_source=bar_source), code=select_code)
    select.js_on_change('value', select_callback)

    # Create grid for graphics
    grid = gridplot([[column(slider, scatter, width=800), column(
        select, bar, width=800)]], toolbar_location=None)

    # Store components
    script, div = components(grid)

    stop = timeit.default_timer()
    print()
    print('Time: ', stop - start)

    # Return to Django with Components sent as arguments which will then de
    # displayed
    return render(request,
        'pages/base.html', {'script': script, 'div': div})


def graph_2(request, csv, csv_2):

    start = timeit.default_timer()

    # Get csv
    df = pd.read_csv(csv)

    # Get Data
    # Coordenates
    x = df['coordX'].unique()
    y = df['coordY'].unique()

    # csvList
    csvList = list(df['csvName'].unique())

    # Get csv Count q
    sumtime = df.loc[df['Time'] == 1]
    countList = list(sumtime['sumTime'])

    # Get time Count
    time = df.loc[df['id'] == 1]

    # Get cvs time values in x Time
    timeList = []
    for i in range((len(time))):
        aux = i
        l = df.loc[df['Time'] == aux]
        lList = list(l['sumTime'])
        timeList.append(lList)

    # Slider
    slider = Slider(start=1, end=len(time), value=1, step=1, title="Time")

    # Scatter Graphic:
    # Colors
    N = len(sumtime['sumTime'])
    _x = random(size=N) * 100
    color_count = np.asarray(countList)
    colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(
        50 + 2 * _x, (30 + 2 * (color_count / 100)))]

    # Data Source
    source = ColumnDataSource(dict(
        x=x,
        y=y,
        csv=csvList,
        t_hover=countList,
        colors=colors,
        aux_color=_x,
        color_values=color_count))

    # Hover
    hover = HoverTool(tooltips=[
        ('csv', '@csv'),
        ('Total', '@t_hover')
    ])

    scatter = figure(tools=[hover])

    scatter.scatter(x='x', y='y', size=15, source=source,
              fill_color='colors', fill_alpha=0.6,
              line_color=None)

    # Bar Graph
    # Get Column List
    col_list = list(df)
    col_list.remove('id')
    col_list.remove('coordY')
    col_list.remove('coordX')
    col_list.remove('csvName')
    col_list.remove('Time')
    col_list.remove('sumTime')
    col_list.remove('Unnamed: 0')

    # Get df for first csv
    bar_initial = df.loc[df['id'] == 0]
    bar_initial = bar_initial[col_list]

    gene_list = []
    # Get list of gene values
    count_csv = len(df['id'].unique())
    for i in range(count_csv):

        # Get gene values for a single csv
        bar_initial = df.loc[df['id'] == i]
        bar_initial = bar_initial[col_list]
        aux_gene = []
        for rows in bar_initial.itertuples(index=False):
            x = list(rows)
            aux_gene.append(x)

        gene_list.append(aux_gene)

    csv_selected = gene_list[0]

    # Get data for graph
    counts = csv_selected[0]
    print(counts)

    # Get colors
    bar_colors = cividis(len(col_list))
    print(bar_colors)

    bar_source = ColumnDataSource(data=dict(
        col_list=col_list,
        counts=counts,
        bar_colors=bar_colors,
        gene_list=gene_list,
        selected_csv=[0, 0],
        selected_time=[1, 0]))

    # Hover
    hover = HoverTool(tooltips=[
        ('gene', '@col_list'),
        ('Total', '@counts')
    ])

    bar = mg_bar(col_list, bar_source, hover)

    # Slider Code
    with open('./charts/slider.js', 'r') as slider_file:
        slider_code = slider_file.read()

    callback = CustomJS(
        args=dict(
            source=source,
            slider=slider,
            timeList=timeList,
            _x=_x,
            bar_source=bar_source),
        code=slider_code)
    slider.js_on_change('value', callback)

    # Select
    select = Select(title="csv File:", value=csvList[0], options=csvList)

    # Select Code
    with open('./charts/select.js', 'r') as select_file:
        select_code = select_file.read()

    select_callback = CustomJS(
        args=dict(select=select, bar_source=bar_source), code=select_code)
    select.js_on_change('value', select_callback)
    # 2 Graphs
    # Get csv
    df_2 = pd.read_csv(csv_2)

    # Get Data
    # Coordenates
    x_2 = df_2['coordX'].unique()
    y_2 = df_2['coordY'].unique()

    # csvList
    csvList_2 = list(df_2['csvName'].unique())

    # Get csv Count
    sumtime_2 = df_2.loc[df_2['Time'] == 1]
    countList_2 = list(sumtime_2['sumTime'])

    # Get time Count
    time_2 = df_2.loc[df_2['id'] == 1]

    # Get cvs time values in x Time
    timeList_2 = []
    for i in range((len(time_2))):
        aux_2 = i
        l_2 = df_2.loc[df_2['Time'] == aux_2]
        lList_2 = list(l_2['sumTime'])
        timeList_2.append(lList_2)

    # Slider
    slider_2 = Slider(start=1, end=len(time_2), value=1, step=1, title="Time")

    # Scatter Graphic:
    # Colors
    N_2 = len(sumtime_2['sumTime'])
    _x_2 = random(size=N_2) * 100
    color_count_2 = np.asarray(countList_2)
    colors_2 = ["#%02x%02x%02x" % (int(r), 150, int(g)) for r, g in zip(
        50 + 2 * _x_2, (30 + 2 * (color_count_2 / 100)))]

    # Data Source
    source_2 = ColumnDataSource(dict(
        x=x_2,
        y=y_2,
        csv=csvList_2,
        t_hover=countList_2,
        colors=colors_2,
        aux_color=_x_2,
        color_values=color_count_2))

    # Hover
    hover_2 = HoverTool(tooltips=[
        ('csv', '@csv'),
        ('Total', '@t_hover')
    ])

    p_2 = figure(tools=[hover_2])

    p_2.scatter(x='x', y='y', size=15, source=source_2,
                fill_color='colors', fill_alpha=0.6,
                line_color=None)

    # Bar Graph
    # Get Column List
    col_list_2 = list(df_2)
    col_list_2.remove('id')
    col_list_2.remove('coordY')
    col_list_2.remove('coordX')
    col_list_2.remove('csvName')
    col_list_2.remove('Time')
    col_list_2.remove('sumTime')
    col_list_2.remove('Unnamed: 0')

    # Get df for first csv
    bar_initial_2 = df_2.loc[df_2['id'] == 0]
    bar_initial_2 = bar_initial_2[col_list_2]

    gene_list_2 = []
    # Get list of gene values
    count_csv_2 = len(df_2['id'].unique())
    for i in range(count_csv_2):

        # Get gene values for a single csv
        bar_initial_2 = df_2.loc[df_2['id'] == i]
        bar_initial_2 = bar_initial_2[col_list_2]
        aux_gene_2 = []
        for rows in bar_initial_2.itertuples(index=False):
            x_2 = list(rows)
            aux_gene_2.append(x_2)

        gene_list_2.append(aux_gene_2)

    csv_selected_2 = gene_list_2[0]

    # Get data for graph
    counts_2 = csv_selected_2[0]
    print(counts_2)

    # Get colors
    bar_colors_2 = viridis(len(col_list_2))
    print(bar_colors_2)

    bar_source_2 = ColumnDataSource(data=dict(
        col_list=col_list_2,
        counts=counts_2,
        bar_colors=bar_colors_2,
        gene_list=gene_list_2,
        selected_csv=[0, 0],
        selected_time=[1, 0]))

    # Hover
    hover_2 = HoverTool(tooltips=[
        ('gene', '@col_list'),
        ('Total', '@counts')
    ])

    bar_2 = mg_bar(col_list_2, bar_source_2, hover_2)

    callback_2 = CustomJS(
        args=dict(
            source=source_2,
            slider=slider_2,
            timeList=timeList_2,
            _x=_x_2,
            bar_source=bar_source_2),
        code=slider_code)
    slider_2.js_on_change('value', callback_2)

    # Select
    select_2 = Select(title="csv File:", value=csvList_2[0], options=csvList_2)

    select_callback_2 = CustomJS(
        args=dict(
            select=select_2,
            bar_source=bar_source_2),
        code=select_code)
    select_2.js_on_change('value', select_callback_2)

    # Create grid for graphics
    grid = gridplot([[column(slider, scatter, slider_2, p_2, width=800), column(
        select, bar, select_2, bar_2, width=800)]], toolbar_location=None)

    # Store components
    script, div = components(grid)

    stop = timeit.default_timer()
    print()
    print('Time: ', stop - start)

    # Return to Django with Components sent as arguments which will then de
    # displayed
    return render(request,
        'pages/base.html', {'script': script, 'div': div})
