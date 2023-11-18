import numpy as np
import pandas as pd
# from here functions are of medal tally


def medal_tally(df):
    # drop duplicates rows on basis of 8 columns
    medal_tally = df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    # apply group by method
    medal_tally = medal_tally.groupby("region").sum()[["Gold","Silver","Bronze"]].sort_values('Gold',ascending=False).reset_index()

    # add new column which contain total of all medals
    medal_tally["Total"] = medal_tally["Gold"]+medal_tally["Silver"]+medal_tally["Bronze"]

    # change float to int type
    col = ["Gold","Silver","Silver","Bronze"]
    for i in col:
        df[i] = df[i].astype("int")

    return medal_tally


def country_year_list(df):
    years = np.unique(df["Year"]).tolist()
    years.sort()
    years.insert(0, "Overall")

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")

    return years, country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    flag = 0
    
    if year == "Overall" and country == "Overall":
        temp_df = medal_df

    if year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(year)]
    
    if year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
    
    if year != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df["region"] == country) & (medal_df["Year"] == int(year))]
        
    if flag==1:
        x = temp_df.groupby("Year").sum()[["Gold","Silver","Bronze"]].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby("region").sum()[["Gold","Silver","Bronze"]].sort_values('Gold',ascending=False).reset_index()
    
    x["Total"] = x["Gold"] + x["Silver"] + x["Bronze"]
    
    return x
    

# from here functions are of overall analysis


def data_over_time(df, col):
    over_time = df.drop_duplicates(subset=["Year",col])["Year"].value_counts().reset_index().sort_values(by="Year")
    if col=="region":
        over_time.rename(columns={"count":"No of countries"}, inplace=True)
    if col=="Event":
        over_time.rename(columns={"count":"No of events"}, inplace=True)
    if col=="Name":
        over_time.rename(columns={"count":"No of athletes"}, inplace=True)

    return over_time


def successfull_athletes(df, sport):
    temp_df = df.dropna(subset=["Medal"])
    
    if sport!="Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]
    
    x = temp_df["Name"].value_counts().reset_index().head(15).merge(df, on="Name", how="left")[["Name","count","Sport","region"]].drop_duplicates(["Name"])
    x.rename(columns={"count":"Medals"}, inplace=True)
    return x


# from here functions are of country-wise analysis

def yearwise_country_medal_tally(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"], inplace=True)
    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year").count()["Medal"].reset_index()
    return final_df

def country_heatmap(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"], inplace=True)
    new_df = temp_df[temp_df["region"] == country]
    pivot_table = new_df.pivot_table(index="Sport", columns="Year", values="Medal", aggfunc="count").fillna(0)
    
    return pivot_table


def successfull_country_athletes(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df[temp_df["region"] == country]
    
    x = temp_df["Name"].value_counts().reset_index().head(10).merge(df, on="Name", how="left")[["Name","count","Sport"]].drop_duplicates(["Name"])
    x.rename(columns={"count":"Medals"}, inplace=True)
    return x


# from here functions are of athelete-wise analysis

def width_v_height(df, sport):
    athelete_df = df.drop_duplicates(subset=["Name","region"])
    athelete_df["Medal"].fillna("No Madel", inplace=True)
    if sport!="Overall":
        temp_df = athelete_df[athelete_df["Sport"]==sport]
        return temp_df
    else:
        return athelete_df
    

def men_female_over_year(df):
    athelete_df = df.drop_duplicates(subset=["Name","region"])
    men_df = athelete_df[athelete_df["Sex"]=="M"].groupby("Year").count()["Name"].reset_index()
    female_df = athelete_df[athelete_df["Sex"]=="F"].groupby("Year").count()["Name"].reset_index()
    final = men_df.merge(female_df, on="Year", how="left")
    final = final.fillna(0).astype("int")
    final.rename(columns={"Name_x":"Male", "Name_y":"Female"}, inplace=True)

    return final