import pandas as pd
import geopandas as gpd
import fiona
import sys
import twokenize
import pathlib
from collections import defaultdict
import subprocess
import numpy as np
import datetime
from io import StringIO
import json
import os
import re

TWEETS = "/home/ceggleston/dataset/tweets/"

# Total Population  B03002e1
# White             B03002e3
# African American  B03002e4
# Asian             B03002e6
# Hispanic          B03002e12

def get_month(month):
    return sorted([str(i) for i in pathlib.Path(TWEETS).glob(f'*{month}*')])

def get_year(year):
    return sorted([str(i) for i in pathlib.Path(TWEETS).glob(f'*{year}*')])

def get_output(geo):
    return subprocess.run(['./text.sh', str(geo)], capture_output=True, text=True)

if __name__ == '__main__':
    year = sys.argv[1]
    if len(sys.argv) == 3:
        month = sys.argv[2]
        if int(month) < 10:
            month = '0'+month 
        queue = get_month(year+'-'+month)
        if len(queue) > 0: 
            gdf = gpd.read_file(f"/home/ceggleston/dataset/ACS/ACS_{year}.geojson", driver="GeoJSON")
        while len(queue) > 0:
            handle = get_output(queue[0])
            df = pd.read_csv(StringIO(handle.stdout), sep=',', names=['lat','long','twid'])
            geoid_df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.long, df.lat))
            result = gpd.sjoin(geoid_df.set_crs("EPSG:4269"), gdf, how='inner', op='within')
            result = result.sort_index()
            result = result[['twid','GEOID','B03002e1','B03002e3','B03002e4','B03002e6','B03002e12']]
            name = queue[0].split('datatweets.')[1]
            print(name)
            result.to_csv(f'/home/ceggleston/dataset/geoids/geoid{name}', sep='\t', header=False, index=False)                        
            queue = queue[1:]
