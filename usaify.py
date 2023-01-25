import pandas as pd
import geopandas as gpd
import numpy as np
import os
import sys
import orjson
import pathlib

TWEETS = '../extracted/'

def get_month(month):
    return sorted([str(i) for i in pathlib.Path(TWEETS).glob(f'{month}*/*')])

# joined geography of us regions
usa = gpd.read_file("https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson", driver="GeoJSON")

if __name__ == '__main__':
    for day_file in get_month(sys.argv[1]):
        with open(day_file, 'r', encoding='utf-8') as day:
            geo_table = []
            for i,line in enumerate(day):
                obj = orjson.loads(line)
                geo_table.append([i, obj['geo']['coordinates'][0], obj['geo']['coordinates'][1]])
            df = pd.DataFrame(geo_table, columns=['id','lat','long'])
            gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.long, df.lat), crs="EPSG:4326")
            gdf = gdf[['id','geometry']]
            gdf2 = gdf.sjoin(usa)
            goodset = set(gdf2['id'])
            new_name = 'usa'+day_file.split('geo')[1]
        with open(day_file, 'r', encoding='utf-8') as day:
            with open(f'../usa_extracted/{new_name}', 'w+', encoding='utf-8') as newday:
                for i, line in enumerate(day):
                    if i in goodset:
                        newday.write(line)
