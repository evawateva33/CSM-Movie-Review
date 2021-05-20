#!/usr/bin/env python
# coding: utf-8

# In[4]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

import dash_core_components as dcc
import dash_html_components as html
import dash_building_blocks as dbb
import plotly.express as px

import pickle
import pandas as pd  #Pandas for data pre-processing
import joblib

import flask
import numpy as np
from flask import Flask, request, jsonify, render_template


ex2 = pd.read_csv("ALL_TIME_TWEET_SENTIMENT.csv", lineterminator='\n')
ex3 = pd.read_csv("ALL_TIME_TWEET_SENTIMENT_pt2.csv", lineterminator='\n')
ex3 = ex3.append(ex2)
ex3 = ex3[['movie', 'Datetime', 'Text', 'count_racist', 'count_problematic', 'count_sexist',
       'count_stereotypes', 'count_whitewashing', 'count_stigma', 'score']]

ex3 = ex3.dropna()
class Graph(dbb.Block):
    def layout(self):
        return html.Div([
            dcc.Dropdown(
                id=self.register('dropdown'),
                options=self.data.options,
                value="Breakfast at Tiffany's",
                placeholder='Select specific movie to search'
            ),

        dcc.Input(id=self.register("input1"), type="text", placeholder="Input word to search",),
        #dcc.Input(id=self.register("input2"), type="text", placeholder="", debounce=True),

     dcc.Dropdown( id =self.register('dropdown2'),
        options = [
            {'label':'count_racist', 'value':'count_racist' },
            {'label': 'count_sexist', 'value':'count_sexist'},
            {'label': 'count_problematic', 'value':'count_problematic'},
            {'label': 'count_whitewashing', 'value':'count_whitewashing'},
            {'label': 'count_stigma', 'value':'count_stigma'},
             {'label': 'count_stereotypes', 'value':'count_stereotypes'},
            ],
        value = 'count_racist', placeholder="Select a word to see frequency of mentions"),
        dcc.Graph(id=self.register('graph2')),
        dcc.Graph(id=self.register('graph')),
        dcc.Graph(id=self.register('graph3'))

        ], style={'width': '500'})

    def callbacks(self):
        @self.app.callback(

            self.output('graph', 'figure'),
            self.output('graph2', 'figure'),
            self.output('graph3', 'figure'),
            self.input("input1", "value"),
            #self.input("input2", "value"),
            [self.input('dropdown', 'value')],
     [self.input(component_id='dropdown2', component_property= 'value')]
        )
        def update_graph(input1,selected_dropdown_value , selected_dropdown_value2):
            #ex3['count_custom_word'] = ex3['Text'].str.count(str(input1))
            ex33 = ex3[ex3['movie'] == str(selected_dropdown_value)]
            # Creation of query method using parameters
            dif0= px.scatter(ex3, x='Datetime', y = ex3['{}'.format(selected_dropdown_value2)],
                            color='movie')
            figgs = px.line(ex33, x='Datetime',y = ex33['count_stereotypes'],
                        hover_data=["Text"])
            figgz = px.line(ex33, x='Datetime', y = ex33['{}'.format(selected_dropdown_value2)],
                        hover_data=["Text"] , color = 'score')
            return   figgz,dif0,figgs

app = dash.Dash(__name__)
server = app.server
fig_names = ex3.movie.unique()
options=[{'label': x, 'value': x} for x in fig_names]
data = {
    'options': options,
    'value': None
}
n_graphs =1
graphs = [Graph(app, data) for _ in range(n_graphs)]

app.layout = html.Div(
    [html.Div(graph.layout, className='six columns')
    for graph in graphs],
    className='container'
)

for graph in graphs:
    graph.callbacks()

if __name__ == '__main__':
    app.run_server( port=3339)
