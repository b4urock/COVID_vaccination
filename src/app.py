# Imports
import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from IPython.display import HTML
from matplotlib.dates import DateFormatter
from datetime import datetime
from datetime import timedelta

import urllib.request
import io
from PIL import Image
import base64

import plotly.offline as pyo
import plotly.graph_objs as go 
from plotly.subplots import make_subplots    

@st.cache(allow_output_mutation=True)
def load_data(path):
    data  = pd.read_csv(path,
                        encoding = 'utf-8', 
                        parse_dates=['date'],
                        sep = ',')
    return data

# Função para plotar painel de Casos de COVID-19, óbitos por COVID-19
# e Percentual de Isolamento.

# Função para plotar painel de Casos de COVID-19, óbitos por COVID-19
# e Percentual de Isolamento.

def COVID_Cases_per_million(dfCountry1: pd.DataFrame, 
                            dfCountry2: pd.DataFrame,
                            cTitleCountry1: str,
                            cTitleCountry2: str,
                            titulo: str):
  #-----------------------------------------------------------#
  # dfCountry1: Country 1 DataFrame                           #
  # dfCountry2: Country 2 DataFrame                           #
  # cTitleCountry1: selected country1                         #
  # cTitleCountry1: selected country2                         #
  # titulo: Graph Title                                       #
  # Returns: Ploted Graph                                     #
  #-----------------------------------------------------------#

  fig = make_subplots(rows=3, 
                      cols=2, 
                      vertical_spacing=0.12,
                      horizontal_spacing=0.08,
                      specs=[[{"type": "scatter"}, {"type": "scatter"}],
                             [{"type": "scatter"}, {"type": "scatter"}],                          
                             [{"type": "table"}, {"type": "table"}]],
                      subplot_titles=(f"<b>Daily cases per million in {cTitleCountry1}</b>",
                                      f"<b>Daily cases per million in {cTitleCountry2}</b>",
                                      f"<b>Testing and Vaccination Evolution per million in {cTitleCountry1}</b>",     
                                      f"<b>Testing and Vaccination Evolution per million in {cTitleCountry2}</b>",
                                      f"<b>Demographics of {cTitleCountry1}</b>",
                                      f"<b>Demographics of {cTitleCountry2}</b>"))
                                              
  fig.add_trace(
      go.Scatter(x=dfCountry1['date'], 
                y=dfCountry1['new_cases_per_million'],
                marker=dict(
                            color='blue',
                            size=120
          ),
      name=f"Daily cases per million in {cTitleCountry1}",
      hovertemplate=
        f"<b>{cTitleCountry1}'s new cases per million</b><br><br>" +
        "Date: %{x}<br>" +
        "New cases per million: %{y:,.}<br>" +
        "<extra></extra>"),
      row=1, col=1
  )

  fig.add_trace(
    go.Scatter(
    x=dfCountry1['date'],
    y=dfCountry1['new_cases_per_million_rollmean7'],
    mode='lines',
        marker=dict(
            color='Red',
            size=120,
            line=dict(
                color='Red',
                width=20
            )),
    name=f"{cTitleCountry1}'s 7 day rolling mean",
    hovertemplate=
        f"<b>{cTitleCountry1}'s 7 day rolling mean</b><br><br>" +
        "Date: %{x}<br>" +
        "New cases: %{y:,.}<br>" +
        "<extra></extra>"),
    row=1, col=1)

  fig.add_trace(
      go.Scatter(x=dfCountry2['date'], 
                y=dfCountry2['new_cases_per_million'],
                marker=dict(
                            color='goldenrod',
                            size=120,
          ), 
      name=f"Daily Cases in {cTitleCountry2}",
      hovertemplate=
        f"<b>{cTitleCountry2}'s new cases per million </b><br><br>" +
        "Date: %{x}<br>" +
        "New cases per million: %{y:,.}<br>" +
        "<extra></extra>"),   
      row=1, col=2
  )

  fig.add_trace(
      go.Scatter(
      x=dfCountry2['date'],
      y=dfCountry2['new_cases_per_million_rollmean7'],
      mode='lines',
          marker=dict(
              color='Red',
              size=120,
              line=dict(
                  color='Red',
                  width=20
              )),
      name=f"{cTitleCountry2}'s 7 day rolling mean",
      hovertemplate=
        f"<b>{cTitleCountry2}'s 7 day rolling mean</b><br><br>" +
        "Date: %{x}<br>" +
        "New cases per million: %{y:,.}<br>" +
        "<extra></extra>",
      showlegend=False),
      row=1, col=2)
    
  fig.add_trace(
      go.Scatter(x=dfCountry1['date'], 
                y=dfCountry1['people_fully_vaccinated_per_million'],
                marker=dict(color='darkorchid',
                            size=160,
                            line=dict(
                            color='darkorchid',
                            width=40)), 
      name="People Fully Vaccinated per Million",
      hovertemplate=
        f"<b>{cTitleCountry1}'s fully vaccinated per million</b><br><br>" +
        "Date: %{x}<br>" +
        "Vaccinated per million: %{y:,.}<br>" +
        "<extra></extra>"),   
      row=2, col=1
  )
  
  fig.add_trace(
      go.Scatter(x=dfCountry1['date'], 
                y=dfCountry1['total_tests_per_million'],
                marker=dict(
                            color='Green',
                            size=180,
                            line=dict(
                            color='Green',
                            width=40)),
      name="People Tested per Million", 
      hovertemplate=
        f"<b>{cTitleCountry1}'s tested per million</b><br><br>" +
        "Date: %{x}<br>" +
        "Tested per million: %{y:,.}<br>" +
        "<extra></extra>"),
      row=2, col=1
  )
  fig.add_trace(
      go.Scatter(
      x=dfCountry2['date'],
      y=dfCountry2['people_fully_vaccinated_per_million'],
      mode='lines',
          marker=dict(
              color='darkorchid',
              size=160,
              line=dict(
                  color='darkorchid',
                  width=40
              )),
      name='People Fully Vaccinated per Million"',
      hovertemplate=
        f"<b>{cTitleCountry2}'s fully vaccinated per million</b><br><br>" +
        "Date: %{x}<br>" +
        "Vaccinated per million: %{y:,.}<br>" +
        "<extra></extra>",
      showlegend=False),
      row=2, col=2)

  fig.add_trace(
      go.Scatter(
      x=dfCountry2['date'],
      y=dfCountry2['total_tests_per_million'],
      mode='lines',
          marker=dict(
              color='Green',
              size=160,
              line=dict(
                  color='Green',
                  width=40
              )),
      name='Tested per Million',
      hovertemplate=
        f"<b>{cTitleCountry2}'s tested per million</b><br><br>" +
        "Date: %{x}<br>" +
        "Tested per million: %{y:,.}<br>" +
        "<extra></extra>",
      showlegend=False),
      row=2, col=2)   

  # Table Calculations for the first country
  today = pd.to_datetime('today')
  last_month = today - pd.DateOffset(months=1)
  last_month_cases1 = dfCountry1.loc[dfCountry1['date'] < last_month, 'new_cases'].sum()
  this_month_cases1 = dfCountry1.loc[dfCountry1['date'] >= last_month, 'new_cases'].sum()
  Population1             = dfCountry1['population'].max()
  Perc_Fully_Vaccinated1  = dfCountry1['people_fully_vaccinated_perc'].max()#round((dfCountry1['people_fully_vaccinated'].max()/ 
                           # dfCountry1['population'].max())*100,2)
  try:                            
    Vaccination_Start_Date1 = dfCountry1.loc[~dfCountry1['new_vaccinations'].isnull()].iloc[0]['date']
  except:
    Vaccination_Start_Date1 = '-'

  Cases_Total1            = int(dfCountry1['total_cases'].max())
  Deaths_Total1           = int(dfCountry1['total_deaths'].max())
  Mortality_Rate1         = round(dfCountry1['new_deaths'].sum()/dfCountry1['new_cases'].sum()*100,2)
  Growth_Rate1            = round(abs(1+(this_month_cases1-last_month_cases1)/last_month_cases1)*100,2)
  cells1 = []
  cells1.append(round((Population1/1000000),1))
  cells1.append(f'{Perc_Fully_Vaccinated1}%')

  if Vaccination_Start_Date1 == '-':
    cells1.append(Vaccination_Start_Date1)
  else:
    cells1.append(Vaccination_Start_Date1.strftime("%m/%d/%y"))

  cells1.append("{:,}".format(Cases_Total1))
  cells1.append("{:,}".format(Deaths_Total1))
  cells1.append(f'{Mortality_Rate1}%')
  cells1.append(f'{Growth_Rate1}%')      

  fig.add_trace(
      go.Table(
          header=dict(
              values=["<b>Population (Millions)</b>", "<b>Perc. of Population fully vaccineted</b>","<b>Vaccination started on (MM/DD/YY)</b>", "<b>Cases Total</b>", "<b>Deaths Total</b>", "<b>Mortality Rate</b>", "<b>Last Month Growth Rate</b>"],
              font=dict(size=12),
              align="center"
          ),
          cells=dict(
              values=cells1,
              font=dict(size=12),              
              align = "center")
      ),
      row=3, col=1
  )          

  # Table Calculations for the second country
  today = pd.to_datetime('today')
  last_month = today - pd.DateOffset(months=1)
  last_month_cases2 = dfCountry2.loc[dfCountry2['date'] < last_month, 'new_cases'].sum()
  this_month_cases2 = dfCountry2.loc[dfCountry2['date'] >= last_month, 'new_cases'].sum()
  Population2             = dfCountry2['population'].max()
  Perc_Fully_Vaccinated2  = round((dfCountry2['people_fully_vaccinated'].max()/ 
                            dfCountry2['population'].max())*100,2)
  try:                            
    Vaccination_Start_Date2 = dfCountry2.loc[~dfCountry2['new_vaccinations'].isnull()].iloc[0]['date']
  except:
    Vaccination_Start_Date2 = None

  Cases_Total2            = int(dfCountry2['total_cases'].max())
  Deaths_Total2           = int(dfCountry2['total_deaths'].max())
  Mortality_Rate2         = round(dfCountry2['new_deaths'].sum()/dfCountry2['new_cases'].sum()*100,2)
  Growth_Rate2            = round(abs(1+(this_month_cases2-last_month_cases2)/last_month_cases2)*100,2)
  cells2 = []
  cells2.append(round((Population2/1000000),1))
  cells2.append(f'{Perc_Fully_Vaccinated2}%')

  if Vaccination_Start_Date2 is None:
    cells2.append('-')
  else:
    cells2.append(Vaccination_Start_Date2.strftime("%m/%d/%y"))

  cells2.append("{:,}".format(Cases_Total2))
  cells2.append("{:,}".format(Deaths_Total2))
  cells2.append(f'{Mortality_Rate2}%')
  cells2.append(f'{Growth_Rate2}%')

  fig.add_trace(
      go.Table(
          header=dict(
              values=["<b>Population (Millions)</b>", "<b>Perc of Population fully vaccineted</b>","<b>Vaccination Started on (MM/DD/YY)</b>", "<b>Cases Total</b>", "<b>Deaths Total</b>", "<b>Mortality Rate</b>", "<b>Last Month Growth Rate</b>"],
              font=dict(size=12),
              align="center"
          ),
          cells=dict(
              values=cells2,
              font=dict(size=12),
              align = "center")
      ),
      row=3, col=2
  ) 

  data_date = dfCountry1.date.max().strftime("%m/%d/%Y")
  plot1 = ''
  plot2 = ''

  if dfCountry1['total_tests_per_million'].isnull().values.sum():
     plot1 = f'** Not all test data avaiable for {cTitleCountry1}'
  elif dfCountry2['total_tests_per_million'].isnull().values.sum():
     plot2 = f'** Not all test data avaiable for {cTitleCountry2}'

  fig.update_layout(
      template = 'plotly_dark',
      title = { 'text': f'{titulo}<br>**Interative Graph**',
                'font': dict(size=20),
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
      showlegend=False,        
      yaxis = {  'categoryorder': 'total descending'},
      yaxis3 = { 'categoryorder': 'total descending'},              
      autosize=False,
      width=1280,
      height=900,     
      margin=dict(
          l=50,
          r=50,
          b=10,
          t=110,
          pad=2
      )
  )

  fig.add_annotation(text=f'Source: https://ourworldindata.org/ <br> * Data available until: {data_date} <br> {plot1} <br> {plot2}',
                  xref="paper", yref="paper",
                  x=0.9999, y=0.001, showarrow=False)

  if not plot1 is None: 
    fig.add_annotation(text=f'<b>{plot1}</b>',
                    xref="paper", yref="paper",
                    x=0.03, y=0.33, showarrow=False)                        

  if not plot2 is None: 
    fig.add_annotation(text=f'<b>{plot2}</b>',
                    xref="paper", yref="paper",
                    x=0.77, y=0.33, showarrow=False)    

  fig.update_layout( hoverlabel_font_color='white')                    

  # Removing the Grid
  
  fig.update_xaxes(showgrid=False)
  fig.update_yaxes(showgrid=False)                    
                            
  return fig

# Função para plotar painel de Casos de COVID-19, óbitos por COVID-19
# e Percentual de Isolamento.

# Função para plotar painel de Casos de COVID-19, óbitos por COVID-19
# e Percentual de Isolamento.

def COVID_deaths (dfCountry1: pd.DataFrame, 
                  dfCountry2: pd.DataFrame,
                  cTitleCountry1: str,
                  cTitleCountry2: str,
                  titulo: str):
  #-----------------------------------------------------------#
  # dfCountry1: Country 1 DataFrame                           #
  # dfCountry2: Country 2 DataFrame                           #
  # cTitleCountry1: selected country1                         #
  # cTitleCountry1: selected country2                         #
  # titulo: Graph Title                                       #
  # Returns: Ploted Graph                                     #
  #-----------------------------------------------------------#

  fig = make_subplots(rows=3, 
                      cols=2, 
                      vertical_spacing=0.12,
                      horizontal_spacing=0.08,
                      specs=[[{"type": "scatter"}, {"type": "scatter"}],
                             [{"type": "scatter"}, {"type": "scatter"}],                          
                             [{"type": "table"}, {"type": "table"}]],
                      subplot_titles=(f"<b>Daily death count in {cTitleCountry1}</b>",
                                      f"<b>Daily death count in {cTitleCountry2}</b>",
                                      f"<b>Testing and Vaccination Evolution per million in {cTitleCountry1}</b>",     
                                      f"<b>Testing and Vaccination Evolution per million in {cTitleCountry2}</b>",
                                      f"<b>Demographics of {cTitleCountry1}</b>",
                                      f"<b>Demographics of {cTitleCountry2}</b>"))
                                              
  fig.add_trace(
      go.Scatter(x=dfCountry1['date'], 
                y=dfCountry1['new_deaths'],
                marker=dict(
                            color='blue',
                            size=120
          ),
      name=f"Daily death count in {cTitleCountry1}",
      hovertemplate=
        f"<b>{cTitleCountry1}'s daily death count </b><br><br>" +
        "Date: %{x}<br>" +
        "Daily death count: %{y:,.}<br>" +
        "<extra></extra>"),
      row=1, col=1
  )

  fig.add_trace(
    go.Scatter(
    x=dfCountry1['date'],
    y=dfCountry1['new_deaths_rollmean7'],
    mode='lines',
        marker=dict(
            color='Red',
            size=120,
            line=dict(
                color='Red',
                width=20
            )),
    name=f"{cTitleCountry1}'s 7 day rolling mean",
    hovertemplate=
        f"<b>{cTitleCountry1}'s 7 day rolling mean</b><br><br>" +
        "Date: %{x}<br>" +
        "Daily death count: %{y:,.}<br>" +
        "<extra></extra>"),
    row=1, col=1)

  fig.add_trace(
      go.Scatter(x=dfCountry2['date'], 
                y=dfCountry2['new_deaths'],
                marker=dict(
                            color='goldenrod',
                            size=120,
          ), 
      name=f"Daily death count in {cTitleCountry2}",
      hovertemplate=
        f"<b>{cTitleCountry2}'s daily death count</b><br><br>" +
        "Date: %{x}<br>" +
        "Daily death count: %{y:,.}<br>" +
        "<extra></extra>"),      
      row=1, col=2
  )

  fig.add_trace(
      go.Scatter(
      x=dfCountry2['date'],
      y=dfCountry2['new_deaths_rollmean7'],
      mode='lines',
          marker=dict(
              color='Red',
              size=120,
              line=dict(
                  color='Red',
                  width=20
              )),
      name=f"{cTitleCountry2}'s 7 day rolling mean",
      hovertemplate=
        f"<b>{cTitleCountry2}'s 7 day rolling mean</b><br><br>" +
        "Date: %{x}<br>" +
        "Daily death count: %{y:,.}<br>" +
        "<extra></extra>",
      showlegend=False),
      row=1, col=2)
    
  fig.add_trace(
      go.Scatter(x=dfCountry1['date'], 
                y=dfCountry1['people_fully_vaccinated_per_million'],
                marker=dict(color='darkorchid',
                            size=160,
                            line=dict(
                            color='darkorchid',
                            width=40)), 
      name="People Fully Vaccinated per Million",
      hovertemplate=
        f"<b>{cTitleCountry1}'s fully vaccinated per million</b><br><br>" +
        "Date: %{x}<br>" +
        "Vaccinated per million: %{y:,.}<br>" +
        "<extra></extra>"),   
      row=2, col=1
  )

  fig.add_trace(
      go.Scatter(x=dfCountry1['date'], 
                y=dfCountry1['total_tests_per_million'],
                marker=dict(
                            color='Green',
                            size=180,
                            line=dict(
                            color='Green',
                            width=40)),
      name="People Tested per Million", 
      hovertemplate=
        f"<b>{cTitleCountry1}'s tested per million</b><br><br>" +
        "Date: %{x}<br>" +
        "Tested per million: %{y:,.}<br>" +
        "<extra></extra>"),
      row=2, col=1
  )

  fig.add_trace(
      go.Scatter(
      x=dfCountry2['date'],
      y=dfCountry2['people_fully_vaccinated_per_million'],
      mode='lines',
          marker=dict(
              color='darkorchid',
              size=160,
              line=dict(
                  color='darkorchid',
                  width=40
              )),
      name='People Fully Vaccinated per Million"',
      hovertemplate=
        f"<b>{cTitleCountry2}'s fully vaccinated per million</b><br><br>" +
        "Date: %{x}<br>" +
        "Vaccinated per million: %{y:,.}<br>" +
        "<extra></extra>",
      showlegend=False),
      row=2, col=2)

  fig.add_trace(
      go.Scatter(
      x=dfCountry2['date'],
      y=dfCountry2['total_tests_per_million'],
      mode='lines',
          marker=dict(
              color='Green',
              size=160,
              line=dict(
                  color='Green',
                  width=40
              )),
      name='Tested per Million',
      hovertemplate=
        f"<b>{cTitleCountry2}'s tested per million</b><br><br>" +
        "Date: %{x}<br>" +
        "Tested per million: %{y:,.}<br>" +
        "<extra></extra>",
      showlegend=False),
      row=2, col=2)  

  # Table Calculations for the first country
  today = pd.to_datetime('today')
  last_month = today - pd.DateOffset(months=1)

  last_month_death1 = dfCountry1.loc[dfCountry1['date'] < last_month, 'new_deaths'].sum()
  this_month_death1 = dfCountry1.loc[dfCountry1['date'] >= last_month, 'new_deaths'].sum()
  Population1             = dfCountry1['population'].max()
  Perc_Fully_Vaccinated1  = dfCountry1['people_fully_vaccinated_perc'].max()#round((dfCountry1['people_fully_vaccinated'].max()/ 
                           # dfCountry1['population'].max())*100,2)
  try:                          
    Vaccination_Start_Date1 = dfCountry1.loc[~dfCountry1['new_vaccinations'].isnull()].iloc[0]         ['date']
  except:
    Vaccination_Start_Date1 = '-'    

  cases_Total1            = int(dfCountry1['total_cases'].max())
  deaths_Total1           = int(dfCountry1['total_deaths'].max())
  Mortality_Rate1         = round(dfCountry1['new_deaths'].sum()/dfCountry1['new_cases'].sum()*100,2)
  Growth_Rate1            = round(abs(1+(this_month_death1-last_month_death1)/last_month_death1)*100,2)
  cells1 = []
  cells1.append(f'<b>{round((Population1/1000000),1)}</b>')
  cells1.append(f'<b>{Perc_Fully_Vaccinated1}%</b>')

  if Vaccination_Start_Date1 == '-':
    cells1.append(f'<b>{Vaccination_Start_Date1}</b>')
  else:
    cells1.append(f'<b>{Vaccination_Start_Date1.strftime("%m/%d/%y")}</b>')
  
  cases_formatted1 = "{:,}".format(cases_Total1)
  deaths_formatted1 = "{:,}".format(deaths_Total1)
  cells1.append(f'<b>{cases_formatted1}</b>')
  cells1.append(f'<b>{deaths_formatted1}</b>')
  cells1.append(f'<b>{Mortality_Rate1}%</b>')
  cells1.append(f'<b>{Growth_Rate1}%</b>')    

  fig.add_trace(
      go.Table(
          header=dict(
              values=["<b>Population (Millions)</b>", "<b>Perc. of Population fully vaccineted</b>","<b>Vaccination Started on (MM/DD/YY)</b>", "<b>Case Count Total</b>", "<b>Death Count Total</b>", "<b>Mortality Rate</b>", "<b>Last Month Growth Rate</b>"],
              font=dict(size=12, color='white'),
              align="center"
          ),
          cells=dict(
              values=cells1,
              font=dict(size=12, color='white'),
              align = "center"),
      ),
      row=3, col=1
  )          

  # Table Calculations for the second country
  last_month_death2       = dfCountry2.loc[dfCountry2['date'] < last_month, 'new_deaths'].sum()
  this_month_death2       = dfCountry2.loc[dfCountry2['date'] >= last_month, 'new_deaths'].sum()
  Population2             = dfCountry2['population'].max()
  Perc_Fully_Vaccinated2  = round((dfCountry2['people_fully_vaccinated'].max()/ 
                            dfCountry2['population'].max())*100,2)
                            
  try:                          
    Vaccination_Start_Date2 = dfCountry2.loc[~dfCountry2['new_vaccinations'].isnull()].iloc[0]         ['date']
  except:
    Vaccination_Start_Date2 = '-'

  cases_Total2            = int(dfCountry2['total_cases'].max())
  deaths_Total2           = int(dfCountry2['total_deaths'].max())
  Mortality_Rate2         = round(dfCountry2['new_deaths'].sum()/dfCountry2['new_cases'].sum()*100,2)
  Growth_Rate2            = round(abs(1+(this_month_death2 - last_month_death2)/last_month_death2)*100,2)
  cells2 = []
  cells2.append(f'<b>{round((Population2/1000000),1)}</b>')
  cells2.append(f'<b>{Perc_Fully_Vaccinated2}%</b>')

  if Vaccination_Start_Date2 == '-':
    cells2.append(f'<b>{Vaccination_Start_Date2}</b>')
  else:
    cells2.append(f'<b>{Vaccination_Start_Date2.strftime("%m/%d/%y")}</b>')
  
  cases_formatted2 = "{:,}".format(cases_Total2)
  deaths_formatted2 = "{:,}".format(deaths_Total2)
  cells2.append(f'<b>{cases_formatted2}</b>')
  cells2.append(f'<b>{deaths_formatted2}</b>')
  cells2.append(f'<b>{Mortality_Rate2}%</b>')
  cells2.append(f'<b>{Growth_Rate2}%</b>')

  fig.add_trace(
      go.Table(
          header=dict(
              values=["<b>Population (Millions)</b>", "<b>Perc of Population Fully Vaccineted</b>","<b>Vaccination Started on (MM/DD/YY)</b>", "<b>Case Count Total</b>", "<b>Death Count Total</b>", "<b>Mortality Rate</b>", "<b>Last Month Growth Rate</b>"],
              font=dict(size=12, color='white'),
              align="center"
          ),

          cells=dict(
              values=cells2,
              font=dict(size=12, color='white'),              
              align = "center")
      ),
      row=3, col=2
  ) 

  data_date = dfCountry1.date.max().strftime("%m/%d/%Y")
  plot1 = ''
  plot2 = ''

  if dfCountry1['total_tests_per_million'].isnull().values.sum():
     plot1 = f'** Not all test data avaiable for {cTitleCountry1}'
  elif dfCountry2['total_tests_per_million'].isnull().values.sum():
     plot2 = f'** Not all test data avaiable for {cTitleCountry2}'

  fig.update_layout(
      template = 'plotly_dark',
      title = { 'text': f'{titulo}<br>**Interative Graph**',
                'font': dict(size=20),
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
      showlegend=False,        
      yaxis = {  'categoryorder': 'total descending'},
      yaxis3 = { 'categoryorder': 'total descending'},              
      autosize=False,
      width=1280,
      height=900,          
      margin=dict(
          l=50,
          r=50,
          b=10,
          t=110,
          pad=2
      )
  )

  fig.add_annotation(text=f'Source: https://ourworldindata.org/ <br> * Data available until: {data_date} <br> {plot1} <br> {plot2}',
                  xref="paper", yref="paper",
                  x=0.9999, y=0.001, showarrow=False)

  if not plot1 is None: 
    fig.add_annotation(text=f'<b>{plot1}</b>',
                    xref="paper", yref="paper",
                    x=0.03, y=0.33, showarrow=False)                        

  if not plot2 is None: 
    fig.add_annotation(text=f'<b>{plot2}</b>',
                    xref="paper", yref="paper",
                    x=0.77, y=0.33, showarrow=False)   

  fig.update_layout( hoverlabel_font_color='white')

  # Removing the Grid
  fig.update_xaxes(showgrid=False)
  fig.update_yaxes(showgrid=False)

  return fig

def main():
    url = 'https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv?raw=true'
    dfVaccination = load_data(url)    

    urlimg = "https://github.com/b4urock/COVID_vaccination/raw/main/assets/2019-nCoV-CDC-23312_without_background-pubic-domain.png"
    with urllib.request.urlopen(urlimg) as i:
	    byteImg = io.BytesIO(i.read())
	    img = Image.open(byteImg)

    # Creating support columns for the dataframe
    dfVaccination['new_cases_per_million_rollmean7'] = round(dfVaccination['new_cases_per_million'].rolling(7, center=True).mean(),2) # Rolling mean 7 days
    dfVaccination['new_deaths_rollmean7'] = round(dfVaccination['new_deaths'].rolling(7, center=True).mean(),2) # Rolling mean 7 days
    dfVaccination['total_tests_per_million'] = round((dfVaccination['total_tests']/dfVaccination['population'])*1000000,2)
    dfVaccination['people_fully_vaccinated_per_million'] = round((dfVaccination['people_fully_vaccinated']/dfVaccination['population'])*1000000,2)

    dfVaccination['people_fully_vaccinated_perc'] = round((dfVaccination['people_fully_vaccinated']/ dfVaccination['population'])*100,2)

    dfVaccination['new_vaccinations_per_million'] =  round((dfVaccination['new_vaccinations']/dfVaccination['population'])*1000000,2)

    # drop continents from data frame
    countries = ['South America', 'North America', 'World', 'Oceania','Europe', 'International', 'Africa', 'Asia', 'European Union']
    i = dfVaccination[dfVaccination.location.isin(countries)].index
    dfVaccination.drop(i, inplace=True)

    countries = dfVaccination.location.unique().tolist()
    graph_type = ['Cases Comparison', 'Deaths Comparison']

    st.title('COVID-19 Comparison Dashboard')
    st.markdown('app by Pablo Pereira')

    default_ix1 = countries.index('Brazil')
    default_ix2 = countries.index('United States')

    pGraphType = st.sidebar.selectbox('Graph type', graph_type, index=1)
    pCountry1 = st.sidebar.selectbox('First country', countries, index=default_ix1)
    pCountry2 = st.sidebar.selectbox('Second country', countries, index=default_ix2)

    # Creating the sliced dataframe to plot
    country1 = pd.DataFrame(dfVaccination.loc[dfVaccination.location==pCountry1])
    country2 = pd.DataFrame(dfVaccination.loc[dfVaccination.location==pCountry2])    

    # Adjusting the vaccination info is necessary
    if country1.people_fully_vaccinated_per_million.isnull().all():
        country1.people_fully_vaccinated_per_million = round(((country1['new_vaccinations'].cumsum()/2)/country1['population'])*1000000,2)
        country1['people_fully_vaccinated_perc']     = round(((country1['new_vaccinations'].cumsum()/2)/country1['population'])*100,2)

    if country2.people_fully_vaccinated_per_million.isnull().all():
        country2.people_fully_vaccinated_per_million =  round(((country2['new_vaccinations'].cumsum()/2)/country2['population'])*1000000,2)
        country2['people_fully_vaccinated_perc']     = round(((country2['new_vaccinations'].cumsum()/2)/country2['population'])*100,2)  

    if pGraphType == 'Deaths Comparison':
       figure = COVID_deaths(country1, 
                            country2,
                            pCountry1,
                            pCountry2,
                            'COVID-19 Country deaths comparison')

    elif pGraphType == 'Cases Comparison':
        figure = COVID_Cases_per_million(country1, 
                                        country2,
                                        pCountry1,
                                        pCountry2,
                                        'COVID-19 Country cases comparison')     
    
    st.plotly_chart(figure)    

if __name__ == '__main__':
  main()