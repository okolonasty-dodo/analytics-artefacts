#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import geopandas as gpd
from matplotlib import pyplot as plt
import json 


# https://github.com/okolonasty-dodo/Russia_geojson_OSM/blob/master/GeoJson's/Countries/Russia_regions.geojson

# In[ ]:


f = open ("Russia_regions.geojson", "r")
geo_json = json.loads(f.read())


# In[ ]:


geo_json_regions = [geo_json["features"][i]["properties"]["region"] for i in range(len(geo_json["features"]))]


# In[ ]:


data = pd.read_csv("Sessions_by_City_2023_06_21.csv")
data = data.fillna("NaN")
data["ClientCity"] = data["ClientCity"].str.replace('ё', 'e', regex=False)
data["City"] = data.ClientCity.apply(lambda x: x.split(" (")[0])
data.head()


# In[ ]:


regions = pd.read_csv("Города и Регионы России - main.csv")
regions["Город"] = regions["Город"].str.replace('ё', 'e', regex=False)
regions["reg"] = regions["Регион"].apply(lambda x: x.split()[0])
data_regions = list(regions["reg"])
regions.head()


# In[ ]:


new_regions = []
for reg in data_regions:
    for json_reg in geo_json_regions:
        if reg in json_reg.split():
            new_regions.append(json_reg)
            break


# In[ ]:


regions["NewRegion"] = new_regions
data = pd.merge(data, regions, how = "left", left_on = "City", right_on = "Город" )
data.head()


# In[ ]:


regions[regions["Регион"].apply(lambda x: x.find("аб")) != -1]


# In[ ]:


data[data.NewRegion.isna()]


# In[ ]:


d = data.groupby(by = ["NewRegion"])[["MenuVisited_Sessions", "OrderCreated_Sessions", "OrderCanceled_Sessions"]].sum().reset_index()
d["menu_order"]          = round(d["OrderCreated_Sessions"]  / d["MenuVisited_Sessions"] * 100, 1)
d["create_cancel_order"] = round(d["OrderCanceled_Sessions"] / d["OrderCreated_Sessions"] * 100, 1)
d.head()


# In[ ]:


import plotly.express as px

fig = px.choropleth_mapbox(d, geojson=geo_json, locations='NewRegion', 
                           color='menu_order', featureidkey = "properties.region",
                           color_continuous_scale= "RdYlGn",#"Magma", #"Viridis",
                           hover_name = "NewRegion",
                           #range_color=(0, 1),
                           mapbox_style="carto-positron",
                           #mapbox_style = "carto-darkmatter",
                           zoom=3, center = {"lat": 55.44, "lon": 37.4},
                           opacity=0.8,
                           labels={'menu_order':'Конверсия меню-заказ',
                                  "NewRegion": "регион"},
                           #width = 1400,
                           #height = 700
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()


# In[ ]:


fig_canceled = px.choropleth_mapbox(d, geojson=geo_json, locations='NewRegion', 
                           color='create_cancel_order', featureidkey = "properties.region",
                           color_continuous_scale= "Viridis",#"Magma", #"Viridis",
                           hover_name = "NewRegion",
                           #range_color=(0, 1),
                           mapbox_style="carto-positron",
                           #mapbox_style = "carto-darkmatter",
                           zoom=3, center = {"lat": 55.44, "lon": 37.4},
                           opacity=0.7,
                           labels={'menu_order':'Конверсия меню-заказ',
                                  "NewRegion": "регион"},
                           #width = 1400,
                           #height = 700
                          )
fig_canceled.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig_canceled.show()


# In[ ]:


#from dash import Dash, html, dcc, callback, Output, Input
from dash import Dash, dcc, html, Input, Output, callback
import dash_auth
import base64
import datetime
import io
import plotly.express as px
import pandas as pd


# In[ ]:


PORT = 8005
#ADDRESS = 127.0.0.1


# In[ ]:


'''
VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}
'''

app = Dash(__name__)

'''
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
'''


app.layout = html.Div(
    children=[
    html.H2(
        children='Конверсия Меню-Заказ'
    ),
    html.A("Visit my Notion page for more...", href='https://plot.ly', target="_blank"),
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),   
])


if __name__ == '__main__':
    app.run(port=PORT, debug=False)

