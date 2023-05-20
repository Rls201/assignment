import matplotlib_inline

matplotlib_inline
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon

myFig = plt.figure(figsize=(10, 10))

myCRS = ccrs.UTM(29)

ax = plt.axes(projection=myCRS)

# first, we just add the outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature) # add the features we've created to the map.

myFig

myFig.savefig('map.png', bbox_inches='tight', dpi=300)







df = pd.read_csv('data_files/Airports.csv')  # read the airport csv file

# create geodataframe for airports
airports = gpd.GeoDataFrame(geometry=gpd.points_from_xy(df['lon'], df['lat']),
                            crs='epsg:4326')
airports.head()  # show the airport geodataframe

myFig