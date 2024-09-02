import pandas as pd
import numpy as np


def medal_tally(df):
    medal=(df.groupby('region').sum()[['Gold','Silver','Bronze']]).sort_values(by='Gold',ascending=False).reset_index()
    medal.index+=1
    medal['Total']=medal['Gold']+medal['Silver']+medal['Bronze']
    return medal
def fetch_year_country(df):
    year=np.unique(df.Year.sort_values()).tolist()
    year.insert(0,'Overall')
    country=df.region.dropna().unique().tolist()
    country.sort()
    country.insert(0,'Overall')
    return year,country

def slice_data_country_year_basis(df,medal,year,country):
    if year=='Overall' and  country=='Overall':
        return medal,'Overall Tally'
    if year=='Overall' and country!='Overall':
        k = df[df['region'] == country]
        tally=k.groupby(k['Year']).sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
        tally['Total']=tally['Gold']+tally['Silver'] + tally['Bronze']
        tally.index+=1
        return tally,country+' Overall Performance'
    if year!='Overall' and country=='Overall':
        return medal_tally(df[df['Year']==year]),'Medal Tally in '+str(year)+' Olympics'
    if year!='Overall' and country!='Overall':
        c = df[df['Year'] == year]
        return medal_tally(c[c['region'] == country]),'Total Medals won by '+country+' in '+str(year)+' Olympics'
def participation_graph(df):
    participation_over_time = df[['Year', 'region']].drop_duplicates()['Year'].value_counts().reset_index().sort_values(
        by='Year')
    return participation_over_time
def Events_over_time(df):
    Events_over_time = df[['Year', 'Event']].drop_duplicates()['Year'].value_counts().reset_index().sort_values(
        by='Year')
    Events_over_time.rename(columns={'Year': 'Year', 'count': 'Number of Events'}, inplace=True)
    return Events_over_time
def fetch_sport(df):
    sport = sorted(df['Sport'].unique())
    sport.insert(0, 'Overall')
    return sport
def get_top_15_sports(df):
    temp=df.dropna(subset=['Medal'])
    temp=temp[['Name','Sport','region','Medal']]['Name'].value_counts().reset_index()
    temp=temp.rename(columns={'Name':'Name','count':'Medals won'})
    temp=temp.head(15).merge(df,on='Name',how='left')[['Name','Sport','region','Medals won']].drop_duplicates().reset_index(drop=True)
    temp.index+=1

    return temp
def fetch_country(df):
    country = df.region.dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')
    return country
def fetch_medal_tally_country_wise(df,country):
    temp_df=df.dropna(subset=['Medal'])
    if country=='Overall':
        temp_df=temp_df
    else:
        temp_df=temp_df[temp_df['region']==country]
    temp_df=temp_df.groupby('Year').count()['Medal'].reset_index()
    return temp_df
def fetch_dataset(df,selected_country):
    if selected_country != 'Overall':
        temp = df[df['region'] == selected_country]
    else:
        temp = df
    return temp

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df