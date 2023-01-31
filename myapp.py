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
dbc.Row([dbc.Col([dbc.Card([dbc.CardImg(src="data:image/jpeg;base64,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",top=True,bottom=False),
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
        fig1=go.FigureWidget()
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
        fig2=go.FigureWidget()
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
        fig3=go.FigureWidget()
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
                df['date']=pd.to_datetime(df['date'], format='%Y-%m-%d')
                date=df['date'].dt.strftime('%Y-%m-%d')
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
    
    
