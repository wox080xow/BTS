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
        html.H2(children='台北市房屋環境細細察',style={'font-weight':'bold'}),
    html.Div([
            html.H2('環境變數相關圖',style={'text-align':'center','color':'#FF8800', 'font-family':'微軟正黑體','font-weight':'bold'}),
        html.Div([
            html.H5("請選擇x軸環境變數",style={'font-weight':'bold'}),
            #下拉式篩選器設定
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='警察局'
            ),
        ],
        style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.H5("請選擇y軸環境變數",style={'font-weight':'bold'}),
            
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='犯罪數'
            ),
        ],
        style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic')]),
    html.Div([],style={'height': '200px'}),

    
    html.Div([
            html.H2('經濟變數相關圖',style={'text-align':'center','color':'#FF8800', 'font-family':'微軟正黑體','font-weight':'bold'}),
        html.Div([
            html.H5("請選擇經濟變數",style={'font-weight':'bold'}),
            
            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators1],
                value='所得收入總計'
            ),
        ],
        style={'width': '30%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic1'),
    html.Div([],style={'height': '200px'}),
        
    html.Div([
            html.H2('房屋特性相關圖',style={'text-align':'center','color':'#FF8800', 'font-family':'微軟正黑體','font-weight':'bold'}),
        html.Div([
            html.H5("請選擇房屋特性",style={'font-weight':'bold'}),
            
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators2],
                value='房間數'
            ),
        ],
        style={'width': '30%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic2'),
       ])
    ])
],style={'padding': '5%', 'width': '750px', 'margin': '0px auto', 'font-family':'微軟正黑體','backgroundColor':'white'
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
                         y=df_env[yaxis_column_name], text = df_env['地區'],size = df_env[xaxis_column_name],color= df_env[yaxis_column_name])

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
        fig = px.bar(x=df_eco[xaxis_column_name], y=df_eco['地區'],color_discrete_sequence=['#00DDDD'], labels={'y':"地區"})
    
        fig.update_xaxes(title=xaxis_column_name)

        fig.update_layout(yaxis={'categoryorder':'total ascending'},font_size=16,dragmode = False)

        return fig

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    dash.dependencies.Input('xaxis-column2', 'value'))
def update_graph(xaxis_column_name):
    if xaxis_column_name == None:
        fig = px.histogram()
        fig.update_layout(yaxis={'categoryorder':'total ascending'},font_size=16,dragmode = False,yaxis_title="數量")
        return fig
    else:
        if xaxis_column_name == '樓層數' :
            range1 = [-1,20]
        else:
            range1 = [-1,6]

        fig = px.histogram(x=df_house[xaxis_column_name],range_x=range1,range_y=[-1000,max(df_house.groupby(xaxis_column_name).count().iloc[:,:1].values.tolist())[0]*1.1],color_discrete_sequence=['#FF0000'])

        fig.update_xaxes(title=xaxis_column_name)

        fig.update_layout(yaxis={'categoryorder':'total ascending'},font_size=16,dragmode = False,yaxis_title="數量")

        return fig

# main
if __name__ == '__main__':
    app.run_server(debug = True)
