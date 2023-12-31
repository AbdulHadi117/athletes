
#$ Import necessary libraries
import pandas as pd , streamlit as st
import plotly.express as px , plotly.graph_objects as go

#@ Read data from CSV files
df = pd.read_csv(f'Richest Athletes (Richest Athletes 1990-2021).csv')
dfo = pd.read_csv(f'Forbes Richest Athletes (Forbes Richest Athletes 1990-2021).csv')

#$ Configure Streamlit app settings
st.set_page_config(page_title='Dashboard',
                   page_icon='⚽',
                   layout='wide')

#! Create a sidebar
with st.sidebar:

    #@ Create title of sidebar
    st.title('HELLO THERE ! 👋')
    st.write('''
    - My name is Abdul Hadi. 
    - This is my Streamlit Web Application displaying the EDA i did on the dataset of FORBES RICHEST ATHLETES (1990-2021).
             ''')
    st.markdown('---')
    
    #@ Radio button for viewing data
    st.header('WOULD YOU LIKE TO VIEW THE DATASET')
    a = st.radio('Select :',['Yes','No'],index=1)
    if 'Yes' in a:
        st.subheader('FILTER AND VIEW DATASET')
        
        #$ Slider and Multiselect buttons
        year = st.select_slider('Select Year :',options=df['Year'].unique())
        sport = st.multiselect('Select Sport :',options=df['Sport'].unique(),default=df['Sport'].unique())
        
        #$ Filter data according to selection
        df_selection= df.query(
            'Year == @year & Sport == @sport'
        )
        st.dataframe(df_selection)
    st.markdown('---')

    #@ Selectbox for basic information
    st.header('WOULD YOU LIKE THE BASIC INFORMATION')
    b = st.selectbox('PICK',['OVERVIEW','DESCRIPTIVE','NONE'],index=2)   
    if 'OVERVIEW' in b:
            st.write('''                         
- **Dimensions**: 1659 rows x 5 columns
- **Columns**:
  1. **Name**: The names of the athletes (object data type, 535 unique values).
  2. **Nationality**: The nationalities of the athletes (object data type, 44 unique values).
  3. **Earnings**: The earnings of the athletes in millions of USD (FLoat data type, 477 unique values).
  4. **Year**: The year of data collection (Integer data type, 31 unique values).
  5. **Sport**: The sport in which the athletes excel (object data type, 15 unique values).
''')    
    elif 'DESCRIPTIVE' in b:
        col1,col2,col3 = st.columns([2,0.5,4])
        with col1:
             st.write(df.Earnings.describe())
        with col3:
             st.write('''
- **Count**: 1659
- **Mean**: $27.5 million USD
- **Standard Deviation**: $20.3 million USD
- **Minimum Earnings**: $3.8 million USD
- **Maximum Earnings**: $300 million USD
- **25% Percentile**: $17.75 million USD
- **50% Percentile**: $24 million USD
- **75% Percentile**: $32 million USD
- This gives a descriptive statistical approach to the dataset
''')         
    else :
         st.error("Please select an option")    
    
    st.markdown('---')

    #@ Purpose of dashboard and main questions
    st.markdown('''
- In this Dashboard, You can view different plots and charts that answer some general questions like
    1. Which Sports have the highest number of Athletes ?
    2. How the Earnings in different Sports have progressed throughout the years ?
    3. Which are the top 25 highest Earnings Athletes ?
    4. What is the distribution and frequency in Earnings of Athletes ?
    5. Is there a Positive or Negative Correlation between Earnings and Sports ?          
''')
    
#! Main dashboard title and information
st.title('***RICHEST ATHLETES 1990-2021*** 💸⚽')
st.header('CREATED BY :  **_ABDUL HADI_**')
st.markdown('---')

#! Create columns for displaying different plots and charts
col_1, col_2, col_3 = st.columns([1.2, 0.5, 3])

with col_1:
#$ Plot the pie chart for the top 8 sports with the most athletes    
    
    #@ Sort and modify data
    df_3 = df.sort_values(by='Earnings', ascending=False)
    df_3 = df_3.reset_index()
    df_3 = df_3.drop(columns='index')
    top = df_3.Sport.value_counts()
    sport = top.nlargest(8)
    sport = sport.to_dict()
    values = sport.values()
    names = sport.keys()

    #@ Plot the chart
    fig_pie = px.pie(values=sport, names=names, template='plotly_dark', width=500, height=650)
    fig_pie.update_traces(
        textposition='inside', textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=1))
    )
    fig_pie.update_layout(
        title_text='<b>TOP 8 SPORTS WITH MOST ATHLETES</b>',
        title_font_size=20
    )
    st.plotly_chart(fig_pie)

#$ Plot the bar chart for the top 25 highest paid athletes

    #@ Sort and modify data
    df_1=df.sort_values(by='Earnings',ascending=False)
    df_1 = df_1.reset_index()
    df_1 = df_1.drop(columns='index')
    df_1 = df_1.head(25)

    #@ Plot the chart
    fig_bar = px.bar(df_1,x='Name',y='Earnings',
                 hover_data=df_1,range_y=(0,250),color_discrete_sequence=['#0083B8'])
    fig_bar.update_layout(
            title="<b>TOP 25 HIGHEST PAID ATHLETES</b>",
            title_font_size = 20,
            xaxis_title='<b>NAME OF ATHLETES</b>',
            yaxis_title="<b>EARNINGS (MILLIONS USD)</b>",
            showlegend=False,width=750,height=500,plot_bgcolor='rgba(0,0,0,0)'
            ,yaxis=(dict(showgrid=False)))
    st.plotly_chart(fig_bar)

with col_3:

#$ Plot the area chart showing the growth in earnings for different sports
    
    #@ Filtee data for top sports
    df_basket = df.loc[df['Sport']=='Basketball']
    df_base = df.loc[df['Sport']=='Baseball']
    df_foot = df.loc[df['Sport']=='Football']
    df_ten = df.loc[df['Sport']=='Tennis']
    df_soc = df.loc[df['Sport']=='Soccer']
    df_rac = df.loc[df['Sport']=='Racing']
    df_golf = df.loc[df['Sport']=='Golf']
    df_box = df.loc[df['Sport']=='Boxing']
    df_2 = pd.concat([df_basket,df_base,df_foot,df_ten,df_soc,df_rac,df_golf,df_box],axis=0)
    
    #@ Sort and modify data 
    df_2 = df_2.sort_values(by='Earnings',ascending=False)
    df_2 = df_2.reset_index()
    df_2 = df_2.drop(columns='index')
    
    #@ Plot the chart
    fig_line = px.area(df_2,x='Year',y='Earnings',color='Sport',
                  facet_col='Sport',facet_col_wrap=4,range_y=(0,200),
                  markers=True,hover_data=df_2,template='plotly_dark')
    fig_line.update_layout(
        title='<b>GROWTH IN EARNINGS AND QUALITY OF ATHLETES</b>',
        width=1200,
        height=600,plot_bgcolor='rgba(0,0,0,0)'
    )
    fig_line.update_xaxes(
        tickvals=[1990,2005,2020]
    )
    st.plotly_chart(fig_line)

#! Create two columns for displaying histograms and scatter plots
    col_a, col_b = st.columns(2)

#$ Plot the histogram for the distribution of earnings
    with col_a:

        #@ Sort and modify data
        df_5 =df.sort_values(by='Earnings',ascending=False)
        df_5 = df_5.reset_index()
        df_5 = df_5.drop(columns='index')
        color= px.colors.qualitative.Light24

        #@ Plot the chart
        fig_hist = px.histogram(df_5,x='Earnings',log_x=True,marginal='box',
                   template='plotly_dark',color_discrete_sequence=color,hover_data=df_5)
        fig_hist.update_layout(bargap=0.05,width=600,height=500,
                           title='<b>DISTRIBUTION IN EARNINGS OF PLAYERS</b>'
                           ,plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_hist)

#$ Plot the scatter plot showing the correlation of earnings along the years
    with col_b:
    
        #@ Sort and modify data
        df_4 = df.sort_values(by='Earnings',ascending=False)
        df_4 = df_4.sort_values(by='Year')
        df_4 = df_4.reset_index()
        df_4 = df_4.drop(columns='index')

        #@ Plot the chart
        colors = px.colors.qualitative.Light24        
        fig_scatter = px.scatter(df_4,x='Year',y='Earnings',
                    size='Earnings',color='Sport',hover_data=df_4,template='plotly_dark',
                    size_max=50,color_discrete_sequence=colors)                                                        
        fig_scatter.update_layout(
            title='<b>POSITIVE CORRELATION OF EARNINGS ALONG THE YEARS </b>',width=700,height=500
        ,plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter)
