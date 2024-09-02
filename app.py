import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import preprocessor,helper

df=pd.read_csv('athlete_events.csv')
noc_regions=pd.read_csv('noc_regions.csv')

k=preprocessor.process_with_11_player_teammatches_medals_issue(df,noc_regions)
df=preprocessor.preprocess(df,noc_regions)

st.sidebar.title('Olympic Analysis')
st.sidebar.image('https://th.bing.com/th/id/OIP.yd9qSz8riDZf_JjmFO0zSwHaEB?w=322&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7')


user_menu=st.sidebar.radio('Select an Option',
           ('Medal Tally','Overall analysis','Country-wise analysis','Athlete-wise Analysis')
           )
if user_menu=='Medal Tally':
    medal_tally = helper.medal_tally(df)
    # st.header('Medal Tally')

    year,country=helper.fetch_year_country(df)
    selected_year=st.sidebar.selectbox('Select Year',year)
    selected_country=st.sidebar.selectbox('Select Country',country)

    sliced,ti=helper.slice_data_country_year_basis(df,medal_tally,selected_year,selected_country)
    st.title(ti)
    st.table(sliced)
if user_menu=='Overall analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    players=k['Name'].unique().shape[0]
    games=df['Sport'].unique().shape[0]
    country=df['region'].unique().shape[0]
    events=df['Event'].unique().shape[0]

    c1,c2,c3=st.columns(3)
    with c1:
        st.subheader('Editions')
        st.title(editions)
    with c2:
        st.subheader('Hosts')
        st.title(cities)
    with c3:
        st.subheader('Players')
        st.title(players)
    c4,c5,c6=st.columns(3)
    with c4:
        st.subheader('Games')
        st.title(games)
    with c5:
        st.subheader('Countries')
        st.title(country)
    with c6:
        st.subheader('Events')
        st.title(events)
    participation=helper.participation_graph(df)
    st.title('Participation of nation over time')
    fig=px.line(participation, x='Year', y='count')
    st.plotly_chart(fig)


    Events_over_time=helper.Events_over_time(df)
    st.title('Events over time')
    figure=px.line(Events_over_time, x='Year',y='Number of Events')
    st.plotly_chart(figure)

    st.title('Number of each Events over Time')
    x = df[['Year', 'Sport', 'Event']].drop_duplicates()
    fig,ax=plt.subplots(figsize=(15,15))
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)

    sport=helper.fetch_sport(df)
    st.title('Most Successful Players')
    selected_sport=st.selectbox('Select a Sport',sport)

    if selected_sport=='Overall':
        top_15_athletes=helper.get_top_15_sports(k)
    if selected_sport!='Overall':
        top_15_athletes=helper.get_top_15_sports(k[k['Sport']==selected_sport])
        st.title('Top Players in '+selected_sport)
    st.table(top_15_athletes)

if user_menu=='Country-wise analysis':
    st.sidebar.title('Country wise analysis')
    country=helper.fetch_country(df)
    selected_country=st.sidebar.selectbox('Select a country',country)
    data=helper.fetch_medal_tally_country_wise(df,selected_country)
    # st.table(data)
    st.title(selected_country+' Medal Tally over the Years')
    fig=px.line(data,x='Year',y='Medal',markers=True)
    st.plotly_chart(fig)



    st.title(selected_country+' excels in following sports')
    temp=helper.fetch_dataset(df,selected_country)
    temp = temp.dropna(subset=['Medal'])
    x = temp.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    figg,ax=plt.subplots(figsize=(15, 15))
    ax=sns.heatmap(x, annot=True)

    st.pyplot(figg)

    st.title(selected_country+' top players')
    temp_team=helper.fetch_dataset(k,selected_country)
    st.table(helper.get_top_15_sports(temp_team))

if user_menu=='Athlete-wise Analysis':
    st.title('Age Distribution')
    a = k['Age'].dropna()
    b = k[k['Medal'] == 'Gold']['Age'].dropna()
    c = k[k.Medal == 'Silver']['Age'].dropna()
    d = k[k.Medal == 'Bronze']['Age'].dropna()



    fig = ff.create_distplot([a, b, c, d], ['Age Distribution', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,height=500,width=800)
    st.plotly_chart(fig)


    st.title('Age distribution of different sports')
    sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
              'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
              'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
              'Water Polo', 'Hockey', 'Rowing', 'Fencing',
              'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
              'Tennis', 'Golf', 'Softball', 'Archery',
              'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
              'Rhythmic Gymnastics', 'Rugby Sevens',
              'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    players_df = k.drop_duplicates(subset=['Name', 'region'])
    x = []
    name = []
    kk = ['Athletics', 'Volleyball', 'Wrestling']
    for i in sports:
        temp_df = players_df[players_df.Sport == i]
        x.append(temp_df[temp_df.Medal == 'Gold']['Age'].dropna())
        name.append(i)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight in different sports')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', data=temp_df, hue='Medal', style='Sex', s=40)

    st.pyplot(fig)

    men = k[k.Sex == 'M'].groupby('Year').count()['Name'].reset_index()
    women = k[k.Sex == 'F'].groupby('Year').count()['Name'].reset_index()
    participant = men.merge(women, on='Year', how='left')
    participant.rename(columns={'Year': 'Year', 'Name_x': 'M', 'Name_y': 'F'}, inplace=True)
    participant.fillna(0, inplace=True)
    fig = px.line(participant, x='Year', y=['M', 'F'])
    st.title('Men vs Women participation over the years')
    st.plotly_chart(fig)