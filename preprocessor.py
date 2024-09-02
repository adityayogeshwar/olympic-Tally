import pandas as pd
def preprocess(df,noc_regions):
    #extracting only summer
    df=df[(df.Season=='Summer')==True]
    #merging both noc and df
    df=df.merge(noc_regions,how='left',on='NOC')
    #encoding
    df=pd.concat([df,pd.get_dummies(df['Medal'],dtype=int)],axis=1)
    #removing duplicates
    df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    return df

def process_with_11_player_teammatches_medals_issue(f,noc_regions):
    f = f[(f.Season == 'Summer') == True]
    # merging both noc and df
    f = f.merge(noc_regions, how='left', on='NOC')
    # encoding
    f = pd.concat([f, pd.get_dummies(f['Medal'], dtype=int)], axis=1)
    f=f.drop_duplicates()
    # removing duplicates
    # df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    return f