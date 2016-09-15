# -*- coding: utf-8 -*-
import pandas as pd
data = pd.read_csv('gapminder.csv', thousands=',', index_col='Year')

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (
    BoxAnnotation,
    Button,
    Label,
    LinearInterpolator,
    CategoricalColorMapper,
    ColumnDataSource,
    NumeralTickFormatter,
    HoverTool,
    Slider,
)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure


def make_plot(legend=False):
    source = ColumnDataSource(dict(
        x=data.loc[1950].income,
        y=data.loc[1950].life,
        country=data.loc[1950].Country,
        population=data.loc[1950].population,
        region=data.loc[1950].region
    ))
    if legend:
        width = 800
    else:
        width = 600
    p = figure(
        height=400, width=width,
        x_axis_type='log', x_range=(100, 100000), y_range=(0, 100),
        title='Gapminder',
        x_axis_label='Income',
        y_axis_label='Life expectancy',
        toolbar_location=None,
        tools=[HoverTool(tooltips='@country', show_arrow=False)]
    )

    label = Label(x=100, y=0, text=str(1950), text_font_size='70pt', text_color='#eeeeee')
    p.add_layout(label)
    size_mapper = LinearInterpolator(
        x=[data.population.min(), data.population.max()],
        y=[5, 50]
    )
    color_mapper = CategoricalColorMapper(
        factors=list(data.region.unique()),
        palette=Spectral6,
    )
    p.xaxis[0].formatter = NumeralTickFormatter(format="$0,")
    p.circle(
        x='x', y='y',
        size={'field': 'population', 'transform': size_mapper},
        color={'field': 'region', 'transform': color_mapper},
        alpha=0.6,
        source=source,
        legend='region'
    )
    p.legend.border_line_color = None
    p.right.append(p.legend[0])
    if legend:
        p.legend.location = (5, -15)
    else:
        p.legend.visible = False
    return p, source, label


def make_slider(p, source, label):
    def update(attr, old, new):
        new_data = dict(
            x=data.loc[new].income,
            y=data.loc[new].life,
            country=data.loc[new].Country,
            region=data.loc[new].region,
            population=data.loc[new].population,
        )
        source.data = new_data
        label.text = str(new)

    slider = Slider(start=1950, end=2010, step=1, title='Year', value=1950)
    slider.on_change('value', update)
    return slider

overlay_box = lambda: BoxAnnotation(fill_alpha=0.9, fill_color='white', top=100, bottom=0)
welcome = lambda: Label(text="Welcome to Gapminder, press Next to continue", x=500, y=50)
rich_wealthy = lambda: Label(text="Rich and wealthy", x=10000, y=80)
poor_sick = lambda: Label(text="Poor and sick", x=200, y=20)
region = lambda: Label(text="Countries are colored by region", x=5000, y=90)
pop = lambda: Label(text="and sized by population", x=5000, y=83)

next_button = Button(label="Next", width=100)
prev_button = Button(label="Prev", width=100)

layout = column()


def render_frame(frame):
    layout.children = []
    next_button.disabled = False
    prev_button.disabled = False
    if frame == 0:
        prev_button.disabled = True
        p, source, label = make_plot(legend=False)
        p.add_layout(overlay_box())
        p.add_layout(welcome())
        new_layout = column(
            row(p),
            row(column(prev_button), column(next_button)),
        )
        layout.children = [new_layout]
    if frame == 1:
        p, source, label = make_plot(legend=False)
        p.add_layout(overlay_box())
        p.add_layout(rich_wealthy())
        p.add_layout(poor_sick())
        new_layout = column(
            row(p),
            row(column(prev_button), column(next_button)),
        )
        layout.children = [new_layout]
    if frame == 2:
        p, source, label = make_plot(legend=True)
        p.add_layout(overlay_box())
        p.add_layout(region())
        new_layout = column(
            row(p),
            row(column(prev_button), column(next_button)),
        )
        layout.children = [new_layout]
    if frame == 3:
        p, source, label = make_plot(legend=True)
        p.add_layout(region())
        p.add_layout(pop())
        new_layout = column(
            row(p),
            row(column(prev_button), column(next_button)),
        )
        layout.children = [new_layout]
    if frame == 4:
        next_button.disabled = True
        p, source, label = make_plot(legend=True)
        slider = make_slider(p, source, label)
        button = Button(label='❚❚ Pause', width=100)

        def animate_update():
            year = slider.value + 1
            if year > 2010:
                year = 1950
            slider.value = year

        def animate():
            if button.label == '► Play':
                button.label = '❚❚ Pause'
                curdoc().add_periodic_callback(animate_update, 200)
            else:
                button.label = '► Play'
                curdoc().remove_periodic_callback(animate_update)

        button.on_click(animate)
        curdoc().add_periodic_callback(animate_update, 200)
        new_layout = column(
            row(p),
            row(slider, button),
            row(prev_button, next_button)
        )
        layout.children = [new_layout]


def go_next():
    global frame
    if frame < 4:
        frame += 1
    render_frame(frame)


def go_prev():
    global frame
    if frame > 0:
        frame -= 1
    render_frame(frame)

next_button.on_click(go_next)
prev_button.on_click(go_prev)

frame = 0
render_frame(frame)
curdoc().add_root(layout)
