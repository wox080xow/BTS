import dash
# from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from textwrap import dedent

df = pd.read_csv(
    'data/AreaPredto2021.csv')
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
df['value'] = df['value'].astype('int')

# fig
areas = ['大同區', '大安區', '信義區', '內湖區', '萬華區', '士林區', '中山區',
         '北投區', '中正區', '南港區', '松山區', '文山區']


fig = go.Figure()
fig.add_trace(go.Bar(x=areas, y=[24455, 6757, 6736, 5545, 5350, 722, 177,
                                 -2008, -2108, -8913, -16181, -17510],
                     base=0,
                     marker_color=['#8ac6d1', '#8ac6d1', '#8ac6d1',
                                   '#8ac6d1', '#8ac6d1', '#8ac6d1',
                                   '#8ac6d1', '#ffb6b9', '#ffb6b9',
                                   '#ffb6b9', '#ffb6b9', '#ffb6b9'],
                     name='行情價'))
fig.update_layout(
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='坪/千元',
        titlefont_size=16,
        tickfont_size=14,
    ),
    barmode='group',
    bargap=0.15,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1,  # gap between bars of the same location coordinate.
    dragmode=False
)

# Dash app
app = dash.Dash(__name__)
application = app.server

app.title = '房價趨勢準準抓'

# 1. layout
app.layout = html.Div(
        html.Div(
        children=[
            # H1
            html.H1(
                children='台北市房價趨勢準準抓',
                style={'textAlign': 'left',
                       'color': '#09194F'}),
            # Markdown
            dcc.Markdown("請選擇所欲查詢地區"),

            # Dropdown
            dcc.Dropdown(
                id='Area-dropdown',
                options=[{'label': i, 'value': i}
                         for i in df.Area.unique()],
                multi=True,
                value=['松山區']),
            # Graph 1
            html.H2(
                children='2014-2021年 台北市行政區房價預測',
                style={'textAlign': 'center',
                       'color': '#00818A'}),

            dcc.Graph(id='timeseries-graph'),

            # H4
            html.H4(children='2020年Q4-2021年為預測值',
                    style={
                        'textAlign': 'right',
                        'color': '#00818A'
                    }),

            html.Br(),
            html.Br(),
            html.Br(),

            # Graph 2
            html.H2(
                children='2020年 台北市行政區合理行情價格推估',
                style={'textAlign': 'center',
                       'color': '#ec693f'}),
            dcc.Graph(figure=fig),

            # H4
            html.H4(children='以2020年市場價格作為基準',
                    style={
                        'textAlign': 'right',
                        'color': '#ec693f'
                    }),
        ],style={'padding': '5%', 'width': '750px', 'margin': '0px auto', 'font-family':'微軟正黑體','backgroundColor':'white'}),
        
    style={'padding':'5%','background-image':
                    'url("https://cdn.pixabay.com/photo/2018/01/18/11/44/geometric-3090094_1280.png")'})

# 2. callback
# make apps interactive


@ app.callback(
    dash.dependencies.Output('timeseries-graph', 'figure'),
    dash.dependencies.Input('Area-dropdown', 'value'))
def update_graph(Area_values):
    dff = df.loc[df['Area'].isin(Area_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Area'] == Area]['Date'],
            y=dff[dff['Area'] == Area]['value'],

            mode='lines+markers',
            name=Area,
            marker={
                'size': 7,
                'opacity': 0.5,
                'line': {'width': 0.9, 'color': 'white'}
            }
        ) for Area in dff.Area.unique()],

        'layout': go.Layout(
            #             title="2014-2022年 台北市行政區房價預測",
            xaxis={'title': '日期'},
            yaxis={'title': '房屋價格(萬/坪)'},
            # top / right / bottom / left
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest',
            dragmode=False
        )
    }

# 3. Name Convention
if __name__ == '__main__':
    # app.run_server(host="localhost")
    application.run(host = '0.0.0.0', debug = True, port = 8052)
