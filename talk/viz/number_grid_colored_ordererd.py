import numpy as np
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CategoricalColorMapper

n = np.random.rand(100) * 20
n = n.astype(int)
n.sort()
x = np.array(list(range(0, 10)) * 10) + 0.4
y = np.array([[x] * 10 for x in range(0, 10)]).flatten() + 0.4
source = ColumnDataSource(dict(x=x, y=y, n=n))

p = figure(
    x_range=(0, 10), y_range=(0, 10),
    tools='', toolbar_location=None,
    x_axis_type=None, y_axis_type=None,
    outline_line_color=None, background_fill_color='#fdf6e3', border_fill_color=None,
)
rect_color_mapper = CategoricalColorMapper(factors=list(range(0, 12)), nan_color='#fdf6e3', palette=['firebrick'] * 13)
text_color_mapper = CategoricalColorMapper(factors=list(range(0, 12)), nan_color='black', palette=['white'] * 13)
p.rect(
    x='x', y='y', width=0.6, height=0.6, source=source,
    color={'field': 'n', 'transform': rect_color_mapper},
)
p.text(
    text='n', x='x', y='y', source=source,
    text_baseline='middle', text_align='center',
    text_color={'field': 'n', 'transform': text_color_mapper}
)
show(p)
