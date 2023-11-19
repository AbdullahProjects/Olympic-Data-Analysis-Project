import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
# local file
import preprocessor, helper

# importing datasets
df = pd.read_csv("datasets/athlete_events.csv")
region_df = pd.read_csv("datasets/noc_regions.csv")

# clean dataset
df = preprocessor.preprocess(df, region_df)

# sidebar
st.sidebar.title("Olympic Analysis")
st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSzFPLC4pNAxOfR0aGwzpQiITpTpUyPxb9ug&usqp=CAU")
user_menu = st.sidebar.radio(
    "Select an option",
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)


# medal tally radion option
if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == "Overall" and selected_country == "Overall":
        st.title(f"Overall Medal Tally")

    if selected_year != "Overall" and selected_country == "Overall":
        st.title(f"Medal Tally in {selected_year} Olympics")

    if selected_year == "Overall" and selected_country != "Overall":
        st.title(f"{selected_country} overall performance")
        
    if selected_year != "Overall" and selected_country != "Overall":
        st.title(f"{selected_country} performance in {selected_year} Olympics")
        
    st.table(medal_tally)


# overall analysis radio option
if user_menu == "Overall Analysis":
    st.sidebar.header("Overall Analysis")

    editions = df["Year"].unique().shape[0]-1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    region = df["region"].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Regions")
        st.title(region)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, "region")
    fig = px.line(nations_over_time, y="No of countries", x="Year")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, "Event")
    fig2 = px.line(events_over_time, y="No of events", x="Year")
    st.title("Events over the years")
    st.plotly_chart(fig2)

    athletes_over_time = helper.data_over_time(df, "Name")
    fig2 = px.line(athletes_over_time, y="No of athletes", x="Year")
    st.title("Athletes over the years")
    st.plotly_chart(fig2)

    st.title("No. of Events over the time(Every Sport)")
    fig, axes = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(["Year","Sport","Event"])
    pivot_table = x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype("int")
    axes = sns.heatmap(pivot_table, annot=True)
    axes.tick_params(axis='both', labelsize=17)
    axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
    st.pyplot(fig)

    st.title("Successfull Atheletes")
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Select a sport:", sport_list)
    x = helper.successfull_athletes(df, selected_sport)
    st.table(x)



# country-wise analysis radio option
if user_menu == "Country-wise Analysis":
    # st.sidebar.header("Country-wise Analysis")

    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()

    st.sidebar.header("Country-wise Analysis")
    selected_country = st.sidebar.selectbox("Select the country", country_list)

    country_df = helper.yearwise_country_medal_tally(df, selected_country)
    fig = px.line(country_df, y="Medal", x="Year")
    st.title(f"{selected_country} Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(f"{selected_country} excels in the following Sports")
    pivot_table = helper.country_heatmap(df, selected_country)
    fig, axes = plt.subplots(figsize=(20,20))
    axes = sns.heatmap(pivot_table, annot=True)
    axes.tick_params(axis='both', labelsize=17)
    axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
    st.pyplot(fig)

    st.title(f"Top 10 athletes of {selected_country}")
    country_athletes = helper.successfull_country_athletes(df, selected_country)
    st.table(country_athletes)



# athelete-wise analysis radio option
if user_menu == "Athlete-wise Analysis":
    
    athelete_df = df.drop_duplicates(subset=["Name","region"])
    x1 = athelete_df["Age"].dropna()
    x2 = athelete_df[athelete_df["Medal"]=="Gold"]["Age"].dropna()
    x3 = athelete_df[athelete_df["Medal"]=="Silver"]["Age"].dropna()
    x4 = athelete_df[athelete_df["Medal"]=="Bronze"]["Age"].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4], ["Overall Age ", "Gold Medalist", "Silver Medalist", "Bronze Medalist"], show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)  

    sport_list = athelete_df["Sport"].unique().tolist()
    x = []
    name = []
    for sport in sport_list:
        temp_df = athelete_df[athelete_df["Sport"] == sport]
        age = temp_df[temp_df["Medal"]=="Gold"]["Age"].dropna()
        if age.shape[0] > 50:
            x.append(age) 
            name.append(sport)

    fig2 = ff.create_distplot(x, name, show_hist=False, show_rug=False)

        # Increase the size of the plot
    fig2.update_layout(width=800, height=600)

    # Rotate the labels on the x-axis for better visibility
    # fig2.update_layout(xaxis=dict(tickangle=-45))

    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig2)  

    st.title("Height vs Weight of Atheletes in Sports")
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")
    selected_sport = st.selectbox("Select a sport:", sport_list)

    temp_df = helper.width_v_height(df, selected_sport)

    fig, axes = plt.subplots(figsize=(10,7))
    axes = sns.scatterplot(x=temp_df["Weight"], y=temp_df["Height"], hue=temp_df["Medal"], style=temp_df["Sex"], s=50)
    st.pyplot(fig)

    
    st.title("Men vs Women participation over the years")
    final_df = helper.men_female_over_year(df)
    fig3 = px.line(final_df, x="Year", y=["Male","Female"])
    # fig3.update_layout(width=800, height=600)
    st.plotly_chart(fig3)
