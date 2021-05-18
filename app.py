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
import pickle #Pickle for pickling (saving) the model 
import flask
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import os
 #app name
import pickle

#ex2 = pd.read_csv("ALL_TIME_TWEET_SENTIMENT.csv")

ex3 = pd.read_csv("ALL_TIME_TWEET_SENTIMENT_pt2.csv", low_memory=False)
#ex3 = ex3.append(ex2)

ex3 = ex3[['movie', 'Datetime', 'Text', 'count_racist', 'count_problematic', 'count_sexist',
       'count_stereotypes', 'count_whitewashing', 'count_stigma', 'score']]

ex3['count_racist']  = ex3['Text'].str.count("racist")
ex3['count_problematic']  = ex3['Text'].str.count("problematic")
ex3['count_sexist']  = ex3['Text'].str.count("sexist")
ex3['count_stereotypes']  = ex3['Text'].str.count("stereotype")
ex3['count_whitewashing']  = ex3['Text'].str.count("whitewashing")
ex3['count_stigma']  = ex3['Text'].str.count("stigma")

class Graph(dbb.Block):
    def layout(self):
        return html.Div([
            dcc.Dropdown(
                id=self.register('dropdown'),
                options=self.data.options,
                value=self.data.value
            ),
     dcc.Dropdown( id =self.register('dropdown2'),
        options = [
            {'label':'count_racist', 'value':'count_racist' },
            {'label': 'count_sexist', 'value':'count_sexist'},
            {'label': 'count_problematic', 'value':'count_problematic'},
            {'label': 'count_whitewashing', 'value':'count_whitewashing'},
            {'label': 'count_stigma', 'value':'count_stigma'},
             {'label': 'count_stereotypes', 'value':'count_stereotypes'},
            ],
        value = 'count_racist'),
        dcc.Graph(id=self.register('graph2')),
        dcc.Graph(id=self.register('graph')),
        dcc.Graph(id=self.register('graph3')),
        dcc.Graph(id=self.register('graph4')),
        dcc.Graph(id=self.register('graph5'))
        ], style={'width': '500'})

    def callbacks(self):
        @self.app.callback(
            self.output('graph', 'figure'),
            self.output('graph2', 'figure'),
            self.output('graph3', 'figure'),
             self.output('graph4', 'figure'),
            self.output('graph5', 'figure'),
            [self.input('dropdown', 'value')],
     [self.input(component_id='dropdown2', component_property= 'value')]
        )
        def update_graph(selected_dropdown_value , selected_dropdown_value2):
            ex33 = ex3[ex3['movie'] == str(selected_dropdown_value)]
            ex33.Text = ex33.Text.str.wrap(30)
            ex33.Text = ex33.Text.apply(lambda x: x.replace('\n', '<br>'))
            # Creation of query method using parameters
            dif0= px.scatter(ex3, x='Datetime',y = ex3['count_racist'],
                            color='movie' )
            fig= px.line(ex33, x='Datetime',y = ex33['count_stigma'],
                           hover_data=["Text"] , color='score' )
            figgy = px.line(ex33, x='Datetime',y = ex33['count_racist'],
                       hover_data=["Text"], color= 'score')
            figgs = px.line(ex33, x='Datetime',y = ex33['count_stereotypes'],
                        hover_data=["Text"] , color = 'score')
            figgz = px.line(ex33, x='Datetime',y = ex33['count_problematic'],
                        hover_data=["Text"] , color = 'score')
            return  figgy, dif0,fig,figgs,figgz

app = dash.Dash('Hello World')

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
    
if __name__ == "main":
    app.run_server(debug=True)





