import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Button, Select, CustomJS
from bokeh.plotting import figure

import os

sine_signals = []

x = np.linspace(0, 5, 100000)
y = np.sin(2*np.pi*x)

source1 = ColumnDataSource(data=dict(x=x, y=y))
source2 = ColumnDataSource(data={"x": [], "y": []})


# set up plot
plot1 = figure(height=400, width=1200,
               tools="crosshair,pan,reset,save,wheel_zoom",
               x_range=[0, 5], y_range=[-10.0, 10.0])

plot1.line('x', 'y', source=source1, line_width=3, line_alpha=0.6)

# result plot
plot2 = figure(height=400, width=1200,
               tools="crosshair,pan,reset,save,wheel_zoom",
               x_range=[0, 5], y_range=[-10.0, 10.0])

plot2.line('x', 'y', source=source2, line_width=3, line_alpha=0.6, color="red")


# control panel

amplitude = Slider(title="amplitude", value=1.0, start=1.0, end=8.0, step=0.1)
phase = Slider(title="phase", value=0.0, start=0.0, end=10.0, step=0.1)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)
add_wave_btn = Button(label="add wave", button_type="primary")


wave_select_box = Select(title="sine waves", options=[])
delete_wave_btn = Button(label="delete wave", button_type="danger")

download_btn = Button(label="Download the signal as CSV",
                      button_type="success", max_width=300)


def update_result_plot():
    num_of_waves = len(sine_signals)
    if num_of_waves == 0:
        x = []
        y = []
        source2.data = dict(x=x, y=y)

    else:
        x = np.linspace(0, 5, 100000)

        num_of_data_points = len(sine_signals[0]["data"][1])

        y = [0.0] * num_of_data_points

        for j in range(num_of_data_points):
            for i in range(num_of_waves):
                y[j] += sine_signals[i]["data"][1][j]

        source2.data = dict(x=x, y=y)


def update_data(attrname, old, new):

    a = amplitude.value
    p = phase.value
    f = freq.value

    x = np.linspace(0, 5, 100000)
    y = a*np.sin((2*np.pi*f*x) - p)

    source1.data = dict(x=x, y=y)


for w in [amplitude, phase, freq]:
    w.on_change('value', update_data)


def add_wave_handler():
    x = source1.data["x"].tolist()
    y = source1.data["y"].tolist()
    if (x is not None) and (y is not None):
        sine_wave = {
            "data": [x, y],
            "name": f"{freq.value}/freq,{amplitude.value}/amp,{phase.value}/phase"
        }
        sine_signals.append(sine_wave)

        list_of_signals = map(lambda x: x["name"], sine_signals)

        wave_select_box.options = list(list_of_signals)
        wave_select_box.value = wave_select_box.options[0]

        update_result_plot()

    else:
        print("nothing to show")


def delete_wave_handler():
    if len(sine_signals) >= 1:
        index = 0
        for i in range(len(sine_signals)):
            if sine_signals[i]["name"] == wave_select_box.value:
                index = i
                break
        sine_signals.pop(index)
        list_of_signals = map(lambda x: x["name"], sine_signals)
        wave_select_box.options = list(list_of_signals)
        wave_select_box.value = wave_select_box.options[0] if len(
            sine_signals) > 0 else ""
        update_result_plot()


add_wave_btn.on_click(add_wave_handler)
delete_wave_btn.on_click(delete_wave_handler)

download_btn.js_on_click(CustomJS(args=dict(source=source2),
                            code=open(os.path.join(os.path.dirname(__file__), "download.js")).read()))


# layout

deletion = column(wave_select_box, delete_wave_btn)

inputs = column(amplitude, phase, freq, add_wave_btn, deletion)

generator = column(row(plot1, inputs), column(plot2, download_btn))


curdoc().add_root(generator)
curdoc().title = "Signal Generator"
