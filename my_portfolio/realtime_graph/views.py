from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
import plotly.graph_objects as go
import numpy as np
import random as ran


def line_char(update_data):
    # Add data
    time_x = np.arange(0, 100, 0.5)
    scraped_data = np.random.rand(200)


    trace0 = go.Scatter(
        x = time_x,
        y = scraped_data,
        name = 'scraped_1',
        line = dict(
            color = ('rgb(205, 12, 24)'),
            width = 4)
    )
    data = [trace0]

    # Edit the layout
    layout = dict(title = dict(text = 'scraped_data demonstration'),
                    xaxis = dict(title = 'time'),
                    yaxis = dict(title = 'scraped_data'),
                    )

    fig = dict(data=data, layout=layout)
    
    return fig

def line_charts(x):
    fig = go.Figure(data=line_char(x))
    return fig.to_html(include_plotlyjs=False)  # ❷


class LineChartsView(TemplateView):  # ❶
    template_name = "realtime_graph.html"

    def get_context_data(self, **kwargs):
        update_data = ran.random()
        context = super(LineChartsView, self).get_context_data(**kwargs)
        context["plot"] = line_charts(update_data)  # ❸
        return context
    
class IndexView(TemplateView):
    template_name = "realtime_graph.html"
    
# graph = IndexView.as_view()
plot = LineChartsView.as_view()

