import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
df = pd.read_csv('athlete_event.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df) # preprocessed DataFrame
st.sidebar.title(':red[OLYMPICS] ANALYSIS')
st.sidebar.image('images/download.png')
user_menu = st.sidebar.radio('Select an option',('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis'))


if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select a year',years)
    selected_country = st.sidebar.selectbox('Select a country',country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title('Overall Tally 🥇🥈🥉')
    elif selected_country !='Overall' and selected_year == 'Overall':
        st.title(selected_country+': Overall performance 🥇🥈🥉')
    elif selected_country =='Overall' and selected_year != 'Overall':
        st.title('Medal Tally in '+str(selected_year)+' 🥇🥈🥉')
    elif selected_country !='Overall' and selected_year != 'Overall':
        st.title('Performance of '+selected_country+' in '+str(selected_year)+' 🥇🥈🥉')
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    st.title('Top statistics')
    st.image('images/img.png', width=100)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header(':blue[Editions]')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header(':red[Sports]')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("**:yellow[Events]**")
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('**:green[Athletes]**')
        st.title(athletes)

    nations_over_year = helper.data_over_time(df,'region')
    fig1 = px.line(nations_over_year,x='Edition',y=f'No of region')
    st.title('Participating nations over the years')
    st.plotly_chart(fig1)

    events_over_time = helper.data_over_time(df,'Event')
    fig2 = px.line(events_over_time,x='Edition',y='No of Event')
    st.title('Events over the years')
    st.plotly_chart(fig2)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig3 = px.line(athlete_over_time, x='Edition', y='No of Name')
    st.title('Athletes over the years')
    st.plotly_chart(fig3)

    st.title('No. of events over time(Every sport)')
    fig4,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Event','Sport'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count',fill_value=0),annot=True)
    st.pyplot(fig4)

    st.title('Most successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    countries = helper.country_year_list(df)[1][1:]
    selected_country = st.sidebar.selectbox('Select a country',countries)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    st.title(selected_country+' Medal Tally over the years'+'🏅')
    fig5 = px.line(country_df,x='Year',y='Medal')
    st.plotly_chart(fig5)

    st.title(selected_country + ' excels in the following sports 🏃🏻')
    pt = helper.country_event_heatmap(df,selected_country)
    fig6,ax2 = plt.subplots(figsize=(20,20))
    ax2 = sns.heatmap(pt,annot=True)
    st.pyplot(fig6)

    st.title('Top 10 Athletes of '+selected_country)
    top10_df = helper.most_successful_athletes_country_wise(df,selected_country)
    st.table(top10_df)


if user_menu=='Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig7 = ff.create_distplot([x1, x2, x3, x4],['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig7.update_layout(autosize=False,width=800,height=600)
    st.title("Distribution of Age 📈")
    st.plotly_chart(fig7)

    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Sport', 'Year'])
    famous_sports = temp_df['Sport'].value_counts().index[:40].tolist()

    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig8 = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig8.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age 📈 w.r.t sports (Gold Medalist) 🏅')
    st.plotly_chart(fig8)
    st.title('🧍Height vs Weight 🏋️‍♀️')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    selected_sport = st.selectbox('Select a sport', sport_list)


    temp_df = helper.weight_v_height(df,selected_sport)
    fig9,ax3 = plt.subplots(figsize=(10,10))
    ax3 = sns.scatterplot(data=temp_df,x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=100)
    st.pyplot(fig9)

    st.title('♂ Men vs Women ♀ Participation Over the Years')
    final = helper.men_vs_women(df)
    fig10 = px.line(final,x='Year',y=['Male','Female'])
    fig10.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig10)