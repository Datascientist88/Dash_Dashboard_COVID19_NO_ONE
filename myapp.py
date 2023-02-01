import pandas as pd
import numpy as np
import dash
from dash import html 
from dash import dcc
import plotly.graph_objects as go
from dash.dependencies import Input ,Output
import dash_bootstrap_components as dbc
import plotly_express as px
import requests

# read in the data -------------I used URL to get automically updated data from the data source ---------------------
url="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
df=pd.read_csv(url)
df=df.rename(columns={'iso_code':'Countrycode','location':'Country'})
df['date']=pd.to_datetime(df['date'])
df['Mortality Rate']=df['total_deaths']/df['total_cases']*100
df['Death Rate']=df['total_deaths']/df['population']*100
df_country=df.groupby(['Countrycode','Country']).sum().reset_index()
yesterdays_date=df['date'].max()
df['date']=pd.to_datetime(df['date'], format='%Y-%m-%d')
date=df['date'].dt.strftime('%Y-%m-%d')
# plot the Map :--------- this part is redundant ------------------
def world_map(df):
    fig = px.choropleth(df, locations="Countrycode", color = "total_cases",
                        hover_name= "Country",
                        hover_data = ['total_cases','new_cases','total_deaths'],
                        projection="orthographic",
                        color_continuous_scale=px.colors.sequential.OrRd_r)

    fig.update_layout(paper_bgcolor='#000000',geo=dict(bgcolor= '#000000'),
                       title=f"Cumulative Cases since the start of pandemic untill {yesterdays_date}")
    fig.layout.template='plotly_dark'

    return fig

#setting the app layout ----I used bootstrap components to make the application resposive to various screeen sizes------------
app=dash.Dash(external_stylesheets=[dbc.themes.CYBORG],meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server=app.server
app.layout=dbc.Container( [dbc.Row(dbc.Col(html.H2("COVID 19 DASHBOARD WITH REAL-TIME DATA ",className='text-center mb-4'),width=12)), dbc.Row( html.Marquee("Get Daily Updated News About Covid 19 From Bahgeel Dashboard"), style = {'color':'red'}),
dbc.Row([dbc.Col([dbc.Card([dbc.CardImg(src="https://media.tenor.com/NoO2NL5f5X8AAAAC/covid19-cell.gif",top=True,bottom=False),
dbc.CardBody([html.H4('COVID 19 DASHBOARD',className='card-title'),html.P('Choose The Country:',className='card-text'),
dcc.Dropdown(id='selection_drop',multi=False,value='World',
options=[{'label':x,'value':x} for x in sorted(df['Country'].unique())],clearable=False,style={"color": "#000000"})])],color="dark",inverse=True,outline=False)],width=2,xs=12, sm=12, md=12, lg=5, xl=2) ,
dbc.Col([ dcc.Graph(id='cumulative_fig',figure={})],xs=12, sm=12, md=12, lg=5, xl=5),                                                                                                                     
        dbc.Col([dcc.Graph(id='trajectory',figure={})], xs=12, sm=12, md=12, lg=5, xl=5),
         ]),
         html.Br(),
dbc.Row([dbc.Col([ dcc.Graph(id='indicator',figure={})],xs=4, sm=4, md=4, lg=2, xl=2),dbc.Col([dcc.Graph(id='mortality',figure={})], 
        xs=12, sm=12, md=12, lg=5, xl=5) ,dbc.Col([ dcc.RadioItems(id='selection',options=['Trajectory of Pandemic','Cumulative Cases'],value='Cumulative Cases') ,dcc.Loading(dcc.Graph(id='graph',figure={}),type='cube')],xs=12, sm=12, md=12, lg=5, xl=5)]),
],fluid=True)
# the call back Functions :---------------------- necessary to add interactivity to your dashboard -------------
@app.callback(
        Output('cumulative_fig','figure'),
        Input('selection_drop','value')
)
def update_graph(selected_country):
        filtered_df=df[df['Country']==selected_country]
        fig1=go.Figure()
        fig1.add_scatter(name=f'Total Cases in {selected_country}',x=filtered_df['date'],y=filtered_df['total_cases'] ,fill='tonexty' ,fillcolor='rgba(225,6,0,0.2)' ,line=dict(color='#e10600'))
        fig1.update_layout(title=f'Up to Date Covid 19 Cases in {selected_country} : Cumulative Figures',xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),hovermode='x unified',paper_bgcolor='#000000',
                        plot_bgcolor='#000000') 
        fig1.layout.template='plotly_dark'
        fig1.update_traces(mode="lines",hoverinfo='all')
        return fig1
@app.callback(
        Output('trajectory','figure'),
        Input('selection_drop','value')
)
def update_graph(selected_country):
        filtered_df=df[df['Country']==selected_country]
        fig2=go.Figure()
        fig2.add_scatter(name=f'New  Cases in {selected_country}',x=filtered_df['date'],y=filtered_df['new_cases'] ,fill='tonexty' ,fillcolor='rgb(225,6,0)' ,line=dict(color='#e10600'))
        fig2.update_xaxes(rangeslider_visible=False,rangeselector= dict(buttons=list([dict(count=7,label='1w',step="day",stepmode="backward"),
                                                                                dict(count=14,label='2w',step="day",stepmode="backward"),
                                                                                dict(count=1,label='1m',step="month",stepmode="backward"),
                                                                                dict(count=6,label='6m',step="month",stepmode="backward"),
                                                                                dict(count=12,label='12m',step="month",stepmode="backward"),
                                                                                dict(count=1,label='YTD',step="year",stepmode="todate"),
                                                                                dict(label="All",step="all")
                                                                                ]),activecolor='tomato')
                        )
        fig2.update_layout(title=f'The Trajectory of the Pandemic in {selected_country}',xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),hovermode='x unified' ,
                        paper_bgcolor='#000000',
                        plot_bgcolor='#000000',
                        xaxis_rangeselector_font_color='black',
                        xaxis_rangeselector_activecolor='red',
                        ) 
        fig2.layout.template='plotly_dark'
        return fig2
@app.callback(
        Output('mortality','figure'),
        Input('selection_drop','value')
)
def update_graph(selected_country):
        filtered_df=df[df['Country']==selected_country]
        fig3=go.Figure()
        fig3.add_scatter(name=f'Mortality Rate in {selected_country}',x=filtered_df['date'],y=filtered_df['Mortality Rate'],fill='tonexty' ,fillcolor='rgba(225,6,0,0.2)' ,line=dict(color='#e10600'))
        fig3.add_scatter(name=f'Death Rate in {selected_country}',x=filtered_df['date'],y=filtered_df['Death Rate'],line=dict(color='#FFFF00') )
        fig3.update_layout(title=f'Death Rate vs Mortalitly Rate in {selected_country}',xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),hovermode='x unified',paper_bgcolor='#000000',
                        plot_bgcolor='#000000') 
        fig3.layout.template='plotly_dark'
        fig3.update_traces(mode="lines",hoverinfo='all')
        return fig3
@app.callback(
        Output('indicator','figure'),
        Input('selection_drop','value')
)
def update_graph(selected_country):
        filtered_df=df[df['Country']==selected_country]
        value=filtered_df['new_cases'].replace('NaN',np.nan).fillna(0).iloc[-1]
        reference=filtered_df['new_cases'].replace('NaN',np.nan).fillna(0).iloc[-2]
        text=f"Changes in Cases in {selected_country}"
        fig5 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        title = {'text': text},
        delta = { 'reference':reference,'relative':True},
        gauge={'bar':{'color':'#e10600'}},
        domain = {'x': [0, 1], 'y': [0, 1]}
        
        ))
        fig5.update_layout(height=500 ,width=350, plot_bgcolor='#000000',paper_bgcolor='#000000')
        fig5.layout.template='plotly_dark'
        return fig5
@app.callback(
    Output("graph", "figure"), 
    Input("selection", "value"))
def display_animated_graph(selection):
        if selection=='Trajectory of Pandemic':
       
                df_country=df.groupby(['Countrycode','Country','date']).sum().reset_index()
                fig = px.choropleth(df_country, locations="Countrycode", color = "total_cases",
                                        hover_name= "Country",animation_frame=date,
                                        hover_data = df[['total_cases','new_cases','total_deaths']],
                                        color_continuous_scale=px.colors.sequential.Plasma)

                fig.update_layout(transition={'duration':1000},paper_bgcolor='#000000',geo=dict(bgcolor= '#000000'),margin=dict(l=0,r=0,t=0,b=0))
                fig.update_traces(marker_line_color='rgba(255,255,255,0)', selector=dict(type='choroplethmapbox'))
                fig.layout.template='plotly_dark'
        else:
                df_country=df.groupby(['Countrycode','Country']).sum().reset_index()
                yesterdays_date=df['date'].max()
                fig = px.choropleth(df_country, locations="Countrycode", color = "total_cases",
                                        hover_name= "Country",
                                        hover_data = ['total_cases','new_cases','total_deaths'],
                                        projection="orthographic",
                                        color_continuous_scale=px.colors.sequential.OrRd_r)
                fig.update_layout(paper_bgcolor='#000000',geo=dict(bgcolor= '#000000'),
                                title=f"Cumulative Cases since the start of pandemic untill {yesterdays_date}")
                fig.layout.template='plotly_dark'

        return fig
       
if __name__=='__main__':
    app.run_server(debug=True, port=8000)
    
    
