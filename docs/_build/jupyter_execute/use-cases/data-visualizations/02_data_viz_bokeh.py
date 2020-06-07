# Data Visualization with Bokeh
* **Author**: Pete Bryan (@MSSPete)
* **Project**: Infosec Jupyter Book
* **Public Organization**: Microsoft
* **License**: [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
* **Reference**: https://bokeh.org/

## Description

Often the most effective visualizations are those that are highly customised to the dataset they are representing, and that allow a user to interact with the data to interrogate it further. [Bokeh]("https://bokeh.org/") is a highly flexible and effective data visualization library in Python that can be used to create rich interactive visualizations. Whilst it requires more work than other methods to plot data its customizability makes it ideal for more advanced users who are looking to create thier own visualizations. 

### Pre-requisites - Reading
* [Intro to Pandas](https://infosecjupyterbook.com/fundamentals/libraries/pandas.html)

## Importing Libraries
Pre-requisites:

* pip install pandas
* pip install bokeh
* pip install networkx

# Imports
import pandas as pd
from math import pi
import numpy as np
import datetime
import networkx as nx
from bokeh.io import output_notebook, show
from bokeh.palettes import Spectral10, Category10, Category20c
from bokeh.plotting import figure, from_networkx
from bokeh.transform import factor_cmap, cumsum
from bokeh.models import RadioButtonGroup, HoverTool, Slider, ColumnDataSource
from bokeh.layouts import column

# Bokeh has a number of output options, as we want to output inline in the notebook we need to set output_notebook()
output_notebook()

print('Imports complete')

# Import our network data - originally from https://github.com/hunters-forge/mordor/tree/master/datasets/large/apt29/day1/zeek
data = pd.read_csv("../../../datasets/flow_logs.csv", index_col=0, parse_dates=True)
print("Data loaded")

def total_b(row):
    return row['src_bytes'] + row['dst_bytes']

def total_p(row):
    return row['src_packets'] + row['dst_packets']

# Add some additional aggregated data fields to our table
data['total_bytes'] = data.apply(total_b, axis=1)
data['total_packets'] = data.apply(total_p, axis=1)
# Clean some of our data to make plotting cleaner
clean_data = data.dropna().copy()
clean_data.head()

Bokeh can be used to create simple static plots, of the same format that Pandas allows natively, however creating them is more involved. To create a plot a few basic elements are required:
- A figure: This is our visualizations canvas, where you can set the size, titles and other elements
- One or more Glyghs: These are the visual elements of or plot and vary depending on what sort of visualization you are creating.
    - In the example below our glyph is a sinle vbar glyph

</br>
Once we have these elements we can customize a range of other elements regarding the visualization. Whilst Bokeh has defaults for many values such as colors, and chart axes you will want to manually set these for maximum impact.

# Take a subset of our data and groupby for categorical plotting
serv_data= clean_data[clean_data['dst_port']<1023].copy()
serv_data['dst_port'] = serv_data['dst_port'].astype(str)
group = serv_data.groupby('dst_port')

# Apply a categorical color mapping to our datset
cmap = factor_cmap('dst_port', palette=Spectral10, factors=sorted(serv_data['dst_port'].unique()))

#Create a Bokeh plot, set size and key elements of the blot
p = figure(plot_height=350, x_range=group, title="Bytes by protocol",
           toolbar_location=None, tools="")

#Add vertical bars to our plot
p.vbar(x='dst_port', top='dst_bytes_mean', width=1, source=group,
       line_color=cmap, fill_color=cmap)

# Set our axes setting and labels
p.y_range.start = 0
p.xgrid.grid_line_color = None
p.xaxis.axis_label = "Dst Port"
p.xaxis.major_label_orientation = 1.2
p.outline_line_color = None

show(p)

Once you have a visualization you can start to add interactivity, there are numerous ways to do this but the simplest is to all Bokeh's pre-built tools to the figure. In the example below we have added the 'hover' tool which displays information about a datapoint as you hover over it.</br>
Try this out by hovering over each section of the pie chart below.

# Aggregate data for pie chart
pie_data = group['dst_bytes'].agg(np.mean)
pie_data = pie_data.reset_index(name='bytes').rename(columns={'index':'port'})

# Calculate angles for pie chart wedges
pie_data['angle'] = pie_data['bytes']/pie_data['bytes'].sum() * 2*pi
pie_data['color'] = Category10[len(pie_data.index)]

# Set our Bokeh figure - enable hover over
p = figure(plot_height=250, plot_width=300, title="Bytes by port", toolbar_location=None,
           tools="hover", tooltips="@dst_port: @bytes", x_range=(-0.5, 1.0))

# Add wedges to the plot
p.wedge(x=0, y=1, radius=0.5,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='dst_port', source=pie_data)

# Set axes
p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None

show(p)

Other interactions you can add to a visualization include the ability to pan and zoom in data. In the scatterplot below we have enabled some of these. </br>
The tools are accessed via the toolbar in the bottom right of the visualization, try them out by selecting one and them clicking on the main body of the visualization.

# Add colors to our dataset based on the destination port
scatter_data = serv_data.copy()
ports = scatter_data['dst_port'].unique()
palette = Category20c[len(ports)]
colormap = {ports[i]: palette[i] for i in range(len(ports))}
scatter_data['colors'] = [colormap[x] for x in scatter_data['dst_port']]

# Create a figure and add a number of tools
p = figure(plot_height=800, plot_width=800, title = "Protocol bytes vs packets",
           tools="pan,wheel_zoom,box_zoom,reset,hover", 
           tooltips="Bytes = @dst_bytes - Packets = @dst_packets, Port = @dst_port", 
           toolbar_location="below")

# format our data in a ColumnDataSource format
data = ColumnDataSource(scatter_data)
# Add scatter object 
p.scatter("dst_bytes", "dst_packets", source=data, legend_field="dst_port", fill_alpha=0.8, size=7,
          fill_color='colors', line_color='colors')

# Format axes
p.xaxis.axis_label = 'Bytes'
p.yaxis.axis_label = 'Packets'


show(p)

In the visualizations we have created so far we have had a single glyph showing all our data, this has limited the level of interactivity we can enable. In the scatter plot below rather than plotting all the points as a scatter glyph we instead plot each point as individual circle glyphs. </br>
This means that we use an interactive legend to show or hide certain data points. Try this out by clicking on each item in the legend to toggle it in the main plot.

# Format data, including timeseries
scatter_data_2 = serv_data.copy()
scatter_data_2['timestamp'] = scatter_data_2['ts'].apply(lambda x: datetime.datetime.fromtimestamp(x))
scatter_data_2 = scatter_data_2.groupby('dst_port')

# Create our Bokeh Figure
p = figure(plot_width=800, plot_height=450, x_axis_type="datetime")
# Add a title after
p.title.text = 'Click on legend entries to hide the corresponding points'

# Add our scatter points as seperate circle items so we can filter
colors = Category10[10] 
col_i = 0
for group in scatter_data_2.groups.keys():
    c_data = scatter_data_2.get_group(group)
    c_data.sort_values('timestamp', ascending=False)
    color = colors[col_i]
    p.circle(c_data['timestamp'], c_data['total_packets'], line_width=2,alpha=0.8, legend_label=group, muted_alpha=0.2, color=color)
    col_i += 1
    
# Set our interactive legend action
p.legend.click_policy="mute"
# Set our axes settings
p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Total Packets' 
    
show(p)

Bokeh has a wide range of pre-built interactive elements you can enable, however you can also create your own using [widgets]("https://docs.bokeh.org/en/latest/docs/user_guide/interaction/widgets.html"). These widgets are similar to iPython widgets and can do a range of things such as select items in a list, enter values, or in the example below set a value in a list.</br>
One a widget has been set you can [link the widget to a visualization]("https://docs.bokeh.org/en/latest/docs/user_guide/interaction/linking.html") and set the value of the widget to a variable in our plots.</br>
In the example below we link the value of the slider to the value assigned to size of our data points on the plot, adjust the slider and see how the plot changes in real time.</br>
As well as linking widgets and plots you can link multiple plots together so that a change made to one is reflected in others, this can be useful when looking at the same data set from multiple perspectives.


# Set a slider object
slider = Slider(start=1, end=50, step=1, value=7, bar_color='#37c6ed', show_value=False, title="Move the slider to adjust point size")

# Create our Bokeh figure
p = figure(plot_height=800, plot_width=800, title = "Protocol bytes vs packets",
           tools="pan,wheel_zoom,box_zoom,reset,hover", 
           tooltips="Bytes = @dst_bytes - Packets = @dst_packets, Port = @dst_port", 
           toolbar_location="below")
# Add scatter object to our figure
s = p.scatter("dst_bytes", "dst_packets", source=ColumnDataSource(scatter_data), legend_field="dst_port", fill_alpha=0.8, size=7,
          fill_color='colors', line_color='colors')

# Format axes
p.xaxis.axis_label = 'Bytes'
p.yaxis.axis_label = 'Packets'

# Link the value of our slider to the size value in our scatter object
slider.js_link('value', s.glyph, 'size')

# Display the slider and plot togeher in a column layout
show(column(slider, p))

Bokeh also has a number of integrations to make plotting simple. One of these that is particularly useful when investigating network data is [integration with Networkx]("https://docs.bokeh.org/en/latest/docs/user_guide/graph.html?highlight=networkx").</br> Bokeh can take a Networkx graph and plot it on a figure, in addition you can apply a number of Bokeh's interactive options to this allowing for interactive networkx plots.

# Create a edgelist from our dataset
edgelist= pd.DataFrame({"source": clean_data['src_ip'].to_list(), "target": clean_data['dst_ip'].to_list(), "weight":clean_data['total_bytes'].to_list()})
# Create networkx graph from our edgelist
G = nx.from_pandas_edgelist(edgelist)

# Create our Bokeh figure
p = figure(title="Network node communication graph", x_range=(-2.5,2.5), y_range=(-2.5,2.5))
# Set our hover items and add it to the plot
node_hover_tool = HoverTool(tooltips=[("IP address", "@index")])
p.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

# Generate the graph from networkx and add it to the figure
graph = from_networkx(G, nx.circular_layout, scale=2, center=(0,0))
p.renderers.append(graph)

# Hide all axes
p.xaxis.visible = False
p.xgrid.visible = False
p.yaxis.visible = False
p.ygrid.visible = False

show(p)

## Summary
This is just a small sample of what you can do with Bokeh when investigating network data, there is a huge range of customization options avaliable to you. If you want to learn more Bokeh has some excellent [documentation]("https://docs.bokeh.org/en/latest/docs/user_guide.html") and if you are searching for inspiration thier [gallery]("https://docs.bokeh.org/en/latest/docs/gallery.html") has some excellent and innovative examples.