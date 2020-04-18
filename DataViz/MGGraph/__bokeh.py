from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid, HoverTool
from bokeh.models.callbacks import CustomJS
from bokeh.models.glyphs import HexTile
from bokeh.io import curdoc, show
from bokeh.layouts import column, gridplot
from bokeh.models.widgets import Slider, Select

import pandas


source = ColumnDataSource(dict(
        q=[0,  0, -1, -1,  1, 1, 0],
        r=[0, -1,  0,  1, -1, 0, 1],
        csv=
        [
            'M_Mean_Patch2194',  
            "M_Mean_Patch2193",
            "M_Mean_Patch2192",
            "M_Mean_Patch2191",
            "M_Mean_Patch2190",
            "M_Mean_Patch2189",
            "M_Mean_Patch2188"  
        ],
        t_hover=[10, 1, 2, 0, 4, 0, 6],
        t_1=[10, 1, 2, 0, 4, 0, 6],
        t_2=[9.8, 0, 0, 0, 0, 0, 0],
        t_3=[9.7, 5, 7, 2, 0, 7, 0],
        t_4=[9.4, 0, 4, 6, 2, 1, 1],
    )
)

select = Select(title="Option:", value="M_Mean_Patch2194.csv", 
    options=["M_Mean_Patch2195.csv", "bar", "baz", "quux"])
slider = Slider(start=0, end=10, value=1, step=1, title="Tiempo")

hover = HoverTool(tooltips=
    [
        ('csv', '@csv'), 
        ('Total', '@t_hover')
    ]



code="""
var data = source.data;
var t_slider = slider.value;
var sl = 't_' + t_slider;

t_hover = data['t_hover']
aux = data[sl]

for(i = 0; i < t_hover.length; i++)
{
    t_hover[i] = aux[i]
}
console.log(source.data)
source.change.emit()
"""

slider.callback = CustomJS(args=dict(source=source, slider=slider), code=code)

plot = Plot(
    title=None, 
    plot_width=600, 
    plot_height=600,
    tools=[hover],
    )

glyph = HexTile(
    q="q", 
    r="r", 
    size=1, 
    fill_color="#fb9a99"
    )

hover_HexTile = HexTile(
    q="q", 
    r="r", 
    size=1, 
    fill_color="orange"
    )

plot.add_glyph(
    source, 
    glyph,
    hover_glyph=hover_HexTile)

xaxis = LinearAxis()
plot.add_layout(xaxis, 'below')

yaxis = LinearAxis()
plot.add_layout(yaxis, 'left')

plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))


# Gráficas dispersión

df = pandas.read_csv('M_Mean_Patch2194.csv')

group = pandas.DataFrame(df)

source_2 = ColumnDataSource(group)

p0 = figure(
    plot_width=900, 
    plot_height=250,     
    toolbar_location=None,
    )
p0.yaxis.axis_label = 'WW'
p0.xaxis.visible = False

p0.circle(
    source=source_2,
    x='Time', 
    y='WW',
    alpha=0.2   
)

p1 = figure(
    plot_width=900, 
    plot_height=250, 
    toolbar_location=None,    
    )
p1.yaxis.axis_label = 'WH'

p1.circle(
    source=source_2,
    x='Time', 
    y='WH',
    alpha=0.3,
    color='pink'   
)

p2 = figure(
    plot_width=900, 
    plot_height=250, 
    toolbar_location=None,    
    )
p2.yaxis.axis_label = 'WE'

p2.circle(
    source=source_2,
    x='Time', 
    y='WE',
    alpha=0.3,
    color='yellow'   
)

grid = gridplot([[column(slider, plot, width=600), column(select, p0, p1, p2, width=600)]],
    toolbar_location=None)

show(grid)
# show(column(slider, plot, width=600))
