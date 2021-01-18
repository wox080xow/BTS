import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from jupyter_dash import JupyterDash

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

df_env = pd.read_csv("C:/Users/Student/EnvironmentalVar.csv")
df_eco = pd.read_csv("C:/Users/Student/EconomicVar.csv")
df_house = pd.read_csv("C:/Users/Student/HouseVar.csv")
available_indicators = df_env.columns.tolist()
available_indicators.pop(0)
available_indicators1 = df_eco.columns.tolist()
available_indicators1.pop(0)
available_indicators2 = df_house.columns
# layout
app.layout = html.Div([
        html.Div([
        html.H2(children='�x�_���Ы����ҲӲӹ�',style={'font-weight':'bold'}),
    html.Div([
            html.H2('�����ܼƬ�����',style={'text-align':'center','color':'#FF8800', 'font-family':'�L�n������','font-weight':'bold'}),
        html.Div([
            html.H5("�п��x�b�����ܼ�",style={'font-weight':'bold'}),
            #�U�Ԧ��z�ﾹ�]�w
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='ĵ�'
            ),
        ],
        style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.H5("�п��y�b�����ܼ�",style={'font-weight':'bold'}),
            
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='�Ǹo��'
            ),
        ],
        style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic')]),
    html.Div([],style={'height': '200px'}),

    
    html.Div([
            html.H2('�g���ܼƬ�����',style={'text-align':'center','color':'#FF8800', 'font-family':'�L�n������','font-weight':'bold'}),
        html.Div([
            html.H5("�п�ܸg���ܼ�",style={'font-weight':'bold'}),
            
            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators1],
                value='�ұo���J�`�p'
            ),
        ],
        style={'width': '30%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic1'),
    html.Div([],style={'height': '200px'}),
        
    html.Div([
            html.H2('�ЫίS�ʬ�����',style={'text-align':'center','color':'#FF8800', 'font-family':'�L�n������','font-weight':'bold'}),
        html.Div([
            html.H5("�п�ܩЫίS��",style={'font-weight':'bold'}),
            
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators2],
                value='�ж���'
            ),
        ],
        style={'width': '30%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic2'),
       ])
    ])
],style={'padding': '5%', 'width': '750px', 'margin': '0px auto', 'font-family':'�L�n������','backgroundColor':'white'
        })
],style={'padding': '5%', 'background-image':'url("https://cdn.pixabay.com/photo/2018/01/18/11/44/geometric-3090094_1280.png")'})

# callback
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    dash.dependencies.Input('xaxis-column', 'value'),
    dash.dependencies.Input('yaxis-column', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name):
    if xaxis_column_name == None or yaxis_column_name == None:
        fig = px.scatter()
        fig.update_traces(textposition='top center')
        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest',font_size=16,dragmode = False)
        return fig
    else:
        fig = px.scatter(x=df_env[xaxis_column_name],
                         y=df_env[yaxis_column_name], text = df_env['�a��'],size = df_env[xaxis_column_name],color= df_env[yaxis_column_name])

        fig.update_traces(textposition='top center')

        fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest',font_size=16,dragmode = False)

        fig.update_xaxes(title=xaxis_column_name)

        fig.update_yaxes(title=yaxis_column_name)

        return fig

@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    dash.dependencies.Input('xaxis-column1', 'value'))
def update_graph(xaxis_column_name):
    if xaxis_column_name == None:
        fig = px.bar()
        fig.update_layout(yaxis={'categoryorder':'total ascending'},font_size=16,dragmode = False)
        return fig
    else:
        fig = px.bar(x=df_eco[xaxis_column_name], y=df_eco['�a��'],color_discrete_sequence=['#00DDDD'], labels={'y':"�a��"})
    
        fig.update_xaxes(title=xaxis_column_name)

        fig.update_layout(yaxis={'categoryorder':'total ascending'},font_size=16,dragmode = False)

        return fig

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    dash.dependencies.Input('xaxis-column2', 'value'))
def update_graph(xaxis_column_name):
    if xaxis_column_name == None:
        fig = px.histogram()
        fig.update_layout(yaxis={'categoryorder':'total ascending'},font_size=16,dragmode = False,yaxis_title="�ƶq")
        return fig
    else:
        if xaxis_column_name == '�Ӽh��' :
            range1 = [-1,20]
        else:
            range1 = [-1,6]

        fig = px.histogram(x=df_house[xaxis_column_name],range_x=range1,range_y=[-1000,max(df_house.groupby(xaxis_column_name).count().iloc[:,:1].values.tolist())[0]*1.1],color_discrete_sequence=['#FF0000'])

        fig.update_xaxes(title=xaxis_column_name)

        fig.update_layout(yaxis={'categoryorder':'total ascending'},font_size=16,dragmode = False,yaxis_title="�ƶq")

        return fig

# main
if __name__ == '__main__':
    app.run_server(debug = True)
