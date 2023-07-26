import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

f = open("countries.geojson", "r")
geo_json = json.loads(f.read())
geo_json_regions = [geo_json["features"][i]["properties"]["ISO_A2"] for i in range(len(geo_json["features"]))]
data = pd.read_csv("Редизайн_приложения_старые_новые_клиенты_воронка_по_странам_for_map_2023_07_25.csv")
data = data.fillna("NaN")
data = data.groupby(by = "Country").sum()
d = data.reset_index()
d["menu_order"] = round(d["OrderCreated_Sessions"]  / d["MenuVisited_Sessions"] * 100, 1)
d = d[~d["Country"].isin(["TR", "BG", "AM", "RS", "HR", "CY"])]
d = d[d["menu_order"] != 0]

fig = px.choropleth_mapbox(d, geojson=geo_json, locations='Country',
                           color='menu_order', featureidkey = "properties.ISO_A2",
                           color_continuous_scale= "RdYlGn",#"Magma", #"Viridis",
                           hover_name = "Country",
                           #range_color=(0, 1),
                           mapbox_style="carto-positron",
                           #mapbox_style = "carto-darkmatter",
                           zoom=3, center = {"lat": 55.44, "lon": 37.4},
                           #opacity=0.8,
                           labels={'menu_order':'Конверсия меню-заказ',
                                  "Country": "страна"},
                           width = 1400,
                           height = 700
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

PORT = 8010
app = Dash(__name__)
app.layout = html.Div(
    children=[
    html.H2(
        children='Конверсия Меню-Заказ по странам'
    ),
    html.A("Моя страница в ноушне",
           href='https://www.notion.so/dodobrands/05321e94ff5d4d12a29e5651822f3bae',
           target="_blank"),
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
])

if __name__ == '__main__':
    app.run(port=PORT, debug=False)
