# Python file to read in all the Twitter json files
# into a dataframe along with the finance data

import json
import pandas as pd
import os

# Read in 8months dataframe (included finance data)
df_8mos = pd.read_csv('8_mos_DataFrame.csv')

tickers = ['AMD', 'GE', 'NVDA', 'TSLA']
dict_list = []

for ticker in tickers:
    file_list = os.listdir('tweets/' + ticker)
    finance_data = pd.read_csv('Yahoo Finance/'+ticker+'.csv')
    date_list = finance_data['Date'].tolist()
    for fn in file_list:
        print(fn)
        fn_data = fn.split('.')
        if len(fn_data) != 2: continue # skip file that doesnt have a . in it (shouldn't happen)
        if fn_data[1] != 'json': continue # skip any extra files (probably shouldn't be any)
        # Read the json file 
        t = open('tweets/'+ticker+'/'+fn, 'r')
        tw = json.load(t)
        twitter_df = pd.DataFrame(tw)
        text_col = twitter_df['text'].tolist()
        time_col = twitter_df['created_at'].tolist()
        #indexList = df_8mos[(df_8mos['Date'] == fn_data[0]) & (df_8mos['Ticker']==ticker)].index
        #if len(indexList) == 0: continue # stock market closed on that day
        #index = indexList[0]
        #line_dict = {'Date':fn_data[0], 'Ticker':ticker, 'TweetList':text_col, 'TimeList':time_col, 'PriceChange':df_8mos.loc[index,'Price_Change'], 
            #'PriceDirection':df_8mos.loc[index,'Price_Direction'], 'OpenPrice':df_8mos.loc[index,'Open_Price'], 'ClosePrice':df_8mos.loc[index,'Close_Price'],
            #'HighPrice':df_8mos.loc[index,'High_Price'], 'LowPrice':df_8mos.loc[index,'Low_Price'], 'TradeVolume':df_8mos.loc[index,'Trade_Volume']}

        # Check for date in the finance data and only append data that exists in the finance data
        if fn_data[0] in date_list:
            line_dict = {'Date':fn_data[0], 'Ticker':ticker, 'TweetList':text_col, 'TimeList':time_col, 'Open':finance_data.loc[finance_data['Date']==fn_data[0],'Open'].values[0], 
                 'High':finance_data.loc[finance_data['Date']==fn_data[0],'High'].values[0], 'Low':finance_data.loc[finance_data['Date']==fn_data[0],'Low'].values[0],
                 'Close':finance_data.loc[finance_data['Date']==fn_data[0],'Close'].values[0], 'AdjClose':finance_data.loc[finance_data['Date']==fn_data[0],'Adj Close'].values[0],
                 'Volume':finance_data.loc[finance_data['Date']==fn_data[0],'Volume'].values[0]}
            dict_list.append(line_dict)

df = pd.DataFrame(dict_list)
df.to_csv('twitter_data.csv', index=False)
