from django.shortcuts import render, redirect
from django.contrib import messages

from bokeh.transform import transform
from bokeh.models import (ColumnDataSource, Plot,
                          Grid, HoverTool, LogColorMapper, LogTicker,
                          ColorBar, PrintfTickFormatter, LinearAxis)
from bokeh.models.widgets import Slider
from bokeh.models.callbacks import CustomJS
from bokeh.plotting import figure
from bokeh.layouts import gridplot, layout, column, row
from bokeh.embed import components
from bokeh.transform import cumsum
from bokeh.palettes import inferno, viridis, cividis, Viridis256, Blues256

import pandas as pd
import numpy as np
from numpy.random import random
from datetime import date
import timeit
from math import pi
from .mgcharts import mg_bar, mg_select, mg_slider
import sweetify
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from bokeh.models import ColumnDataSource, LayoutDOM
from bokeh.core.properties import Instance, String
from bokeh.util.compiler import TypeScript

TS_CODE = """
// This custom model wraps one part of the third-party vis.js library:
//
//     http://visjs.org/index.html
//
// Making it easy to hook up python data analytics tools (NumPy, SciPy,
// Pandas, etc.) to web presentations using the Bokeh server.

import {LayoutDOM, LayoutDOMView} from "models/layouts/layout_dom"
import {ColumnDataSource} from "models/sources/column_data_source"
import {LayoutItem} from "core/layout"
import * as p from "core/properties"

declare namespace vis {
  class Graph3d {
    constructor(el: HTMLElement, data: object, OPTIONS: object)
    setData(data: vis.DataSet): void
  }

  class DataSet {
    add(data: unknown): void
  }
}

// This defines some default options for the Graph3d feature of vis.js
// See: http://visjs.org/graph3d_examples.html for more details.
const OPTIONS = {
  width: '600px',
  height: '600px',
  style: 'surface',
  showPerspective: true,
  showGrid: true,
  keepAspectRatio: true,
  verticalRatio: 1.0,
  legendLabel: 'stuff',
  cameraPosition: {
    horizontal: -0.35,
    vertical: 0.22,
    distance: 1.8,
  },
}
// To create custom model extensions that will render on to the HTML canvas
// or into the DOM, we must create a View subclass for the model.
//
// In this case we will subclass from the existing BokehJS ``LayoutDOMView``
export class Surface3dView extends LayoutDOMView {
  model: Surface3d

  private _graph: vis.Graph3d

  initialize(): void {
    super.initialize()

    const url = "https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"
    const script = document.createElement("script")
    script.onload = () => this._init()
    script.async = false
    script.src = url
    document.head.appendChild(script)
  }

  private _init(): void {
    // Create a new Graph3s using the vis.js API. This assumes the vis.js has
    // already been loaded (e.g. in a custom app template). In the future Bokeh
    // models will be able to specify and load external scripts automatically.
    //
    // BokehJS Views create <div> elements by default, accessible as this.el.
    // Many Bokeh views ignore this default <div>, and instead do things like
    // draw to the HTML canvas. In this case though, we use the <div> to attach
    // a Graph3d to the DOM.
    this._graph = new vis.Graph3d(this.el, this.get_data(), OPTIONS)

    // Set a listener so that when the Bokeh data source has a change
    // event, we can process the new data
    this.connect(this.model.data_source.change, () => {
      this._graph.setData(this.get_data())
    })
  }

  // This is the callback executed when the Bokeh data has an change. Its basic
  // function is to adapt the Bokeh data source to the vis.js DataSet format.
  get_data(): vis.DataSet {
    const data = new vis.DataSet()
    const source = this.model.data_source
    for (let i = 0; i < source.get_length()!; i++) {
      data.add({
        x: source.data[this.model.x][i],
        y: source.data[this.model.y][i],
        z: source.data[this.model.z][i],
      })
    }
    return data
  }

  get child_models(): LayoutDOM[] {
    return []
  }

  _update_layout(): void {
    this.layout = new LayoutItem()
    this.layout.set_sizing(this.box_sizing())
  }
}

// We must also create a corresponding JavaScript BokehJS model subclass to
// correspond to the python Bokeh model subclass. In this case, since we want
// an element that can position itself in the DOM according to a Bokeh layout,
// we subclass from ``LayoutDOM``
export namespace Surface3d {
  export type Attrs = p.AttrsOf<Props>

  export type Props = LayoutDOM.Props & {
    x: p.Property<string>
    y: p.Property<string>
    z: p.Property<string>
    data_source: p.Property<ColumnDataSource>
  }
}

export interface Surface3d extends Surface3d.Attrs {}

export class Surface3d extends LayoutDOM {
  properties: Surface3d.Props
  __view_type__: Surface3dView

  constructor(attrs?: Partial<Surface3d.Attrs>) {
    super(attrs)
  }

  // The ``__name__`` class attribute should generally match exactly the name
  // of the corresponding Python class. Note that if using TypeScript, this
  // will be automatically filled in during compilation, so except in some
  // special cases, this shouldn't be generally included manually, to avoid
  // typos, which would prohibit serialization/deserialization of this model.
  static __name__ = "Surface3d"

  static init_Surface3d() {
    // This is usually boilerplate. In some cases there may not be a view.
    this.prototype.default_view = Surface3dView

    // The @define block adds corresponding "properties" to the JS model. These
    // should basically line up 1-1 with the Python model class. Most property
    // types have counterparts, e.g. ``bokeh.core.properties.String`` will be
    // ``p.String`` in the JS implementatin. Where the JS type system is not yet
    // as rich, you can use ``p.Any`` as a "wildcard" property type.
    this.define<Surface3d.Props>({
      x:            [ p.String   ],
      y:            [ p.String   ],
      z:            [ p.String   ],
      data_source:  [ p.Instance ],
    })
  }
}
"""

# This custom extension model will have a DOM view that should layout-able in
# Bokeh layouts, so use ``LayoutDOM`` as the base class. If you wanted to create
# a custom tool, you could inherit from ``Tool``, or from ``Glyph`` if you
# wanted to create a custom glyph, etc.
class Surface3d(LayoutDOM):

    # The special class attribute ``__implementation__`` should contain a string
    # of JavaScript code that implements the browser side of the extension model.
    __implementation__ = TypeScript(TS_CODE)

    # Below are all the "properties" for this model. Bokeh properties are
    # class attributes that define the fields (and their types) that can be
    # communicated automatically between Python and the browser. Properties
    # also support type validation. More information about properties in
    # can be found here:
    #
    #    https://docs.bokeh.org/en/latest/docs/reference/core/properties.html#bokeh-core-properties

    # This is a Bokeh ColumnDataSource that can be updated in the Bokeh
    # server by Python code
    data_source = Instance(ColumnDataSource)

    # The vis.js library that we are wrapping expects data for x, y, and z.
    # The data will actually be stored in the ColumnDataSource, but these
    # properties let us specify the *name* of the column that should be
    # used for each field.
    x = String

    y = String

    z = String



def time_function(function):
    def wrapper(*args, **kwargs):
        print(function.__name__, 'starting...')
        start = timeit.default_timer()
        result = function(*args, **kwargs)
        stop = timeit.default_timer()
        print(function.__name__, 'took:', stop - start, 'seconds')
        return result
    return wrapper


@time_function
def index(request):
    # Check that the request is POST type
    if request.method == 'POST':
        # Declare variables
        count = 0
        df_csv = pd.DataFrame()

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
            try:
                if csv.name.endswith('.csv'):
                    df = pd.read_csv(csv)
                else:
                    df = pd.read_pickle(csv)
            except Exception as e:
                messages.error(
                    request,
                    'One of the files uploaded is not a csv or pickle file: ' +
                    csv.name)
                return HttpResponseRedirect(reverse_lazy('charts:index'))

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

        return redirect('charts:graph', csv=csv_name)

    template = 'pages/index.html'
    return render(request, template)


def one_experiment(csv):
    # Get csv
    df = pd.read_csv(csv)
    print(df)
    # Get Data
    # Coordenates
    df2 = df.drop_duplicates('coordX')
    df2 = df.drop_duplicates('coordY')
    xx = df2['coordX']
    yy = df2['coordY']
    zz = df2['sumTime']
    x = df['coordX'].unique()
    y = df['coordY'].unique()

    # Get csv Count
    sumtime = df.loc[df['Time'] == 1]
    countList = list(sumtime['sumTime'])

    # csvList
    csvList = list(df['csvName'].unique())

    # Get time Count
    time = df.loc[df['id'] == 1]

    # Get cvs time values in x Time
    timeList = []
    for i in range(len(time)):
        res = df.loc[df['Time'] == i + 1]
        lList = list(res['sumTime'])
        timeList.append(lList)

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
        count=countList,
        colors=colors))

    xx, yy, zz = np.meshgrid(xx, yy, zz)

    surface_source = ColumnDataSource(dict(
        x=xx,
        y=yy,
        z=zz
    ))


    # Hover
    hover = HoverTool(tooltips=[
        ('csv', '@csv'),
        ('Total', '@count')
    ])

    scatter = figure(tools=[hover])

    scatter.scatter(x='x', y='y', size=16, source=source,
                    fill_color='colors', fill_alpha=0.7)

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
    
  
    heatmap_data = np.array(gene_list).sum(axis=0).T
    heatmap_genes = ('WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
                     'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB')
    heatmap_df = pd.DataFrame(data=heatmap_data, index=heatmap_genes)
    heatmap_df.columns.name = 'time'
    heatmap_df.index.name = 'gene'
    heatmap_data = pd.DataFrame(heatmap_df.stack(),
                                columns=['value']).reset_index()
    
    hm_hover = HoverTool(tooltips=[
        ('Gene', '@gene'),
        ('Time', '@time'),
        ('Value', '@value')
    ])
    heatmap_source = ColumnDataSource(heatmap_data)

    # Heatmap
    hm_max = heatmap_data.value.max()

    # Using 0 as low prevents it from using LogTicker
    mapper = LogColorMapper(palette=Blues256,
                               low=1,
                               high=hm_max)

    heatmap = figure(
        title="Heatmap",
        x_range=list(heatmap_df.columns.astype('str')),
        y_range=heatmap_genes,
        tools="save,pan,box_zoom,reset,wheel_zoom"
    )
    heatmap.add_tools(hm_hover)
    heatmap.rect(x="time", y="gene", width=1, height=1, source=heatmap_source,
                 line_color=None, fill_color=transform('value', mapper), dilate=True)
    
    surface = Surface3d(x="x", y="y", z="z", data_source=surface_source, width=600, height=600)

    color_bar = ColorBar(
        color_mapper=mapper,
        location=(0, 0),
        ticker=LogTicker(),
        formatter=PrintfTickFormatter(format="%d"),
        orientation='horizontal'
    )

    heatmap.add_layout(color_bar, 'below')

    csv_selected = gene_list[0]

    # Get data for graph
    counts = csv_selected[0]

    # Get colors
    bar_colors = cividis(len(col_list))

    bar_source = ColumnDataSource(data=dict(
        col_list=col_list,
        counts=counts,
        bar_colors=bar_colors,
        gene_list=gene_list))

    status = ColumnDataSource(data={
        'time': [1],
        'csv': [0]
    })

    bar = mg_bar(col_list, bar_source)

    # Slider
    slider = mg_slider(source, timeList, time, bar_source, status)

    # Select
    select = mg_select(csvList, bar_source, status)
    return scatter, bar, heatmap, slider, select, surface


@time_function
def graph(request, csv):
    scatter, bar, heatmap, slider, select, surface = one_experiment(csv)
    
    controls = row(slider, select)
    # Create grid for graphics
    grid = layout([
        [heatmap, surface],
        [controls],
        [scatter, bar]
    ], sizing_mode="stretch_width")

    # Store components
    script, div = components(grid)

    # Return to Django with Components sent as arguments which will then de
    # displayed
    return render(request,
                  'pages/base.html', {'script': script, 'div': div})


@time_function
def graph_2(request, csv, csv_2):
    scatter, bar, heatmap, slider, select = one_experiment(csv)

    scatter_2, bar_2, heatmap_2, slider_2, select_2 = one_experiment(csv)

    controls = row(slider, select)
    controls_2 = row(slider_2, select_2)
    # Create grid for graphics
    grid = layout([
        [heatmap],
        [controls],
        [scatter, bar],
        [heatmap_2],
        [controls_2],
        [scatter_2, bar_2]
    ], sizing_mode="stretch_width")

    # Store components
    script, div = components(grid)

    # Return to Django with Components sent as arguments which will then de
    # displayed
    return render(request,
                  'pages/base.html', {'script': script, 'div': div})
