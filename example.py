import pixelplot
import random

x = map(lambda x: x/10, range(0, 1+100))
x = range(1+10)
y = map(lambda x: random.randint(0, 500), x)
points = list(zip(x, y))

pixelplot.xy_bars(300, 300, points, bar_width=16,
        x_min=-1,
        x_max=11,
        x_tick_interval=1,
        x_tick_length=2,
        x_tick_space=1,
        x_tick_label_decimals=0,
        x_label="# of fluffdergs",
        x_label_space=10,
        x_grid_style=(2, 2),
        y_min=0,
        y_max=500,
        y_tick_interval=-10,
        y_tick_length=2,
        y_tick_space=1,
        y_tick_label_decimals=0,
        y_label="Floofiness",
        y_label_space=10,
        y_grid_style=(2, 2),
        data_label_font="slkscr-8.pil",
        axis_label_font="slkscr-8.pil",
        bgcolor="white",
        fgcolor="black").show()