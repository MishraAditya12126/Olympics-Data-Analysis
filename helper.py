import numpy as np
import pandas as pd

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    medal_tally = medal_tally.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

def fetch_medal_tally(df,year,country):
  medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
  temp_df = None
  flag = 0
  if year == 'Overall' and country =='Overall':
    temp_df = medal_df
  if year =='Overall' and country !='Overall':
    temp_df = medal_df[medal_df['region']==country]
    flag = 1
  if year !='Overall' and country =='Overall':
    temp_df = medal_df[medal_df['Year']==year]
  if year !='Overall' and country !='Overall':
    temp_df = medal_df[(medal_df['Year']==year) & (medal_df['region']==country)]

  if flag:
    x = temp_df.groupby('Year')[['Gold','Silver','Bronze']].sum().sort_values('Year',ascending=True).reset_index()
  else:
    x = temp_df.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()
  x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

  return x

def data_over_time(df,col):
    nations_over_year = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_year.rename(columns={'index': 'Edition', 'Year': f'No of {col}'}, inplace=True)
    return nations_over_year


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates(subset=['index'])
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count',fill_value=0)
    return pt

def most_successful_athletes_country_wise(df,country):
  temp_df = df.dropna(subset=['Medal'])
  temp_df = temp_df[temp_df['region']==country]

  x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates(subset=['index'])
  x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
  return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    temp_df=athlete_df
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    return temp_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0,inplace=True)

    return final
