import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure

x = np.linspace(0, 5, 100000)
y = np.sin(2*np.pi*x)

source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(height=800, width=800, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 5], y_range=[-10.0, 10.0])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)



text = TextInput(title="title", value='my sine wave')
amplitude = Slider(title="amplitude", value=1.0, start=1.0, end=8.0, step=0.1)
phase = Slider(title="phase", value=0.0, start=0.0, end=20.0, step=0.5)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    a = amplitude.value
    p = phase.value
    f = freq.value

    x = np.linspace(0,5,100000)
    y = a*np.sin((2*np.pi*f*x) - p)

    source.data = dict(x=x, y=y)

for w in [ amplitude, phase, freq]:
    w.on_change('value', update_data)


inputs = column(text, amplitude, phase, freq)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"