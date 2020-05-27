import pandas as pd
from bokeh.plotting import figure
from bokeh.io import show, curdoc
from bokeh.models import HoverTool, ColumnDataSource, Column, Panel

from bokeh.models.widgets import CheckboxGroup
from bokeh.palettes import Category20_16
import bokeh.layouts as layouts


def aspg_plot(data, aspg_data_label='ASPG DATA'):
   
    def style(p) :
        # Title
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p

    def make_dataset(runs_list):
        xs = []
        ys = []
        colors = [] 
        labels = []

        print(runs_list)

        for i, run in enumerate(runs_list):

            run = int(run)

            subset = data[aspg_data_label][data["RUN NO."]==run]

            print(subset)
    

            x = subset.iloc[0].x
            y = subset.iloc[0].cps
            label= subset.iloc[0].run_id

            xs.append(list(x))
            ys.append(list(y)) 
            labels.append(label)
            colors.append(run_colors[i])

        new_src = ColumnDataSource(data={'x': xs, 'y': ys, 'label': labels})

        return new_src

    def make_plot(src):
        # Blank figure with correct labels
        p = figure(
            plot_width=900,
            plot_height=600,
            title='',
            x_axis_label='x (m)',
            y_axis_label='cp_s'
        )

        p.multi_line('x', 'y', legend_label = 'label', line_width = 1, source = src)

        hover = HoverTool(tooltips=[('Run NO.', '@run'),
                                    ('x', '@x'),
                                    ('y', '@y')],
                          mode='vline')

        p.add_tools(hover)

        p = style(p)

        return p

    def update(attr, old, new):
        print(run_selection.active)

        runs_to_plot = [run_selection.labels[i] for i in run_selection.active]

        new_src = make_dataset(runs_to_plot)
        src.data.update(new_src.data)
    

    # Carriers and colors
    available_runs = list(set(data['RUN NO.'].apply(str)))
    available_runs.sort()   
    run_colors = Category20_16

     
    run_selection = CheckboxGroup(labels=available_runs, active = [0, 1])
    run_selection.on_change('active', update)   


    initial_runs = [run_selection.labels[i] for i in run_selection.active]



    src = make_dataset(initial_runs)

    p = make_plot(src)

    controls= layouts.Column(run_selection)

    layout = layouts.row(controls,p)

    tab = Panel(child=layout, title='ASPG')

    return tab


