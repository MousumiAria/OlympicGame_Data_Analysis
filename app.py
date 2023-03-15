import streamlit as st 
import pandas as pd
import numpy as np
import Preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

athlete=pd.read_csv("athlete_events.csv")
noc=pd.read_csv("noc_regions.csv")

df=Preprocessor.preprocess(athlete,noc)

st.sidebar.title('Olympics Analysis')
#st.sidebar.image('https://statathlon.com/wp-content/uploads/2018/01/rio-de-janeiro-2016-summer-olympics-e1467812135773.png')
st.sidebar.image('https://miro.medium.com/max/1400/1*tQRqA2N3Rn8OspbT2wUN-w.png')
user_menu=st.sidebar.radio(
    'Select an Option',
('Medal Tally','Overall Analysis','Contry-wise Analysis','Athlete wise Analysis')
)

if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox('Select Year',years)
    selected_country=st.sidebar.selectbox('Select Country',country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=="Overall" and selected_country=="Overall":
        st.title('Overall Tally')
    if selected_year!="Overall" and selected_country=="Overall":
        st.title('Medal Tally in'  +  str(selected_year)  + 'Olympics')
    if selected_year=="Overall" and selected_country != "Overall":
        st.title(selected_country + "overall performance")
    if selected_year!="Overall" and selected_country!="Overall":
        st.title(selected_country + 'performance in' + str(selected_year) + 'Olympics')
    st.table(medal_tally)

    
if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nation_over_time=helper.Data_over_time(df,'region')
    fig=px.line(nation_over_time,x='Edition',y='region')
    st.title("Participeting Nations over the years")
    st.plotly_chart(fig)

    events_over_time=helper.Data_over_time(df,'Event')
    fig=px.line(events_over_time,x='Edition',y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time=helper.Data_over_time(df,'Name')
    fig=px.line(athletes_over_time,x='Edition',y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title('No. of Events over time(Every Sport)')
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index="Sport",columns="Year",values="Event",aggfunc="count").fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='Contry-wise Analysis':
    st.sidebar.title('Contry-wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select a country',country_list)
    country_df=helper.year_wise_medal_tally(df,selected_country)
    fig=px.line(country_df,x='Year',y='Medal')
    st.title(selected_country+" Medal tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country+" excel in the following sports")
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)
    
    st.title('Top 10 athletes of' + selected_country)
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu=='Athlete wise Analysis':  
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x=[]
    name=[]
    Sport_list=['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
       'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
       'Cricket', 'Ice Hockey']
    for sport in Sport_list:
        temp_df=athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig=ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age  wrt sports(Gold medalist)')
    st.plotly_chart(fig)

    st.title('Height vs Weight')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select a Sport',sport_list)
    temp_df=helper.weight_v_height(df,selected_sport) 
    fig,ax=plt.subplots()   
    ax=sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)                        

    st.title("Men vs Women participation Over the Years")
    final=helper.men_vs_women(df)     
    fig=px.line(final,x='Year',y=['Men','Women'])   
    st.plotly_chart(fig)                    
    
                                                
                               
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                
                                                