import pandas as pd
import dash_auth
from datetime import date
from datetime import datetime as dt

import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output, State

import base64
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_table
import plotly.express as px
import dash_bootstrap_components as dbc 

from datetime import date, timedelta

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

import networkx as nx

from itertools import tee

# import networkx as nx
# from networkx.drawing.nx_pydot import graphviz_layout


import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

import itertools

# VALID_USERNAME_PASSWORD_PAIRS = {
# #     'Admin': 'zewdu2'
# # }

 

mapbox_access_token = 'pk.eyJ1IjoiemV3ZHU5NCIsImEiOiJja2x1emt6eW8wNWd4MnZvNjN4NzFpcmM1In0.FZnjY0hdpPcUV0XCeGqM3w'

#Data
df = pd.read_csv('/Users/zewdumogesse/Documents/Loyalty /land_only new.csv')
df['Date'] = pd.to_datetime(df['TTime'])
# df['Date'] = pd.to_datetime(df['Date'],)
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

df_filtered = pd.read_csv('/Users/zewdumogesse/Documents/Loyalty /df_filtered new2.csv')
df_filtered['date'] = pd.to_datetime(df_filtered['date']) 
df_filtered = df_filtered[['date', 'merchant', 'miles']]


df2 = pd.read_csv('/Users/zewdumogesse/Documents/Loyalty /df_final new2.csv')
df2.drop(columns=['MerchantCount'],inplace = True)
df2.drop(columns=['Unnamed: 0'],inplace = True)
df2['Date'] = pd.to_datetime(df2['Date'])
# df2['Date'] = df2['Date'].dt.strftime('%m/%d/%Y')
currentday = 11
currentmonth = 12
currentyear = 2020 

df2['Frequency'] = df2['merchant'].map(df2['merchant'].value_counts())

df3 = df2[['merchant', 'Frequency']]
df3 = df3.sort_values(by='Frequency', ascending=True)

df4 = df2[['merchant', 'Frequency']]

df_gas = df[df['Gas'].isin(['GAS STATION', 'GAS STATIONS', 'CARS, FUEL & UTILITIES',
       'LUBRICANTS', 'FUEL'])]

df_food = df[df['Food'].isin(['SUPERMARKET', 'FROZEN DESSERT', 'BREAD', 'SEA FOOD',
       'GROCERIES'])]
df_home =  df[df['Home'].isin(['HOME APPLIANCE', 'HOME SUPPLIES'])]
df_clothing_beauty = df[df['Clothing and beauty'].isin(['EYEWEAR', 'TEXTILE', 'CLOTHING', 'SKINCARE', 'FOOTWEAR'])]
df_store = df[df['Clothing and beauty'].isin(['BOOKSTORE', 'PHARMACY', 'KIDS STORE', 'MALL'])]
df_others = df[df['Others'].isin(['WASTE MANAGEMENT', 'HARDWARE & MATERIALS', 'INSURANCE','CAFE', 'TRAVEL', 'COURIER', 'DRY CLEANING', 'POSTAL'])]


df_locations = df[['CustomerId', 'miles', 'latitude','longitude' ]]

df_combinations = df[['CustomerId','miles', 'Segment']]
df_combinations = df_combinations.groupby(['CustomerId','Segment'], sort=False).agg(Total_miles = ('miles','sum'),
                                               Frequency = ('miles','size'))
df_combinations = df_combinations.reset_index()
df_combinations['Percentage'] = df_combinations['Frequency'].div(df_combinations['Frequency'].sum()).mul(100).round(5)
df_combinations['Percentage'] = df_combinations['Percentage'].astype(str) + '%'
df_combinations = df_combinations.sort_values(by='Total_miles', ascending=False)


df.dropna(subset=['merchant'], how='all', inplace=True)
df['TTime'] = pd.to_datetime(df['TTime'])
m_valuable = df[['TType', 'TTime', 'merchant', 'miles']]
m_valuable["miles"] = m_valuable["miles"].astype(int)
m_valuable['TTime'] = pd.to_datetime(m_valuable['TTime'])
m_valuable['Dates'] = pd.to_datetime(m_valuable['TTime']).dt.date
m_valuable['Date'] = m_valuable['Dates'].apply(lambda x: x.strftime('%Y-%m'))
m_valuable = m_valuable[['TType', 'Date', 'Dates', 'merchant', 'miles']]

m_valuable2 = m_valuable.groupby(['Date', 'TType', 'merchant'])['miles'].sum().reset_index()
m_valuable2['percentage'] = m_valuable2['miles'] / m_valuable2.groupby(['Date'])['miles'].transform(sum)
m_valuable2 = m_valuable2[['Date', 'TType', 'merchant', 'miles', 'percentage']]

df_issued = m_valuable2[m_valuable2['TType'] =='I']
df_issued = df_issued.sort_values(by=['percentage'], ascending=False)
df_issued = round(df_issued, 2)

df_redeemed = m_valuable2[m_valuable2['TType'] =='R']
df_redeemed = df_redeemed.sort_values(by=['percentage'], ascending=False)
df_redeemed = round(df_redeemed, 2)

m_valuable_all = m_valuable[[  'Date', 'TType', 'merchant', 'miles']]
m_valuable_all = m_valuable_all.groupby(['Date', 'TType','merchant'])['miles'].sum().reset_index()
m_valuable_all['percentage'] = m_valuable_all['miles'] / m_valuable_all.groupby(['Date'])['miles'].transform(sum)
m_valuable_all1 = m_valuable_all[['Date', 'TType', 'merchant', 'miles', 'percentage']]
m_valuable_all1 = m_valuable_all1.sort_values(by=['percentage'], ascending=False)
m_valuable_all1 = round(m_valuable_all1, 2)
 

###### 
def select_month (month):
    df_new1 = pd.read_csv('/Users/zewdumogesse/Documents/Loyalty /df_graph new2.csv')

    df_new1['merchant'] = df_new1['merchant'].astype(str)
    df_new1 = df_new1[df_new1['month'] ==month]
    df_new1['merchant'] = df_new1['merchant'].str.strip('(,)').str.split(',')
    df_new1 = df_new1.explode('merchant')
    
    df_new1['Frequency'] = df_new1['merchant'].map(df_new1['merchant'].value_counts())
    df_new1 = df_new1[df_new1.groupby('CustomerId').CustomerId.transform('size') > 1]
    df_new1 = df_new1.groupby('CustomerId').merchant.agg([('count', 'count'), ('merchant', ', '.join)])

    df_new = df_new1.groupby(['merchant']).size().reset_index().rename(columns={0:'Frequency'})
    df_new = df_new.reset_index()
    df_new = df_new.sort_values(by = ('Frequency'), ascending = False)
    df_new = df_new[['merchant', 'Frequency']]
    df_new = df_new.replace("'", '', regex=True)

    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    df_new['Node_pairs'] = df_new['merchant'].str.split(',').apply(lambda x: list(pairwise(x)))
    df_new = df_new.explode('Node_pairs')
    df_new['Node1'] = df_new['Node_pairs'].str[0]
    df_new['Node2'] = df_new['Node_pairs'].str[1]

    df_new = df_new[['Node1', 'Node2', 'Frequency']]
    df_new = df_new.sort_values(by =('Frequency'), ascending = False)
    df_new = df_new.head(50)
    return df_new
######


#Date picker
# m_valuable = m_valuable.groupby(['Dates', 'TType', 'merchant'])['miles'].sum().reset_index()
# m_valuable['percentage'] = m_valuable['miles'] / m_valuable2.groupby(['Date'])['miles'].transform(sum)
# m_valuable['Dates'] = pd.to_datetime(m_valuable['Dates'])
# df.set_index('Dates', inplace=True)
# print(df[:5][['TType', 'merchant', 'miles','percentage']])

image_filename =  r'/Users/zewdumogesse/Documents/Loyalty /logo.png'
# logo = mpimg.imread('/Users/zewdumogesse/Documents/Loyalty /logo.png')
encoded_logo = base64.b64encode(open(image_filename, 'rb').read())
logo = html.Img(src='data:image/png;base64,{}'.format(encoded_logo.decode()),style={'width':'19vh'})

colors = {'background': '#FAF9F9', 'text': '#0425CF'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

fnameDict = {'Overall':[''],
            'Gas': ['GAS STATIONS', 'GAS STATION', 'LUBRICANTS', 'Fuel','CARS, FUEL & UTILITIES'],
             'Food': ['FROZEN DESSERT', 'SUPERMARKET','SEA FOOD','BREAD','GROCERIES' ],
             'Home': ['HOME APPLIANCE', 'HOME SUPPLIES' ],
            #  'Clothing and beauty': ['CLOTHING', 'FOOTWEAR','EYEWEAR', 'SKINCARE', 'TEXTILE'],
            # #  'Store': ['BOOKSTORE', 'KIDS STORE','PHARMACY', 'MALL'],
            #  'Others': ['COURIER', 'TRAEL','HARDWARE & MATERIALS', 'WASTE MANAGEMENT', 'CAFE', 'INSURANCE', 
            #             'CHOLESTEROL', 'POSTAL', 'DRY CLEANING'],
             }

names = list(fnameDict.keys())

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
 
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('About', href='#')),
        dbc.NavItem(dbc.NavLink('Products', href='#')),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('More pages', header=True),
                dbc.DropdownMenuItem('Admin Page', href='#'),
                # dbc.DropdownMenuItem('Tasks', href='#'),
                dbc.DropdownMenuItem('Customers', href='#'),
                dbc.DropdownMenuItem('Offers', href='#'),
                dbc.DropdownMenuItem('Rewards', href='#'),
                dbc.DropdownMenuItem('Logout', href='#'),
            ],
            nav=True,
            in_navbar=True,
            label='More',
        ),
    ],
    brand=' ',
    brand_href='#',
    color='#07273B',
    dark=True,
)

# Modal
with open("/Users/zewdumogesse/Documents/Loyalty /description.txt", "r") as f:
    howto_md = f.read()

modal_overlay = dbc.Modal(
    [
        dbc.ModalBody(html.Div([dcc.Markdown(howto_md)], id="howto-md")),
        dbc.ModalFooter(dbc.Button("Close", id="howto-close", className="howto-bn")),
    ],
    id="modal",
    size="lg",
)

button_howto = dbc.Button(
    "About the dashboard",
    id="howto-open", 
    outline=True,
    color="info",
    # Turn off lowercase transformation for class .button in stylesheet
    style={"textTransform": "none"},
)
########-------- PUT EVERYTHING HERE FOR TAB 1 --------########

Total_mile = html.Div(dcc.Graph(id='total_mile', config={'displayModeBar': False}), style = {'width': '80%','display':'inline-block'})

top_customers = html.Div(dcc.Graph(id='top_customers', config={'displayModeBar': False}), style = {'width': '40%','display':'inline-block'})
top_segments = html.Div(dcc.Graph(id='top_segments', config={'displayModeBar': False}), style = {'width': '40%','display':'inline-block'})


new_returning = html.Div(dcc.Graph(id='new_returning', config={'displayModeBar': False}), style = {'width': '40%','display':'inline-block'})
share_wallet = html.Div(dcc.Graph(id='share_wallet', config={'displayModeBar': False}), style = {'width': '40%','display':'inline-block'})

content_tab_1 = html.Div(children = [
    # html.Div(first_graph, style = {'vertical-align':'center', 'horizontal-align':'center'}),
    html.Div(Total_mile, style = {'vertical-align':'center', 'horizontal-align':'center'}),

    html.Div(children = [new_returning, share_wallet], style={'vertical-align':'center', 'horizontal-align':'center'}),

    html.Div(children = [top_customers, top_segments], style={'vertical-align':'center', 'horizontal-align':'center'}),

    # html.Div(box_plot, style = {'vertical-align':'center', 'horizontal-align':'center'})
],
style={'width': '140%'}) 

########-------- PUT EVERYTHING HERE FOR TAB 2 --------#######
map_loc = dcc.Graph(id='map-loc',
                    figure={'layout': {'clickmode': 'event+select'}},
                    config={'scrollZoom': True},
                    style={'height': '100vh','width': '150vh'}
                    )

returning_customers = html.Div(dcc.Graph(id='returning_customers', 
                                            config={'displayModeBar': False}), style = {'width': '80%','display':'inline-block'})

map_div = html.Div(map_loc, style={'float':'left'})

content_tab_2 = html.Div(children = [
    html.Div(children = [map_div], style={'vertical-align':'center', 'width': '70%', 'horizontal-align':'center'}),
    html.Div(returning_customers, style = {'vertical-align':'center', 'horizontal-align':'center'}),

],
style={'width': '140%'}) 

########-------- PUT EVERYTHING HERE FOR TAB 3 --------#######
all_merchants = df['merchant'].unique()
dropdownpicker = dcc.Dropdown(
        id="dropdownpicker",
        options=[{"label": x, "value": x} 
                 for x in all_merchants],
        searchable=True,
        value=all_merchants[:5],
    multi=True
) 

date_range_picker = dcc.DatePickerRange( 
            id='date_range_picker',
            clearable=True,
            min_date_allowed=dt(2019, 1, 1),
            max_date_allowed=df2['Date'].max().to_pydatetime(),
            initial_visible_month=dt(currentyear,df2['Date'].max().to_pydatetime().month, 1),
            start_date=(df2['Date'].max() - timedelta(6)).to_pydatetime(),
            end_date=df2['Date'].max().to_pydatetime(),
            display_format='M/D/Y',
            disabled=False
    )

search_table = dash_table.DataTable(
                    id='datatable',

                   columns=[{"name": i, "id": i} for i in m_valuable2.columns],
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    column_selectable="single",
                    row_selectable="multi",
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    style_table={
                                'maxHeight': '70vh',
                                'overflowY': 'scroll',
                                'margin-top': '5vh',
                                'margin-left': '3vh'
                                },

                    css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],

                    style_cell={
                        'whiteSpace': 'normal',
                        'textAlign': 'left',
                    },

                    style_header={'fontWeight': 'bold'},

                  

                    style_as_list_view=True
)
issued_reedemed = html.Div(dcc.Graph(id='issued_reedemed', config={'displayModeBar': False}), style = {'width': '130%','display':'inline-block'})

content_tab_3 = html.Div(children = [
    html.Br(),
    html.Label(id='category-lab22', children = 'Select Start and end date:'),
    html.Div(date_range_picker, style={'width': '100%', 'margin-left': '3vh', 'margin-top': '3vh', 'vertical-align':'center', 'horizontal-align':'center'}),
       html.Br(), 
    html.Label(id='category-lab2', children = 'Enter one or multiple merchants:'),   
    html.Div(dropdownpicker, style={'width': '100%', 'margin-left': '3vh', 'margin-top': '3vh', 'vertical-align':'center', 'horizontal-align':'center'}),
       html.Br(), 
    html.Div(children = [issued_reedemed, search_table  ], style = {'vertical-align':'center', 'horizontal-align':'center'}),
    html.Br(),
],
style={'width': '80%'}) 

date_picker = dcc.DatePickerSingle( 
            id='date_picker',
            clearable=True,
            min_date_allowed=dt(2019, 1, 1),
            max_date_allowed=dt(2020, 12, 11),
            initial_visible_month=dt(currentyear, currentmonth, currentday),
            date=dt(currentyear, currentmonth, currentday),
            display_format='M/D/Y',
            disabled=False
    )
picker_table = dash_table.DataTable(

                    id='pickertable',

                   columns=[{"name": i, "id": i} for i in df3.columns],
                    editable=True,
                    sort_action="native",
                    column_selectable="single",
                    row_selectable="multi",
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    style_table={
                                'maxHeight': '70vh',
                                'overflowY': 'scroll',
                                'margin-top': '5vh',
                                'margin-left': '3vh',
                                'width': '90%'
                                },

                    css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],

                    style_cell={
                        'whiteSpace': 'normal',
                        'textAlign': 'left',
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                    },

                    style_header={'fontWeight': 'bold'},

                  

                    style_as_list_view=True
)

picker_table2 = dash_table.DataTable(
                    id='pickertable2',

                   columns=[{"name": i, "id": i} for i in df4.columns],
                    editable=True,
                    sort_action="native",
                    column_selectable="single",
                    row_selectable="multi",
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    style_table={
                                'maxHeight': '70vh',
                                'overflowY': 'scroll',
                                'margin-top': '5vh',
                                'margin-left': '3vh',
                                'width': '90%',
                                },

                    css=[{
                        'selector': '.dash-cell div.dash-cell-value',
                        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                    }],

                    style_cell={
                        'whiteSpace': 'normal',
                        'textAlign': 'left',
                        'backgroundColor': 'rgb(50, 50, 50)',
                        'color': 'white'
                         
                    },

                    style_header={'fontWeight': 'bold'},

                  

                    style_as_list_view=True
)

month_dropdown = dcc.Dropdown(
                    id='month_dropdown',
                    options=[
                        {'label': '1', 'value': '1'},
                        {'label': '2', 'value': '2'},
                        {'label': '3', 'value': '3'},
                        {'label': '4', 'value': '4'},
                        {'label': '5', 'value': '5'},
                        {'label': '6', 'value': '6'},
                        {'label': '7', 'value': '7'},
                        {'label': '8', 'value': '8'},
                        {'label': '9', 'value': '9'},
                        {'label': '10', 'value': '10'},
                        {'label': '11', 'value': '11'},
                        {'label': '12', 'value': '12'},

                    ],
                    value='1'
                ),

picker_graph = html.Div(dcc.Graph(id='picker_graph', config={'displayModeBar': False}), style = {'width': '80%','display':'inline-block'})
network_graph = html.Div(dcc.Graph(id='network_graph', config={'displayModeBar': False}), style = {'width': '80%','display':'inline-block'})

content_tab_4 = html.Div(children = [
    html.Br(),
    html.Label(id='category-lab', children = 'Select Date'),
    html.Div(date_picker, style={'width': '100%', 'margin-left': '3vh', 'margin-top': '3vh', 'vertical-align':'center', 'horizontal-align':'center'}),
       html.Br(), 

    html.Div(picker_graph, style = {'vertical-align':'center', 'horizontal-align':'center'}),
    html.Br(),
    html.Div([
        html.Label("Number of combinations for each merchant and value for each merchant", style = {'vertical-align':'center', 'horizontal-align':'center'}),
        html.Br(),
        html.Div([picker_table], style={'width': '50%',  'display': 'inline-block'}),
        html.Div([picker_table2], style={'width': '50%', 'display': 'inline-block'}),
]),
 html.Br(), 
   html.Br(),
   html.Br(),

html.Label(id='month-tab', children = 'Select Month'),
html.Br(),
html.Div(month_dropdown, style = {'width': '20%','vertical-align':'center', 'horizontal-align':'center'}),
   html.Br(),
html.Br(),

html.Div(network_graph, style = {'vertical-align':'center', 'horizontal-align':'center'}),

],
style={'width': '100%'}) 





tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}


app.layout = html.Div([

     html.Div([  
    
    #  html.Div([
    # html.Div(children=logo), 
    #  ],style={'height': '100', 'width':'50', 'display': 'inline-block','vertical-align': 'center'}
    # ),


      html.Div([
     modal_overlay, 
     ],style={'height': '100', 'width':'50', 'display': 'inline-block','vertical-align': 'center'}
    ),
       
   

    # html.Div([
    #     html.H1('Positive ')], 
    #         style={'textAlign': 'left',
    #                 'margin': '6px', 'color' : colors['text'],
    #                 'marginLeft': '1%', 
    #                 'marginRight': '25%',
    #                 'marginTop': '0%',
    #                 'fontFamily': 'system-ui' }
    # ),
                   
    html.Div([
        
    button_howto, 
    ], style={'textAlign': 'right', 'margin': '6px',   'marginTop': '2%', 'marginBottom': '1%', 'padding-left':'61%','display': 'inline-block'}
    ),

                 
     ]),
html.Div([
    dcc.Tabs(id='tabs', value='tab-1', 
        # vertical=True,    
        children=[
            dcc.Tab(label='Home', value='tab-1', children=[content_tab_1], style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Merchant Value', value='tab-4', children= [content_tab_3], style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Merchant - Merchant relationship', value='tab-3',   children = [content_tab_4],style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Location based analysis', value='tab-2', children = [content_tab_2], style=tab_style, selected_style=tab_selected_style),

            # dcc.Tab(label='Reward history', value='tab-4'),
            # dcc.Tab(label='Rewards', value='tab-4'),
    ]),
    html.Div(id='tabs-example-content'),
], style= {'width': '75%', 'height':'50%','display': 'inline-block'}),

html.Div([

html.Br(),
html.Label(id='category-label', children = 'Select Segment'),

html.Div([
  
        dcc.Dropdown(
            id='category',
            options=[{'label':name, 'value':name} for name in names],
            value = list(fnameDict.keys())[0]
            ),
    html.Div(id='category-container'),
         
    ], style={'width': '100%'}), 

# html.Br(),
# html.Label(id='segment-label', children = 'Select segment'),

# html.Div([
#         dcc.Dropdown(
#             id='segment',
#             ),
#             ],style={'width': '100%', 'display': 'inline-block'}
#         ),
html.Br(),
html.Br(),
html.Label(id='time-label', children = 'Select one'),
html.Div([
dcc.RadioItems(
    id='duration',
    options=[
        {'label': 'Daily', 'value': 'daily'},
        {'label': 'Weekly', 'value': 'weekly'}
    ],
    value='daily'
) ,
],style={'width': '30%', 'display': 'inline-block'}),

html.Label(id='issued_reedm', children = 'Select one'),
html.Br(),

html.Div([
dcc.RadioItems(
    id='reedm_issued',
    options=[
        {'label': 'All', 'value': 'all'},
        {'label': 'Issued', 'value': 'issued'},
        {'label': 'Redeemed', 'value': 'redeemed'}
    ],
    value='all'
) ,
],style={'width': '39.5%', 'display': 'inline-block'}),

    html.Hr(),
    html.Div(id='display-selected-values'),



], style={'height': '110%', 'width': '18%', 'background-color': '#F5F4F3', 'float': 'left',  'marginLeft': '2%'}),



])

def get_edges(row):
    '''
    This function gets the edges of the graph from the csv file
    '''
    df_list = []
    to_line_list = str(row['merchant'])
    for i in to_line_list:
        if i == 'nan' or i == '-':
            continue
        else:
            df_list.append((str(row['CustomerId']), str(i)))
    return df_list

def interactive(graph):
    
    pos=nx.get_node_attributes(graph,'pos')
    # set node positions
    pos = nx.spring_layout(graph)
#         pos = graphviz_layout(G, prog='circo')
    for node in graph.nodes():
        graph.nodes[node]['pos']= list(pos[node])

    pos=nx.get_node_attributes(graph,'pos')
    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d

    p = nx.single_source_shortest_path_length(graph, ncenter)
    
    
#     print(etext)
    node_labels = list(graph.nodes)
    

    
    def make_edge(x, y, text, width):
        index = 0
        return  go.Scatter(x = x,
                           y = y,
                           line = dict(width = 2.75
#                                        color = colors[index]
                                      ),
#                            marker=dict(color=colors[index]),
                           hoverinfo = 'text',
                           text = ([text]),
                           mode = 'lines')
    
    
        index = index + 1



#     # For each edge, make an edge_trace, append to list
    edge_trace = []
    for edge in graph.edges():

        if graph.edges()[edge]['Frequency'] > 0:
            char_1 = edge[0]
            char_2 = edge[1]

            x0, y0 = pos[char_1]
            x1, y1 = pos[char_2]

            text   = char_1 + '--' + char_2 + ': ' + str(graph.edges()[edge]['Frequency'])

            trace  = make_edge([x0, x1, None], [y0, y1, None], text,
                               0.1*graph.edges()[edge]['Frequency']**1.75)

            edge_trace.append(trace)
        

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=node_labels,
#         hovertext = labels,
        mode='markers + text ',
        hoverinfo='text',
        textfont=dict(
        family="sans serif",
#         size=17,
        color="#06D5FA",
#         line={'width': 10},
            
    ),
        
        marker=dict(
            showscale=False,
            
            colorscale='Rainbow',
            reversescale=False,
#             color=[color_map],
            size=30,
            colorbar=dict(
                thickness=15,
                title='',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=30))
    )
    for node in graph.nodes():
        x, y = graph.nodes[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(graph.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of relations: '+str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies 
    node_trace.hovertext= node_text

    layout = go.Layout(
        title='Merchnat with Merchant relationship',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=1100,
        height=1100
    )


    fig = go.Figure(layout = layout)

    for trace in edge_trace:
        fig.add_trace(trace)

    fig.add_trace(node_trace)

    fig.update_layout(showlegend = False)

    fig.update_xaxes(showticklabels = False)

    fig.update_yaxes(showticklabels = False)

    return fig


# Callback for modal popup
@app.callback(
    Output("modal", "is_open"),
    [Input("howto-open", "n_clicks"), 
    Input("howto-close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open): 
    if n1 or n2:
        return not is_open
    return is_open

# Enable disable 

@app.callback(
    Output('category', 'style'),
    [Input('tabs', 'value')]
)

def enable_or_disable_cat(selected_tab):

    if selected_tab == 'tab-2':
        return {'display': 'none', 'width':'90%'}
    if selected_tab == 'tab-3':
        return {'display': 'none', 'width':'90%'}
    if selected_tab == 'tab-4':
        return {'display': 'none', 'width':'90%'}
    else:
        return {'display': 'block', 'width':'90%'}


@app.callback(
    Output('category-label', 'style'),
    [Input('tabs', 'value')]
)

def enable_or_disable_cat_label(selected_tab):

    if selected_tab == 'tab-2':
        return {'display': 'none', 'width':'90%'}
    if selected_tab == 'tab-3':
        return {'display': 'none', 'width':'90%'}
    if selected_tab == 'tab-4':
        return {'display': 'none', 'width':'90%'}
    else:
        return {'display': 'block', 'width':'90%'}



@app.callback(
    Output('reedm_issued', 'style'),
    [Input('tabs', 'value')]
)

def enable_or_disable_segment(selected_tab):
    if selected_tab == 'tab-1':
        return {'display': 'none', 'width':'90%'}
    elif selected_tab == 'tab-2':
        return {'display': 'none', 'width':'90%'}
    elif selected_tab == 'tab-3':
        return {'display': 'none', 'width':'90%'}
    else:
        return {'display': 'block', 'width':'90%'}

@app.callback(
    Output('issued_reedm', 'style'),
    [Input('tabs', 'value')]
)
 
def enable_or_disable_segment_label(selected_tab):
    if selected_tab == 'tab-1':
        return {'display': 'none', 'width':'90%'}
    elif selected_tab == 'tab-2':
        return {'display': 'none', 'width':'90%'}
    elif selected_tab == 'tab-3':
        return {'display': 'none', 'width':'90%'}
    else:
        return {'display': 'block', 'width':'90%'}

@app.callback(
    Output('duration', 'style'),
    [Input('tabs', 'value')]
)

def enable_or_disable_duration(selected_tab):
    if selected_tab == 'tab-2':
        return {'display': 'none', 'width':'90%'}
    elif selected_tab == 'tab-3':
        return {'display': 'none', 'width':'90%'}
    elif selected_tab == 'tab-4':
         
        return {'display': 'none', 'width':'90%'}
    else:
        return {'display': 'block', 'width':'90%'}


@app.callback(
    Output('time-label', 'style'),
    [Input('tabs', 'value')]
)

def enable_or_disable_duration_label(selected_tab):
    if selected_tab == 'tab-2':
        return {'display': 'none', 'width':'90%'}
    if selected_tab == 'tab-3':
        return {'display': 'none', 'width':'90%'}
    if selected_tab == 'tab-4':
        return {'display': 'none', 'width':'90%'}
    else:
        return {'display': 'block', 'width':'90%'}


# @app.callback(
#     dash.dependencies.Output('segment', 'options'),
#     [dash.dependencies.Input('category', 'value')]
# )
# def update_date_dropdown(name):
#     return [{'label': i, 'value': i} for i in fnameDict[name]]

# @app.callback(Output('tabs-example-content', 'children'),
#               Input('segment', 'value'))

# def set_display_children(selected_value):
#     if (selected_value == 'Fuel'):
#         return 'you have selected Fuel option'

@app.callback(
    dash.dependencies.Output('total_mile', 'figure'),
    [dash.dependencies.Input('category', 'value'),
    dash.dependencies.Input('duration', 'value')]
)

def total_miles(cat, dur):
    if ((cat == 'Overall') & (dur == 'daily')):
        #Redeemed
        df['TTime'] = pd.to_datetime(df['TTime'])
        plot_miles_R = df.loc[(df['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('D', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()

        #Issued
        df['TTime'] = pd.to_datetime(df['TTime'])
        plot_miles_I = df.loc[(df['TType'] == 'I') ,['TTime','miles']]
        df_miles_D_I = plot_miles_I.resample('D', on='TTime').sum()
        df_miles_D_I = df_miles_D_I.reset_index()

        fig = go.Figure()
        fig = make_subplots(rows=3, cols=2,
                    column_widths=[0.9, 0.1],
                    specs=[[{'rowspan': 3}, {'type': 'indicator'}],   # first row
                           [None,           {'type': 'indicator'}],   # second row
                           [None,           {'type': 'indicator'}]])  # third row

        fig.add_trace(go.Scatter(
            x=df_miles_D_I['TTime'],
            y=df_miles_D_I['miles'],
            name='Issued',
        ))

        fig.add_trace(go.Scatter(
            x=df_miles_D_R['TTime'],
            y=df_miles_D_R['miles'],
            name='Redeemed Transaction',
        ))
        fig.add_trace(go.Indicator(mode='number+delta',
                                value=8000000,
                                delta={'reference': 7500000,
                                        'valueformat': '.0f',
                                        'increasing': {'color': 'green'},
                                        'decreasing': {'color': 'gray'}},
                                title={'text': 'Total mile'},
                                domain={'y': [0, 1], 'x': [0.25, 0.75]}),
                    row=1, col=2)
        fig.update_layout(  
            plot_bgcolor='rgba(0,0,0,0)',
            # title_text="Total miles",showlegend=True
            )
        return fig

    elif ((cat == 'Overall') & (dur == 'weekly')):
        #Redeemed
        df['TTime'] = pd.to_datetime(df['TTime'])
        plot_miles_R = df.loc[(df['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('w', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()

        #Issued
        df['TTime'] = pd.to_datetime(df['TTime'])
        plot_miles_I = df.loc[(df['TType'] == 'I') ,['TTime','miles']]
        df_miles_D_I = plot_miles_I.resample('w', on='TTime').sum()
        df_miles_D_I = df_miles_D_I.reset_index()


        fig = go.Figure()

        fig = make_subplots(rows=3, cols=2,
                    column_widths=[0.9, 0.1],
                    specs=[[{'rowspan': 3}, {'type': 'indicator'}],   # first row
                           [None,           {'type': 'indicator'}],   # second row
                           [None,           {'type': 'indicator'}]])  # third row

        fig.add_trace(go.Scatter(
            x=df_miles_D_I['TTime'],
            y=df_miles_D_I['miles'],
            name='Issued',
        ))

        fig.add_trace(go.Scatter(
            x=df_miles_D_R['TTime'],
            y=df_miles_D_R['miles'],
            name='Redeemed Trx',
        ))
        
        fig.add_trace(go.Indicator(mode='number+delta',
                                value=4000000,
                                delta={'reference': 20000,
                                        'valueformat': '.0f',
                                        'increasing': {'color': 'green'},
                                        'decreasing': {'color': 'gray'}},
                                title={'text': 'Total mile'},
                                domain={'y': [0, 1], 'x': [0.25, 0.75]}),
                    row=1, col=2)

        fig.update_layout(  
            plot_bgcolor='rgba(0,0,0,0)',
            # title_text="Total miles",showlegend=True
            )
        return fig

    elif((cat == 'Gas') & (dur == 'daily')):

        # gas_stations = df[df['Segment'] =='GAS STATIONS']
        df_gas['TTime'] = pd.to_datetime(df_gas['TTime'])
        df['TTime'] = pd.to_datetime(df_gas['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
        plot_miles_R = df_gas.loc[(df_gas['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('D', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()
        fig = px.line(df_miles_D_R, x = 'TTime', y='miles')
        return fig

    elif((cat == 'Gas') & (dur == 'weekly')):

        # gas_stations = df[df['Segment'] =='GAS STATIONS']
        df_gas['TTime'] = pd.to_datetime(df_gas['TTime'])
        df['TTime'] = pd.to_datetime(df_gas['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
        plot_miles_R = df_gas.loc[(df_gas['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('W', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()

        fig = px.line(df_miles_D_R, x = 'TTime', y='miles')
        
        fig.update_layout(
            title_text="Redeemed Transaction for Gas stations")
        return fig
        #Food
    elif((cat == 'Food') & (dur == 'daily')):
        df_food['TTime'] = pd.to_datetime(df_food['TTime'])
        df['TTime'] = pd.to_datetime(df_food['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
        plot_miles_R = df_food.loc[(df_food['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('D', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()
        fig = px.line(df_miles_D_R, x = 'TTime', y='miles')
        return fig
    elif((cat == 'Food') & (dur == 'weekly')):

        df_food['TTime'] = pd.to_datetime(df_food['TTime'])
        df['TTime'] = pd.to_datetime(df_food['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
        plot_miles_R = df_food.loc[(df_food['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('W', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()

        fig = px.line(df_miles_D_R, x = 'TTime', y='miles')
        
        fig.update_layout(
            title_text="Redeemed Transaction for Gas stations")
        return fig
        
        #Home
    elif((cat == 'Home') & (dur == 'daily')):
        df_home['TTime'] = pd.to_datetime(df_home['TTime'])
        df['TTime'] = pd.to_datetime(df_home['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
        plot_miles_R = df_home.loc[(df_home['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('D', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()
        fig = px.line(df_miles_D_R, x = 'TTime', y='miles')
        return fig
    elif((cat == 'Home') & (dur == 'weekly')):
        df_home['TTime'] = pd.to_datetime(df_home['TTime'])
        df['TTime'] = pd.to_datetime(df_home['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
        plot_miles_R = df_home.loc[(df_home['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('W', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()
        fig = px.line(df_miles_D_R, x = 'TTime', y='miles')      
        fig.update_layout(
            title_text="Redeemed Transaction for Gas stations")
        return fig

        #Clothing and beauty 
    elif((cat == 'Clothing and beauty') & (dur == 'daily')):
        df_clothing_beauty['TTime'] = pd.to_datetime(df_clothing_beauty['TTime'])
        df['TTime'] = pd.to_datetime(df_clothing_beauty['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
        plot_miles_R = df_clothing_beauty.loc[(df_clothing_beauty['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('D', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()
        fig = px.line(df_miles_D_R, x = 'TTime', y='miles')
        return fig
    elif((cat == 'Clothing and beauty') & (dur == 'weekly')):
        df_clothing_beauty['TTime'] = pd.to_datetime(df_clothing_beauty['TTime'])
        df['TTime'] = pd.to_datetime(df_clothing_beauty['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
        plot_miles_R = df_clothing_beauty.loc[(df_clothing_beauty['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('W', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()
        fig = px.line(df_miles_D_R, x = 'TTime', y='miles')      
        fig.update_layout(
            title_text="Redeemed Transaction for Gas stations")
        return fig

    #     #Store
    # elif((cat == 'Store') & (dur == 'daily')):
    #     df_store['TTime'] = pd.to_datetime(df_store['TTime'])
    #     df['TTime'] = pd.to_datetime(df_store['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
    #     plot_miles_R = df_store.loc[(df_store['TType'] == 'R') ,['TTime','miles']]
    #     df_miles_D_R = plot_miles_R.resample('D', on='TTime').sum()
    #     df_miles_D_R = df_miles_D_R.reset_index()
    #     fig = px.line(df_miles_D_R, x = 'TTime', y='miles')
    #     return fig
    # elif((cat == 'Store') & (dur == 'weekly')):
    #     df_store['TTime'] = pd.to_datetime(df_store['TTime'])
    #     df['TTime'] = pd.to_datetime(df_store['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
    #     plot_miles_R = df_store.loc[(df_store['TType'] == 'R') ,['TTime','miles']]
    #     df_miles_D_R = plot_miles_R.resample('W', on='TTime').sum()
    #     df_miles_D_R = df_miles_D_R.reset_index()
    #     fig = px.line(df_miles_D_R, x = 'TTime', y='miles')      
    #     fig.update_layout(
    #         title_text="Redeemed Transaction for Gas stations")
    #     return fig

        #Others
    elif((cat == 'Others') & (dur == 'daily')):
        df_others['TTime'] = pd.to_datetime(df_others['TTime'])
        df['TTime'] = pd.to_datetime(df_others['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
        plot_miles_R = df_others.loc[(df_others['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('D', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()
        fig = px.line(df_miles_D_R, x = 'TTime', y='miles')
        return fig
    elif((cat == 'Others') & (dur == 'weekly')):
        df_others['TTime'] = pd.to_datetime(df_others['TTime'])
        df['TTime'] = pd.to_datetime(df_others['TTime'], format="%y-%m-%d %H:%M:%S",  infer_datetime_format=True)
        plot_miles_R = df_others.loc[(df_others['TType'] == 'R') ,['TTime','miles']]
        df_miles_D_R = plot_miles_R.resample('W', on='TTime').sum()
        df_miles_D_R = df_miles_D_R.reset_index()
        fig = px.line(df_miles_D_R, x = 'TTime', y='miles')      
        fig.update_layout(
            title_text="Redeemed Transaction for Gas stations")
        return fig
  
 
    else:
        return {}

#Top customers
@app.callback(
    dash.dependencies.Output('top_customers', 'figure'),
    [dash.dependencies.Input('category', 'value')]
) 
def Top_customers(cat):

    if (cat == 'Overall'):
        top_merchants = df[['merchant', 'miles']]
        top_merchants = top_merchants.groupby(['merchant'], sort=True).agg(mile_sum = ('miles','sum'))
        top_merchants = top_merchants.reset_index() 
        top_merchants = top_merchants.sort_values('mile_sum', ascending=True)
        top_merchants = top_merchants.head(10)

        fig = go.Figure(go.Bar(
            x=top_merchants['mile_sum'],
            y=top_merchants['merchant'],
            marker_color='#34495E',
            orientation='h'))

        fig.update_layout(
            xaxis={'categoryorder':'category descending'},
            title=go.layout.Title(
            text="Top merchants based on their miles",
            xref="paper",
            x=0
        ),
            xaxis_tickangle=-45)
        return fig
 #Gas
    if (cat == 'Gas'):
        
        top_merchants = df_gas[['merchant', 'miles']]
        top_merchants = top_merchants.groupby(['merchant']).agg(mile_sum = ('miles','sum'))
        top_merchants = top_merchants.reset_index() 
        top_merchants = top_merchants.sort_values(by='mile_sum', ascending=True)
        top_merchants = top_merchants.head(10)

        fig = go.Figure(go.Bar(
            x=top_merchants['mile_sum'],
            y=top_merchants['merchant'],
            marker_color='#34495E',
            orientation='h'))

        fig.update_layout(
            xaxis={'categoryorder':'total descending'},
            title=go.layout.Title(
            text="Top gas merchants based on their miles",
            xref="paper",
            x=0
        ),
            xaxis_tickangle=-45)
        return fig       
 #Food
    if (cat == 'Food'):
        top_merchants = df_food[['merchant', 'miles']]
        top_merchants = top_merchants.groupby(['merchant']).agg(mile_sum = ('miles','sum'))
        top_merchants = top_merchants.reset_index() 
        top_merchants = top_merchants.sort_values(by='mile_sum', ascending=True)
        top_merchants = top_merchants.head(10)

        fig = go.Figure(go.Bar(
            x=top_merchants['mile_sum'],
            y=top_merchants['merchant'],
            marker_color='#34495E',
            orientation='h'))

        fig.update_layout(
            xaxis={'categoryorder':'total descending'},
            title=go.layout.Title(
            text="Top food category merchants based on their miles",
            xref="paper",
            x=0
        ),
            xaxis_tickangle=-45)
        return fig  
 #Food
    if (cat == 'Home'):
        top_merchants = df_home[['merchant', 'miles']]
        top_merchants = top_merchants.groupby(['merchant'], sort=False).agg(mile_sum = ('miles','sum'))
        top_merchants = top_merchants.reset_index() 
        top_merchants = top_merchants.sort_values(by='mile_sum', ascending=False)
        top_merchants = top_merchants.head(10)

        fig = go.Figure(go.Bar(
            x=top_merchants['mile_sum'],
            y=top_merchants['merchant'],
            marker_color='#34495E',
            orientation='h'))

        fig.update_layout(
            title=go.layout.Title(
            text="Top home category merchants based on their miles",
            xref="paper",
            x=0
        ),
            xaxis_tickangle=-45)
        return fig        
    else:
        return {}


#Top Segments
@app.callback(
    dash.dependencies.Output('top_segments', 'figure'),
    [dash.dependencies.Input('category', 'value')]
) 

def Top_segments(cat):

    if (cat == 'Overall'):
        top_segments = df[['Segment', 'miles']]
        top_segments.loc[top_segments['Segment'] =='CHOLESTEROL', 'Segment'] = 'FOOD'
        top_segments = top_segments.groupby(['Segment']).agg(mile_sum = ('miles','sum'))
        top_segments = top_segments.reset_index() 
        top_segments = top_segments.sort_values(by='mile_sum', ascending=True)
        top_segments = top_segments.head(10)
        fig = go.Figure(go.Bar(
                    x=top_segments['mile_sum'],
                    y=top_segments['Segment'],
                    marker_color='#34495E', 
                    orientation='h'))

        fig.update_layout(
            xaxis={'categoryorder':'total descending'},
            title=go.layout.Title(
            text="Top segments based on miles",
            xref="paper",
            x=0
        ),
            xaxis_tickangle=-45)
        return fig
        #Gas
    if (cat == 'Gas'):
        top_segments = df_gas[['Segment', 'miles']]
        top_segments = top_segments.groupby(['Segment'], sort=True).agg(mile_sum = ('miles','sum'))
        top_segments = top_segments.reset_index() 
        top_segments = top_segments.sort_values(by='mile_sum', ascending=True)
        top_segments = top_segments.head(10)
        fig = go.Figure(go.Bar(
                    x=top_segments['mile_sum'],
                    y=top_segments['Segment'],
                    marker_color='#34495E',
                    orientation='h'))

        fig.update_layout(
            xaxis={'categoryorder':'total descending'},
            title=go.layout.Title(
            text="Top gas segments based on miles",
            xref="paper",
            x=0
        ),
            xaxis_tickangle=-45)
        return fig 

    if (cat == 'Food'):
        top_segments = df_food[['Segment', 'miles']]
        top_segments = top_segments.groupby(['Segment'], sort=True).agg(mile_sum = ('miles','sum'))
        top_segments = top_segments.reset_index() 
        top_segments = top_segments.sort_values(by='mile_sum', ascending=True)
        top_segments = top_segments.head(10)
        fig = go.Figure(go.Bar(
                    x=top_segments['mile_sum'],
                    y=top_segments['Segment'],
                    marker_color='#34495E',
                    orientation='h'))

        fig.update_layout(
            xaxis={'categoryorder':'total descending'},
            title=go.layout.Title(
            text="Top food segments based on miles",
            xref="paper",
            x=0
        ),
            xaxis_tickangle=-45)
        return fig  

    if (cat == 'Home'):
        top_segments = df_home[['Segment', 'miles']]
        top_segments = top_segments.groupby(['Segment'], sort=True).agg(mile_sum = ('miles','sum'))
        top_segments = top_segments.reset_index() 
        top_segments = top_segments.sort_values(by='mile_sum', ascending=True)
        top_segments = top_segments.head(10)
        fig = go.Figure(go.Bar(
                    x=top_segments['mile_sum'],
                    y=top_segments['Segment'],
                    marker_color='#34495E',
                    orientation='h'))

        fig.update_layout(
            xaxis={'categoryorder':'total descending'},
            title=go.layout.Title(
            text="Top home segments based on miles",
            xref="paper",
            x=0
        ),
            xaxis_tickangle=-45)
        return fig         
    else:
        return {}

#new vs returning customers
@app.callback(
    dash.dependencies.Output('new_returning', 'figure'),
    [dash.dependencies.Input('category', 'value')]
) 
def new_returning_cus(cat):
    if (cat == 'Overall'):
        df_new_returning = list(df['CustomerId'].value_counts())
        df_new_returning = pd.DataFrame(df_new_returning, columns=['type'])
        df_new = df_new_returning[df_new_returning['type']==1]
        df_vistors = df_new_returning[df_new_returning['type']>1]
        df_new = len(df_new['type'])
        df_new = [df_new]
        df_vistors = len(df_vistors['type'])
        df_vistors = [df_vistors]
        new_returning = df_new + df_vistors
        new_returning = pd.DataFrame(new_returning, columns=['value'])
        new_returning = new_returning.T
        new_returning.rename(columns = {0: 'New customers'}, inplace = True)
        new_returning.rename(columns = {1: 'Returning customers'}, inplace = True)
        new =new_returning.T
        new = new.reset_index()

        new.rename(columns = {'index': 'Type'}, inplace = True)

        fig = px.pie(new, values='value', names='Type')

        fig.update_layout(
            title_text="Customer retention")
        return fig
#Gas  
    elif (cat == 'Gas'):
        df_new_returning = list(df_gas['CustomerId'].value_counts())
        df_new_returning = pd.DataFrame(df_new_returning, columns=['type'])
        df_new = df_new_returning[df_new_returning['type']==1]
        df_vistors = df_new_returning[df_new_returning['type']>1]
        df_new = len(df_new['type'])
        df_new = [df_new]
        df_vistors = len(df_vistors['type'])
        df_vistors = [df_vistors]
        new_returning = df_new + df_vistors
        new_returning = pd.DataFrame(new_returning, columns=['value'])
        new_returning = new_returning.T
        new_returning.rename(columns = {0: 'New customers'}, inplace = True)
        new_returning.rename(columns = {1: 'Returning customers'}, inplace = True)
        new =new_returning.T
        new = new.reset_index()
        new.rename(columns = {'index': 'Type'}, inplace = True)
        fig = px.pie(new, values='value', names='Type')
        fig.update_layout(
            title_text="Customer retention")
        return fig
#Food
    elif (cat == 'Food'):
        df_new_returning = list(df_food['CustomerId'].value_counts())
        df_new_returning = pd.DataFrame(df_new_returning, columns=['type'])
        df_new = df_new_returning[df_new_returning['type']==1]
        df_vistors = df_new_returning[df_new_returning['type']>1]
        df_new = len(df_new['type'])
        df_new = [df_new]
        df_vistors = len(df_vistors['type'])
        df_vistors = [df_vistors]
        new_returning = df_new + df_vistors
        new_returning = pd.DataFrame(new_returning, columns=['value'])
        new_returning = new_returning.T
        new_returning.rename(columns = {0: 'New customers'}, inplace = True)
        new_returning.rename(columns = {1: 'Returning customers'}, inplace = True)
        new =new_returning.T
        new = new.reset_index()
        new.rename(columns = {'index': 'Type'}, inplace = True)
        fig = px.pie(new, values='value', names='Type')
        fig.update_layout(
            title_text="Customer retention")
        return fig
#Home
    elif (cat == 'Home'):
        df_new_returning = list(df_home['CustomerId'].value_counts())
        df_new_returning = pd.DataFrame(df_new_returning, columns=['type'])
        df_new = df_new_returning[df_new_returning['type']==1]
        df_vistors = df_new_returning[df_new_returning['type']>1]
        df_new = len(df_new['type'])
        df_new = [df_new]
        df_vistors = len(df_vistors['type'])
        df_vistors = [df_vistors]
        new_returning = df_new + df_vistors
        new_returning = pd.DataFrame(new_returning, columns=['value'])
        new_returning = new_returning.T
        new_returning.rename(columns = {0: 'New customers'}, inplace = True)
        new_returning.rename(columns = {1: 'Returning customers'}, inplace = True)
        new =new_returning.T
        new = new.reset_index()
        new.rename(columns = {'index': 'Type'}, inplace = True)
        fig = px.pie(new, values='value', names='Type')
        fig.update_layout(
            title_text="Customer retention")
        return fig

#Clothing and beauty
    elif (cat == 'Clothing and beauty'):
        df_new_returning = list(df_clothing_beauty['CustomerId'].value_counts())
        df_new_returning = pd.DataFrame(df_new_returning, columns=['type'])
        df_new = df_new_returning[df_new_returning['type']==1]
        df_vistors = df_new_returning[df_new_returning['type']>1]
        df_new = len(df_new['type'])
        df_new = [df_new]
        df_vistors = len(df_vistors['type'])
        df_vistors = [df_vistors]
        new_returning = df_new + df_vistors
        new_returning = pd.DataFrame(new_returning, columns=['value'])
        new_returning = new_returning.T
        new_returning.rename(columns = {0: 'New customers'}, inplace = True)
        new_returning.rename(columns = {1: 'Returning customers'}, inplace = True)
        new =new_returning.T
        new = new.reset_index()
        new.rename(columns = {'index': 'Type'}, inplace = True)
        fig = px.pie(new, values='value', names='Type')
        fig.update_layout(
            title_text="Customer retention")
        return fig

#Store
    elif (cat == 'Store'):
        df_new_returning = list(df_store['CustomerId'].value_counts())
        df_new_returning = pd.DataFrame(df_new_returning, columns=['type'])
        df_new = df_new_returning[df_new_returning['type']==1]
        df_vistors = df_new_returning[df_new_returning['type']>1]
        df_new = len(df_new['type'])
        df_new = [df_new]
        df_vistors = len(df_vistors['type'])
        df_vistors = [df_vistors]
        new_returning = df_new + df_vistors
        new_returning = pd.DataFrame(new_returning, columns=['value'])
        new_returning = new_returning.T
        new_returning.rename(columns = {0: 'New customers'}, inplace = True)
        new_returning.rename(columns = {1: 'Returning customers'}, inplace = True)
        new =new_returning.T
        new = new.reset_index()
        new.rename(columns = {'index': 'Type'}, inplace = True)
        fig = px.pie(new, values='value', names='Type')
        fig.update_layout(
            title_text="Customer retention")
        return fig

#Others
    elif (cat == 'Others'):
        df_new_returning = list(df_others['CustomerId'].value_counts())
        df_new_returning = pd.DataFrame(df_new_returning, columns=['type'])
        df_new = df_new_returning[df_new_returning['type']==1]
        df_vistors = df_new_returning[df_new_returning['type']>1]
        df_new = len(df_new['type'])
        df_new = [df_new]
        df_vistors = len(df_vistors['type'])
        df_vistors = [df_vistors]
        new_returning = df_new + df_vistors
        new_returning = pd.DataFrame(new_returning, columns=['value'])
        new_returning = new_returning.T
        new_returning.rename(columns = {0: 'New customers'}, inplace = True)
        new_returning.rename(columns = {1: 'Returning customers'}, inplace = True)
        new =new_returning.T
        new = new.reset_index()
        new.rename(columns = {'index': 'Type'}, inplace = True)
        fig = px.pie(new, values='value', names='Type')
        fig.update_layout(
            title_text="Customer retention")
        return fig

    else:
        return {}

# share_wallet

@app.callback(
    dash.dependencies.Output('share_wallet', 'figure'),
    [dash.dependencies.Input('category', 'value')]
)

def share_wallet1 (cat):
    if (cat == 'Overall'):
        data = {'Merchant':  ['Merchant 1', 'Merchant 10', 'Merchant 3', 'Merchant 24', 'Merchant 6', 'Merchant 16',
                    'Merchant 30'],
            'Share of wallet': ['84%', '82%', '74%', '93%','97%', '94%','98%']}

        df_wallet = pd.DataFrame (data, columns = ['Merchant','Share of wallet'])
        df_wallet.sort_values(by=['Share of wallet'], inplace=True, ascending=True)

        fig = go.Figure(data=[go.Bar(
                y=df_wallet['Merchant'], 
                x=df_wallet['Share of wallet'],
    
                textposition='auto',
                marker_color='#34495E',
                orientation = 'h'
            )])

        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            title=go.layout.Title(
            text="Top merchants in share of wallet ",
            xref="paper",
            x=0
        ),
        xaxis_tickangle=-45)
        return fig
        #Gas
    if (cat == 'Gas'):

        data = {'Gas stations':  ['Merchant 1','Merchant 20','Merchant 16'],
            'Share of wallet': ['80.3%', '32.12%', '11.25%']}

        df_wallet = pd.DataFrame (data, columns = ['Gas stations','Share of wallet'])
        df_wallet.sort_values(by=['Share of wallet'], inplace=True, ascending=True)

        fig = go.Figure(data=[go.Bar(
                y=df_wallet['Gas stations'], 
                x=df_wallet['Share of wallet'],

                textposition='auto',
                marker_color='#34495E',
                orientation = 'h'
            )])
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            # xaxis={'categoryorder':'total ascending'},
            
            title=go.layout.Title(
            text="Top gas stations in share of wallet ",
            xref="paper",
            x=0
        ),
        xaxis_tickangle=-45)
        return fig

        #Food  
    if (cat == 'Food'):
        data = {'Foods':  ['Merchant 18','Merchant 35','Merchant 26','Merchant 7', 'Merchant 19', 'Merchant 30','Merchant 17'],
            'Share of wallet': ['61.35%', '11.85%', '12.3%', '12.83%', '12.3%', '12.3%','11.8%']}

        df_wallet = pd.DataFrame (data, columns = ['Foods','Share of wallet'])

        fig = go.Figure(data=[go.Bar(
                y=df_wallet['Foods'], 
                x=df_wallet['Share of wallet'],

                textposition='auto',
                marker_color='#34495E',
                orientation = 'h'
            )])
        fig.update_layout(
            yaxis={'categoryorder':'total descending'},
            # xaxis={'categoryorder':'total ascending'},
            
            title=go.layout.Title(
            text="Top food categories based share of wallet ",
            xref="paper",
            x=0
        ),
        xaxis_tickangle=-45)
        return fig
# Home
    if (cat == 'Home'):
        data = {'Home':  ['HOME APPLIANCE','HOME SUPPLIES'],
            'Share of wallet': ['34.4%', '76.86%']}

        df_wallet = pd.DataFrame (data, columns = ['Home','Share of wallet'])
        

        fig = go.Figure(data=[go.Bar(
                x=df_wallet['Home'], 
                y=df_wallet['Share of wallet'],
    
                textposition='auto',
                marker_color='#34495E'
            )]) 

        fig.update_layout(
            yaxis={'categoryorder':'total descending'},
            title=go.layout.Title(
            text="Top Home categories in share of wallet ",
            xref="paper",
            x=0
        ),
        xaxis_tickangle=-45)
        return fig    
    else:
        return {}

# Data table

@app.callback(
    dash.dependencies.Output('datatable', 'data'),
    [dash.dependencies.Input('reedm_issued', 'value')]
) 
def show_table(value):
    if (value == 'all'):
        return m_valuable_all1.to_dict('records')

    elif(value == 'issued'):
        return df_issued.to_dict('records')

    elif(value == 'redeemed'):
        return df_redeemed.to_dict('records')
      

# @app.callback(
#     Output('datatable', 'style_data_conditional'),
#     Input('datatable', 'selected_columns')
# )
# def update_styles(selected_columns):
#     return [{
#         'if': { 'column_id': i },
#         'background_color': '#D2F3FF'
#     } for i in selected_columns]

@app.callback(
    dash.dependencies.Output('map-loc', 'figure'),
    [dash.dependencies.Input('category', 'value')]
)    
 
def location(cat):

    if (cat == 'Overall'):
        fig = go.Figure(go.Scattermapbox(
                lat=df['latitude'],
                lon=df['longitude'],
                mode='markers',
                
                
                marker=go.scattermapbox.Marker(
                    size=14,
                    color=df['miles'],
                ),
                text=df['merchant'],
            ))
  
        fig.update_layout(
            title='Showing segments based on locations',
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=12.174607, 
                    lon=-68.890511
                ),
                pitch=3,
                zoom=9.5
            )
        )

        return fig
    else:
        return {}

@app.callback(
    dash.dependencies.Output('returning_customers', 'figure'),
    [dash.dependencies.Input('category', 'value')]
)
def customer_dist  (value):
    if (value == 'Overall'):

        fig = px.histogram(df, x="merchant",   title="Customer distribution for each merchant")
        fig.update_traces(marker_color='#34495E')

        fig.update_layout(
            
            height=600, width=1000,
        )
        return fig
    else:
        return {}
        

@app.callback(
    dash.dependencies.Output('issued_reedemed', 'figure'), 
    [Input('reedm_issued', 'value'),
    Input('date_range_picker', 'start_date'),
	Input('date_range_picker', 'end_date'),
    Input('dropdownpicker', 'value')]) 
def draw_issued(value, start_date, end_date, dropdownpicker):
    if (value == 'all'):     
        if ((start_date is not None) | (end_date is not None)):
            new_df = df_filtered[(df_filtered['merchant'].isin(dropdownpicker))]
            df_date = new_df.loc[(new_df['date'] > start_date) & (new_df['date'] <= end_date)]

            df_date['date'] = pd.to_datetime(df_date['date'])
            df_date = df_date.groupby(['date', 'merchant']).sum()[["miles"]]
            df_date = df_date.reset_index()
            fig = px.line(df_date, x="date", y="miles", color = 'merchant')

            fig.update_layout(
                    height=800,
                    title_text='Merchant value by redeemed and issued miles'
                )
            return fig

        else:
            return {}

    elif (value == 'issued'):
        if ((start_date is not None) | (end_date is not None)):
            new_df = df_filtered[(df_filtered['merchant'].isin(dropdownpicker))]
            df_date = new_df.loc[(new_df['date'] > start_date) & (new_df['date'] <= end_date)]

            df_date['date'] = pd.to_datetime(df_date['date'])
            df_date = df_date.groupby(['date', 'merchant']).sum()[["miles"]]
            df_date = df_date.reset_index()
            fig = px.line(df_date, x="date", y="miles", color = 'merchant')

            fig.update_layout(
                    height=800,
                    title_text='Merchant value by redeemed and issued miles'
                )
            return fig
        else:
            return {}
    elif (value == 'redeemed'):
        if ((start_date is not None) | (end_date is not None)):
            new_df = df_filtered[(df_filtered['merchant'].isin(dropdownpicker))]
            df_date = new_df.loc[(new_df['date'] > start_date) & (new_df['date'] <= end_date)]

            df_date['date'] = pd.to_datetime(df_date['date'])
            df_date = df_date.groupby(['date', 'merchant']).sum()[["miles"]]
            df_date = df_date.reset_index()
            fig = px.line(df_date, x="date", y="miles", color = 'merchant')

            # fig.update_traces(textposition='top center')

            fig.update_layout(
                    height=800,
                    title_text='Merchant value by redeemed and issued miles'
                )
            return fig
        else:
            return {}
                    
    else:
        return {}

@app.callback(
    Output('pickertable', 'data'),
    Input('date_picker', 'date'))
def update_output(date_value):

    if date_value is not None:
        date_object = dt.fromisoformat(date_value)
        date_string = date_object.strftime('%m/%d/%Y')
        
        df_date= df2[df2['Date']== date_string]
        df_date['merchant'] = df_date['merchant'].str.strip('(,)').str.split(',')
        df_date = df_date.explode('merchant')
        # df_date['Frequency'] = df_date['merchant'].map(df_date['merchant'].value_counts())
        df_date = df_date[df_date['CustomerId'].map(df_date['CustomerId'].value_counts() > 1)]
        
        df_date = df_date.groupby('CustomerId').merchant.agg([('count', 'count'), ('merchant', ', '.join)])
        df_date = df_date.groupby(['merchant']).size().reset_index().rename(columns={0:'Frequency'})
        df_date = df_date.reset_index()
        df_date = df_date.sort_values(by = ('Frequency'), ascending = False)
        df_date2 = df_date[['merchant', 'Frequency']]

        return df_date2.to_dict('records') 
        
#  picker_graph 1

@app.callback(
    Output('picker_graph', 'figure'),
    Input('date_picker', 'date'))

def draw_date_picker(date_value):

    if date_value is not None:
        date_object = dt.fromisoformat(date_value)
        date_string = date_object.strftime('%m/%d/%Y')
        
        df_date= df2[df2['Date']== date_string]
        df_date['merchant'] = df_date['merchant'].str.strip('(,)').str.split(',')
        df_date = df_date.explode('merchant')
        # df_date['Frequency'] = df_date['merchant'].map(df_date['merchant'].value_counts())
        df_date = df_date[df_date['CustomerId'].map(df_date['CustomerId'].value_counts() > 1)]
        df_date = df_date.reset_index()
        # df_date = df_date.head(10)

        fig = px.histogram(df_date, x= "merchant",   title="Customer distribution for each merchant")
        fig.update_traces(marker_color='#34495E')

        fig.update_layout(

            # yaxis={'categoryorder':'category asscending'},
            
            height=600, width=1000,
        )
        return fig

#  picker_graph 2

@app.callback(
    Output('pickertable2', 'data'),
    Input('date_picker', 'date'))
def picker_tables2(date_value):

    if date_value is not None:
        date_object = dt.fromisoformat(date_value)
        date_string = date_object.strftime('%m/%d/%Y')
        
        df_date= df2[df2['Date']== date_string]
        df_date['merchant'] = df_date['merchant'].str.strip('(,)').str.split(',')
        df_date = df_date.explode('merchant')
        # df_date['Frequency'] = df_date['merchant'].map(df_date['merchant'].value_counts())
        df_date = df_date[df_date['CustomerId'].map(df_date['CustomerId'].value_counts() > 1)]
        
        df_date = df_date.groupby('CustomerId').merchant.agg([('count', 'count'), ('merchant', ', '.join)])
        df_date = df_date.groupby(['merchant']).size().reset_index().rename(columns={0:'Frequency'})
        df_date = df_date.reset_index()
        df_date2 = df_date[['merchant', 'Frequency']]
        df_date2 = df_date2.merchant.str.split(',',expand=True).stack().value_counts()
        rslt = pd.DataFrame(df_date2)
        rslt =rslt.reset_index()
        rslt.columns = ['merchant', 'Frequency']
        a, b = 0, 1
        x, y = rslt.Frequency.min(), rslt.Frequency.max()
        rslt['Frequency'] = (rslt.Frequency - x) / (y - x) * (b - a) + a
        rslt = round(rslt, 2)
        return rslt.to_dict('records') 

    else:
        return {}

@app.callback(
    Output('network_graph', 'figure'),
    Input('month_dropdown', 'value'))

def draw_network(month):
    if (month == '1'):
        df_1 = select_month(1)
        G1 = nx.from_pandas_edgelist(df=df_1, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G1)

    elif (month == '2'):
        df_2 = select_month(2)
        G2 = nx.from_pandas_edgelist(df=df_2, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G2)

    elif (month == '3'):
        df_3 = select_month(3)
        G3 = nx.from_pandas_edgelist(df=df_3, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G3)
    elif (month == '4'):
        df_4 = select_month(4)
        G4 = nx.from_pandas_edgelist(df=df_4, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G4)

    elif (month == '5'):
        df_5 = select_month(5)
        G5 = nx.from_pandas_edgelist(df=df_5, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G5)

    elif (month == '6'):
        df_6 = select_month(6)
        G6 = nx.from_pandas_edgelist(df=df_6, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G6)

    elif (month == '7'):
        df_7 = select_month(7)
        G7 = nx.from_pandas_edgelist(df=df_7, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G7)  

    elif (month == '8'):
        df_8 = select_month(8)
        G8 = nx.from_pandas_edgelist(df = df_8, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G8)  

    elif (month == '9'):
        df_9 = select_month(9)
        G9 = nx.from_pandas_edgelist(df = df_9, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G9)
    elif (month == '10'):
        df_10 = select_month(10)
        G10 = nx.from_pandas_edgelist(df = df_10, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G10)

    elif (month == '11'):
        df_11 = select_month(11)
        G11= nx.from_pandas_edgelist(df = df_11, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G11)

    elif (month == '12'):
        df_12 = select_month(12)
        G12 = nx.from_pandas_edgelist(df = df_12, source='Node1', target='Node2', edge_attr='Frequency')
        return interactive(G12)
              
    else:
        return {}

if __name__ == '__main__':
    app.run_server(debug= True)