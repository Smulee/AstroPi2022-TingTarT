import plotly.express as px
import pandas as pd

px.set_mapbox_access_token(open(".mapbox_token").read()) # Get a token from https://www.mapbox.com/

df = pd.read_csv("datamodi.csv")
fig = px.scatter_mapbox(df, lat="Lat", lon="Lng", color="daynight", hover_name="id", zoom=1)
fig.show()
