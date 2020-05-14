from django.shortcuts import render, render_to_response, redirect
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
from datetime import date
import timeit
from math import pi


def index(request):

    start = timeit.default_timer()

    # Declare variables
    count = 0
    df_csv = pd.DataFrame()

    # Declare template
    template = 'pages/index.html'

    # Check that the request is POST type
    if request.method == 'POST':

        #Check that is compare charts
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
                errors = True
                messages.error(request, 'One of the file uploaded is not a cvs file: ' + csv.name)
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
        csv_name = request.POST.get('experiment') + '_' + str(date.today()) + '.csv'
        df_csv.to_csv(csv_name)

        stop = timeit.default_timer()
        print('Time: ', stop - start)

        return redirect('graph', csv=csv_name)

    return render(request, template)

def graph(request, csv):
    
    start = timeit.default_timer()

    # Get csv
    df = pd.read_csv(csv)

    ## Get Data
    # Coordenates
    x = df['coordX'].unique()
    y = df['coordY'].unique()

    # csvList
    csvList = list(df['csvName'].unique())

    # Get csv Count
    sumtime = df.loc[df['Time'] == 1]    
    countList = list(sumtime['sumTime'])
    
    #Get time Count
    time = df.loc[df['id'] == 1]

    # Get cvs time values in x Time
    timeList = []
    for i in range((len(time))):
        aux = i
        l = df.loc[df['Time'] == aux]
        lList = list(l['sumTime'])
        timeList.append(lList)
    
    ## Slider
    slider = Slider(start=1, end=len(time), value=1, step=1, title="Time")    

    ## Scatter Graphic:
    # Colors
    color_values = sumtime['sumTime']
    N = len(sumtime['sumTime'])
    _x = np.random.random(size=N) * 100
    color_count = np.asarray(countList)
    colors = [
    "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50 + 2 * _x, (30 + 2 *(color_count / 100)))]    

    # Data Source
    source = ColumnDataSource(dict(
        x=x,
        y=y,
        csv=csvList,
        t_hover=countList,
        colors=colors,
        aux_color=_x,
        color_values=color_count ))   

    # Hover
    hover = HoverTool(tooltips=
    [
        ('csv', '@csv'), 
        ('Total', '@t_hover')
    ])    
    
    p = figure(tools=[hover])
    
    p.scatter(x='x', y='y', size=15, source=source,
          fill_color='colors', fill_alpha=0.6,
          line_color=None)

    

    ## Bar Graph
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
        for rows in bar_initial.itertuples(index = False):
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
        col_list = col_list, 
        counts = counts,
        bar_colors = bar_colors,
        gene_list = gene_list,
        selected_csv = [0, 0],
        selected_time = [1, 0] ))
    
    # Hover
    hover = HoverTool(tooltips=
    [
        ('gene', '@col_list'), 
        ('Total', '@counts')
    ])        

    bar = figure(x_range=col_list, plot_height=600, plot_width=800, toolbar_location=None, title="Gene Counts", tools=[hover])
    bar.vbar(x='col_list', top='counts', width=0.9, source=bar_source, legend="col_list",
        line_color='white', fill_color='bar_colors')

    bar.xgrid.grid_line_color = None
    bar.y_range.start = 0
    bar.y_range.end = 700
    bar.legend.orientation = "horizontal"
    bar.legend.location = "top_center"

    # Slider Code
    code="""
    console.log("Original Data:")
    console.log(source.data)
    const data = source.data;
    const t_slider = slider.value;

    console.log("Time List:")
    console.log(timeList[t_slider])

    const t_hover = data['t_hover'];
    const x = data['x']
    const colors = data['colors']
    const aux_color = data['aux_color']
    const color_values = data['color_values']
    const _timeList = timeList[t_slider];

    for(var i = 0; i < t_hover.length; i++)
    {
        t_hover[i] = _timeList[i];
        r = (50 + 2 * aux_color[i]);
        r = r.toString(16);
        r = r.substring(0, 2);

        g = _timeList[i];
        g = (30 + 2 *(g / 100));
        g = g.toString(16);
        g = g.substring(0, 2);

        
        b = (150).toString(16);

        s = "#" + r + " " + g + " " + b;
        s = s.replace(" ", "");
        colors[i] = s.replace(" ", "");
    }
    console.log("New Data:")
    console.log(source.data)
    source.change.emit()

    bar_data = bar_source.data;
    console.log("BarChart data:");
    console.log(bar_source.data);

    bar_csv = bar_data['gene_list'];
    console.log("bar_csv");
    console.log(bar_csv);

    selected_csv = bar_data['selected_csv'];
    selected_csv = selected_csv[0];
    console.log("selected_csv index");
    console.log(selected_csv);

    bar_csv = bar_csv[selected_csv];
    console.log("selected_csv");
    console.log(bar_csv);

    time = slider.value;
    console.log("slider value:");
    console.log(time);

    time = time - 1;

    bar_csv = bar_csv[time];
    console.log("final data");
    console.log(bar_csv);

    bar_counts = bar_data['counts'];

    for(var i = 0; i < bar_counts.length; i++)
    {
        bar_counts[i] = bar_csv[i];
    }

    console.log("BarChart New data:");
    console.log(bar_source.data);

    bar_source.change.emit();

    """

    callback = CustomJS(args=dict(source=source, slider=slider, timeList=timeList, _x=_x, bar_source=bar_source), code=code)
    slider.js_on_change('value', callback)

    ## Select
    select = Select(title="csv File:", value=csvList[0], options=csvList)


    #Select Code
    select_code="""
    console.log("Select List:");
    console.log(select.value);
    console.log(select.options);
    select_opt = select.options;
    var index = 0;
    for(var i = 0; i < select_opt.length; i++)
    {
        if(select_opt[i] == select.value)
        {
            index = i;
        }
    }
    console.log("Index Value");
    console.log(index);

    bar_data = bar_source.data;
    console.log("BarChart data:");
    console.log(bar_source.data);

    bar_csv = bar_data['gene_list'];
    console.log("bar_csv");
    console.log(bar_csv);

    selected_csv = bar_data['selected_csv'];
    selected_csv = selected_csv[index];
    console.log("selected_csv index");
    console.log(selected_csv);

    bar_csv = bar_csv[index];
    console.log("selected_csv");
    console.log(bar_csv);

    time = bar_data['selected_time'];
    time = time[0];    
    console.log("time: ");
    console.log(time);

    time = time - 1;

    bar_csv = bar_csv[time];
    console.log("final data");
    console.log(bar_csv);

    bar_counts = bar_data['counts'];

    for(var i = 0; i < bar_counts.length; i++)
    {
        bar_counts[i] = bar_csv[i];
    }

    console.log("BarChart New data:");
    console.log(bar_source.data);

    bar_source.change.emit();
    
    """
    select_callback = CustomJS(args=dict(select=select, bar_source=bar_source), code=select_code)
    select.js_on_change('value', select_callback)
    


    # Create grid for graphics
    grid = gridplot([[column(slider, p, width=800),column(select, bar, width=800)]],
            toolbar_location=None )

    # Store components
    script, div = components(grid)

    stop = timeit.default_timer()
    print()
    print('Time: ', stop - start)
    
    # Return to Django with Components sent as arguments which will then de displayed
    return render_to_response('pages/base.html', {'script' : script, 'div' : div} )

def graph_2(request, csv, csv_2):
    
    start = timeit.default_timer()

    # Get csv
    df = pd.read_csv(csv)

    ## Get Data
    # Coordenates
    x = df['coordX'].unique()
    y = df['coordY'].unique()

    # csvList
    csvList = list(df['csvName'].unique())

    # Get csv Count q
    sumtime = df.loc[df['Time'] == 1]    
    countList = list(sumtime['sumTime'])
    
    #Get time Count
    time = df.loc[df['id'] == 1]

    # Get cvs time values in x Time
    timeList = []
    for i in range((len(time))):
        aux = i
        l = df.loc[df['Time'] == aux]
        lList = list(l['sumTime'])
        timeList.append(lList)
    
    ## Slider
    slider = Slider(start=1, end=len(time), value=1, step=1, title="Time")    

    ## Scatter Graphic:
    # Colors
    color_values = sumtime['sumTime']
    N = len(sumtime['sumTime'])
    _x = np.random.random(size=N) * 100
    color_count = np.asarray(countList)
    colors = [
    "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50 + 2 * _x, (30 + 2 *(color_count / 100)))]    

    # Data Source
    source = ColumnDataSource(dict(
        x=x,
        y=y,
        csv=csvList,
        t_hover=countList,
        colors=colors,
        aux_color=_x,
        color_values=color_count ))   

    # Hover
    hover = HoverTool(tooltips=
    [
        ('csv', '@csv'), 
        ('Total', '@t_hover')
    ])    
    
    p = figure(tools=[hover])
    
    p.scatter(x='x', y='y', size=15, source=source,
          fill_color='colors', fill_alpha=0.6,
          line_color=None)

    

    ## Bar Graph
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
        for rows in bar_initial.itertuples(index = False):
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
        col_list = col_list, 
        counts = counts,
        bar_colors = bar_colors,
        gene_list = gene_list,
        selected_csv = [0, 0],
        selected_time = [1, 0] ))
    
    # Hover
    hover = HoverTool(tooltips=
    [
        ('gene', '@col_list'), 
        ('Total', '@counts')
    ])        

    bar = figure(x_range=col_list, plot_height=600, plot_width=800, toolbar_location=None, title="Gene Counts", tools=[hover])
    bar.vbar(x='col_list', top='counts', width=0.9, source=bar_source, legend="col_list",
        line_color='white', fill_color='bar_colors')

    bar.xgrid.grid_line_color = None
    bar.y_range.start = 0
    bar.y_range.end = 700
    bar.legend.orientation = "horizontal"
    bar.legend.location = "top_center"

    # Slider Code
    code="""
    console.log("Original Data:")
    console.log(source.data)
    const data = source.data;
    const t_slider = slider.value;

    console.log("Time List:")
    console.log(timeList[t_slider])

    const t_hover = data['t_hover'];
    const x = data['x']
    const colors = data['colors']
    const aux_color = data['aux_color']
    const color_values = data['color_values']
    const _timeList = timeList[t_slider];

    for(var i = 0; i < t_hover.length; i++)
    {
        t_hover[i] = _timeList[i];
        r = (50 + 2 * aux_color[i]);
        r = r.toString(16);
        r = r.substring(0, 2);

        g = _timeList[i];
        g = (30 + 2 *(g / 100));
        g = g.toString(16);
        g = g.substring(0, 2);

        
        b = (150).toString(16);

        s = "#" + r + " " + g + " " + b;
        s = s.replace(" ", "");
        colors[i] = s.replace(" ", "");
    }
    console.log("New Data:")
    console.log(source.data)
    source.change.emit()

    bar_data = bar_source.data;
    console.log("BarChart data:");
    console.log(bar_source.data);

    bar_csv = bar_data['gene_list'];
    console.log("bar_csv");
    console.log(bar_csv);

    selected_csv = bar_data['selected_csv'];
    selected_csv = selected_csv[0];
    console.log("selected_csv index");
    console.log(selected_csv);

    bar_csv = bar_csv[selected_csv];
    console.log("selected_csv");
    console.log(bar_csv);

    time = slider.value;
    console.log("slider value:");
    console.log(time);

    time = time - 1;

    bar_csv = bar_csv[time];
    console.log("final data");
    console.log(bar_csv);

    bar_counts = bar_data['counts'];

    for(var i = 0; i < bar_counts.length; i++)
    {
        bar_counts[i] = bar_csv[i];
    }

    console.log("BarChart New data:");
    console.log(bar_source.data);

    bar_source.change.emit();

    """

    callback = CustomJS(args=dict(source=source, slider=slider, timeList=timeList, _x=_x, bar_source=bar_source), code=code)
    slider.js_on_change('value', callback)

    ## Select
    select = Select(title="csv File:", value=csvList[0], options=csvList)    

    #Select Code
    select_code="""
    console.log("Select List:");
    console.log(select.value);
    console.log(select.options);
    select_opt = select.options;
    var index = 0;
    for(var i = 0; i < select_opt.length; i++)
    {
        if(select_opt[i] == select.value)
        {
            index = i;
        }
    }
    console.log("Index Value");
    console.log(index);

    bar_data = bar_source.data;
    console.log("BarChart data:");
    console.log(bar_source.data);

    bar_csv = bar_data['gene_list'];
    console.log("bar_csv");
    console.log(bar_csv);

    selected_csv = bar_data['selected_csv'];
    selected_csv = selected_csv[index];
    console.log("selected_csv index");
    console.log(selected_csv);

    bar_csv = bar_csv[index];
    console.log("selected_csv");
    console.log(bar_csv);

    time = bar_data['selected_time'];
    time = time[0];    
    console.log("time: ");
    console.log(time);

    time = time - 1;

    bar_csv = bar_csv[time];
    console.log("final data");
    console.log(bar_csv);

    bar_counts = bar_data['counts'];

    for(var i = 0; i < bar_counts.length; i++)
    {
        bar_counts[i] = bar_csv[i];
    }

    console.log("BarChart New data:");
    console.log(bar_source.data);

    bar_source.change.emit();
    
    """
    
    select_callback = CustomJS(args=dict(select=select, bar_source=bar_source), code=select_code)
    select.js_on_change('value', select_callback)




    ### 2 Graphs
    # Get csv
    df_2 = pd.read_csv(csv_2)

    ## Get Data
    # Coordenates
    x_2 = df_2['coordX'].unique()
    y_2 = df_2['coordY'].unique()

    # csvList
    csvList_2 = list(df_2['csvName'].unique())

    # Get csv Count
    sumtime_2 = df_2.loc[df_2['Time'] == 1]    
    countList_2 = list(sumtime_2['sumTime'])
    
    #Get time Count
    time_2 = df_2.loc[df_2['id'] == 1]

    # Get cvs time values in x Time
    timeList_2 = []
    for i in range((len(time_2))):
        aux_2 = i
        l_2 = df_2.loc[df_2['Time'] == aux_2]
        lList_2 = list(l_2['sumTime'])
        timeList_2.append(lList_2)
    
    ## Slider
    slider_2 = Slider(start=1, end=len(time_2), value=1, step=1, title="Time")    

    ## Scatter Graphic:
    # Colors
    color_values_2 = sumtime_2['sumTime']
    N_2 = len(sumtime_2['sumTime'])
    _x_2 = np.random.random(size=N_2) * 100
    color_count_2 = np.asarray(countList_2)
    colors_2 = [
    "#%02x%02x%02x" % (int(r), 150, int(g)) for r, g in zip(50 + 2 * _x_2, (30 + 2 *(color_count_2 / 100)))]    

    # Data Source
    source_2 = ColumnDataSource(dict(
        x=x_2,
        y=y_2,
        csv=csvList_2,
        t_hover=countList_2,
        colors=colors_2,
        aux_color=_x_2,
        color_values=color_count_2 ))   

    # Hover
    hover_2 = HoverTool(tooltips=
    [
        ('csv', '@csv'), 
        ('Total', '@t_hover')
    ])    
    
    p_2 = figure(tools=[hover_2])
    
    p_2.scatter(x='x', y='y', size=15, source=source_2,
          fill_color='colors', fill_alpha=0.6,
          line_color=None)

    

    ## Bar Graph
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
        for rows in bar_initial_2.itertuples(index = False):
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
        col_list = col_list_2, 
        counts = counts_2,
        bar_colors = bar_colors_2,
        gene_list = gene_list_2,
        selected_csv = [0, 0],
        selected_time = [1, 0] ))
    
    # Hover
    hover_2 = HoverTool(tooltips=
    [
        ('gene', '@col_list'), 
        ('Total', '@counts')
    ])        

    bar_2 = figure(x_range=col_list_2, plot_height=600, plot_width=800, toolbar_location=None, title="Gene Counts", tools=[hover_2])
    bar_2.vbar(x='col_list', top='counts', width=0.9, source=bar_source_2, legend="col_list",
        line_color='white', fill_color='bar_colors')

    bar_2.xgrid.grid_line_color = None
    bar_2.y_range.start = 0
    bar_2.y_range.end = 700
    bar_2.legend.orientation = "horizontal"
    bar_2.legend.location = "top_center"

    # Slider Code
    code_2="""
    console.log("Original Data:")
    console.log(source.data)
    const data = source.data;
    const t_slider = slider.value;

    console.log("Time List:")
    console.log(timeList[t_slider])

    const t_hover = data['t_hover'];
    const x = data['x']
    const colors = data['colors']
    const aux_color = data['aux_color']
    const color_values = data['color_values']
    const _timeList = timeList[t_slider];

    for(var i = 0; i < t_hover.length; i++)
    {
        t_hover[i] = _timeList[i];
        r = (50 + 2 * aux_color[i]);
        r = r.toString(16);
        r = r.substring(0, 2);

        g = _timeList[i];
        g = (30 + 2 *(g / 100));
        g = g.toString(16);
        g = g.substring(0, 2);

        
        b = (150).toString(16);

        s = "#" + r + " " + g + " " + b;
        s = s.replace(" ", "");
        colors[i] = s.replace(" ", "");
    }
    console.log("New Data:")
    console.log(source.data)
    source.change.emit()

    bar_data = bar_source.data;
    console.log("BarChart data:");
    console.log(bar_source.data);

    bar_csv = bar_data['gene_list'];
    console.log("bar_csv");
    console.log(bar_csv);

    selected_csv = bar_data['selected_csv'];
    selected_csv = selected_csv[0];
    console.log("selected_csv index");
    console.log(selected_csv);

    bar_csv = bar_csv[selected_csv];
    console.log("selected_csv");
    console.log(bar_csv);

    time = slider.value;
    console.log("slider value:");
    console.log(time);

    time = time - 1;

    bar_csv = bar_csv[time];
    console.log("final data");
    console.log(bar_csv);

    bar_counts = bar_data['counts'];

    for(var i = 0; i < bar_counts.length; i++)
    {
        bar_counts[i] = bar_csv[i];
    }

    console.log("BarChart New data:");
    console.log(bar_source.data);

    bar_source.change.emit();

    """       

    # bar_selected_csv = bar_csv[bar_data['selected_csv']];
    
    # console.log("Selected csv:");
    # console.log(bar_selected_csv);

    callback_2 = CustomJS(args=dict(source=source_2, slider=slider_2, timeList=timeList_2, _x=_x_2, bar_source=bar_source_2), code=code_2)
    slider_2.js_on_change('value', callback_2)

    ## Select
    select_2 = Select(title="csv File:", value=csvList_2[0], options=csvList_2)

    #Select Code
    select_code_2="""
    console.log("Select List:");
    console.log(select.value);
    console.log(select.options);
    select_opt = select.options;
    var index = 0;
    for(var i = 0; i < select_opt.length; i++)
    {
        if(select_opt[i] == select.value)
        {
            index = i;
        }
    }
    console.log("Index Value");
    console.log(index);

    bar_data = bar_source.data;
    console.log("BarChart data:");
    console.log(bar_source.data);

    bar_csv = bar_data['gene_list'];
    console.log("bar_csv");
    console.log(bar_csv);

    selected_csv = bar_data['selected_csv'];
    selected_csv = selected_csv[index];
    console.log("selected_csv index");
    console.log(selected_csv);

    bar_csv = bar_csv[index];
    console.log("selected_csv");
    console.log(bar_csv);

    time = bar_data['selected_time'];
    time = time[0];    
    console.log("time: ");
    console.log(time);

    time = time - 1;

    bar_csv = bar_csv[time];
    console.log("final data");
    console.log(bar_csv);

    bar_counts = bar_data['counts'];

    for(var i = 0; i < bar_counts.length; i++)
    {
        bar_counts[i] = bar_csv[i];
    }

    console.log("BarChart New data:");
    console.log(bar_source.data);

    bar_source.change.emit();
    
    """
    
    select_callback_2 = CustomJS(args=dict(select=select_2, bar_source=bar_source_2), code=select_code_2)
    select_2.js_on_change('value', select_callback_2)



    # Create grid for graphics
    grid = gridplot([[column(slider, p, slider_2, p_2, width=800), column(select, bar, select_2, bar_2, width=800)]],
            toolbar_location=None )

    # Store components
    script, div = components(grid)

    stop = timeit.default_timer()
    print()
    print('Time: ', stop - start)
    
    # Return to Django with Components sent as arguments which will then de displayed
    return render_to_response('pages/base.html', {'script' : script, 'div' : div} )