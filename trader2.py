import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


# Import yfinance
import yfinance as yf

# Get the daily data for stock Apple from 2017-04-01 to 2019-04-30
df = yf.download('AMD', start="2017-04-01", end="2019-04-30")


#calculating the smas and percent changes

df['percent change'] = df['Close'].pct_change()
df['200 sma'] = df['Close'].rolling(window = 200).mean().round(5)
df['50 sma'] = df['Close'].rolling(window = 50).mean().round(5)




total_df = pd.concat([df['50 sma'],df['200 sma'] , df['percent change']], axis = 1)

# #buy signals 
total_df['Criteria 1'] = df['Close'] > df['50 sma'] #when Price greater than 50 sma for hour periods
total_df['Criteria 2'] = df['Close'] > df['200 sma']
total_df['Criteria 3'] = total_df['Criteria 2'] | (df['50 sma'] >= df['200 sma']) == True

#strategies performance
# 1.buy and hold
# 2.buy or sell based on criteria 1
# 3.buy or sell based on criteria 2



total_df['buy and hold'] = 100*(1+df['percent change']).cumprod()
total_df['price crossover'] = 100*(1+total_df['Criteria 1'].shift(1)*df['percent change']).cumprod()
total_df['price crossover2'] = 100*(1+total_df['Criteria 2'].shift(1)*df['percent change']).cumprod()
total_df['price crossover3'] = 100*(1+total_df['Criteria 3'].shift(1)*df['percent change']).cumprod()

#calculate returns
start1 = df['Close'].iloc[50]
end1 = df['Close'].iloc[-1]
years1 = (df['Close'].count()+1-50)/252
return1 = (end1/start1)**(1/years1) -1 

print('buying and holding model yields', return1*100)

start2 = total_df['price crossover'].iloc[50]
end2 = total_df['price crossover'].iloc[-1]
years2 = (total_df['price crossover'].count()+1-50)/252
return2 = (end2/start2)**(1/years2) -1 

print('50sma crossover model yields', return2*100)

start3 = total_df['price crossover2'] .iloc[200]
end3 = total_df['price crossover2'] .iloc[-1]
years3 = (total_df['price crossover2'] .count()+1-200)/252
return3 = (end3/start3)**(1/years3) -1 

print('200 sma crossover yields ', return3*100)

start4 = total_df['price crossover3'].iloc[200]
end4 = total_df['price crossover3'].iloc[-1]
years4 = (total_df['price crossover3'].count()+1-200)/252
return4 = (end4/start4)**(1/years4) -1 

print('200 sma and price crossover yields', return1*100)


print(total_df)

plotdf = pd.concat([total_df['price crossover2'],total_df['price crossover'] , total_df['buy and hold'], total_df['price crossover3']], axis = 1)
plotdf.plot()
plt.show()


