import pandas as pd


def preprocess(df, region_df):

    # filtering summer values
    df = df[df["Season"] == "Summer"]
    
    # merge with region_df_subset
    df = df.merge(region_df, on="NOC", how="left")
    
    # dropping duplicates
    df.drop_duplicates(inplace=True)
    
    # one-hot encoding medals
    # medal = pd.get_dummies(df['Medal'])
    # medal_numeric = medal.astype(int)

    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df
