#importtamos las librerias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import json

#importamos poligonos de comunas 
shapefile='/home/kali/datascience/data//PROVINCIAS_inei_geogpsperu_suyopomalia.shp'

gdf=gpd.read_file(shapefile,encoding='utf-8')

df_final=gdf[['NOMBDEP','NOMBPROV','POBTOTAL','geometry']]

#leer data como json
merged_json=json.loads(df_final.to_json())
#convertir objeto a string
json_data=json.dumps(merged_json)

from bokeh.io import output_notebook, show, output_file, save
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource,LinearColorMapper, HoverTool
from bokeh.palettes import brewer   
import plotly as plt

#max color
max_color=df_final['POBTOTAL'].max()
print(max_color)
#cargar la data json_data
gsource=GeoJSONDataSource(geojson=json_data)
#Definimos una paleta de colores
colores =brewer['YlGnBu'][9]
#revertir la paleta para que a mayor numero, mas oscuro 
#inicializar linearcolormapper para que asocie un numero a los colores 
color_mapper=LinearColorMapper(palette=colores,low=0,high=max_color)
#agregar hovers 
hover=HoverTool(name='NOMBPROV',tooltips=[('PROVINCIA','@NOMBPROV'),
                                             ('DEPARTAMENTO','@NOMBDEP'),
                                             ('POBLACION','@POBTOTAL')])
#creamos el bojeto figura
fig=figure(title='mapa provincial',
           toolbar_location=None,
           tools=[hover])

fig.xgrid.grid_line_color=None
fig.ygrid.grid_line_color=None
fig.title.text_font_size='20pt'

#ocultamos los ejes 
fig.axis.visible=False

#agregamos provincias
fig.patches('xs','ys',
            source=gsource,
            fill_color={'field':'POPTOTAL','transform':color_mapper},
            line_width=0.2,
            name='provincias')

output_notebook()
show(fig)