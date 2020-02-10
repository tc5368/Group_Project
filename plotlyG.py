
#These are not used anywhere in the code ?

# import chart_studio.plotly as py
# import chart_studio
# from datetime import datetime
# chart_studio.tools.set_credentials_file(username='group13Yes', api_key='OspkIgNNW6CTIM7110px')


import plotly.graph_objs as go
import pandas as pd


df = pd.read_csv('tsla.csv', parse_dates= True, index_col=0)
df.reset_index(inplace=True)


fig = go.Figure(data=go.Ohlc(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']))
fig.show()
