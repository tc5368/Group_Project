# group13Yes
# group13HelloWorld

#pip install cufflinks plotly
#pip install chart-studio
import chart_studio.plotly as py
import plotly.graph_objs as go
import chart_studio
chart_studio.tools.set_credentials_file(username='group13Yes', api_key='OspkIgNNW6CTIM7110px')


import pandas as pd
from datetime import datetime

df = pd.read_csv('tsla.csv', parse_dates= True, index_col=0)
df.reset_index(inplace=True)


fig = go.Figure(data=go.Ohlc(x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']))
fig.show()
