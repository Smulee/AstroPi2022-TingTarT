# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:43:32 2022

@author: marsjo001
"""

import pandas as pd
import plotly.express as px

csv = pd.read_csv('datamodi.csv') #Astropi CSV File

fig = px.scatter_geo(csv,lat="Lat", lon="Lng", hover_name="id")

fig.show()
    
