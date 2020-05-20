from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.models.widgets import Select
from bokeh.models.callbacks import CustomJS

def mg_bar(col_list, bar_source):
    hover = HoverTool(tooltips=[
        ('gene', '@col_list'),
        ('Total', '@counts')
    ])

    bar = figure(x_range=col_list, plot_height=600, plot_width=800,
                 toolbar_location=None, title="Gene Counts", tools=[hover])
    bar.vbar(
        x='col_list',
        top='counts',
        width=0.9,
        source=bar_source,
        legend="col_list",
        line_color='white',
        fill_color='bar_colors')

    bar.xgrid.grid_line_color = None
    bar.y_range.start = 0
    bar.y_range.end = 700
    bar.legend.orientation = "horizontal"
    bar.legend.location = "top_center"

    return bar

def mg_select(csvList, bar_source):
    select = Select(title="csv File:", value=csvList[0], options=csvList)
    # Select Code
    with open('./charts/select.js', 'r') as select_file:
        select_code = select_file.read()

    select_callback = CustomJS(
        args=dict(select=select, bar_source=bar_source), code=select_code)
    select.js_on_change('value', select_callback)

    return select