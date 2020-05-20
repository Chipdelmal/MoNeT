from bokeh.plotting import figure

def mg_bar(col_list, bar_source, hover):
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
