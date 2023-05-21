import matplotlib_inline

matplotlib_inline
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import pandas as pd
import geopandas as gpd
import os
from shapely.geometry import Point, LineString, Polygon
from geopy.geocoders import Nominatim

#calculate lat & lon from inputted location
loc = Nominatim(user_agent="GetLoc")
getLoc = loc.geocode("Morpeth")

#print location & coordinates
print(getLoc.address)
print("latitude = ", getLoc.latitude)
print("Longitude = ", getLoc.longitude)






outline = gpd.read_file('data_files/UK_Outline.shp')
outline.to_crs(epsg=27700, inplace=True)
#print(outline.head())

myFig = plt.figure(figsize=(10, 10), dpi=100)
myCRS = ccrs.epsg(27700)
m = outline.explore(cmap='viridis')
ax = plt.axes(projection=myCRS)

# first, we just add the outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature)  # add the features we've created to the map.

df = pd.read_csv('data_files/Airports.csv')  # read the airport csv file

# create geodataframe for airports
airports = gpd.GeoDataFrame(df[['name', 'category']],
                            geometry=gpd.points_from_xy(df['lon'], df['lat']),
                            crs='epsg:27700')
airports.head()
print(airports.head())  # show the airport geodataframe

# add the airport points to the existing map
airports.explore('name',
                 m=m,  # add the markers to the same map we just created
                 marker_type='circle',  # use a marker for the points, instead of a circle
                 popup=True,  # show the information as a popup when we click on the marker
                 legend=False,  # don't show a separate legend for the point layer
                 )

myFig

ax.set_extent([xmin - 5000, xmax + 5000, ymin - 5000, ymax + 5000], crs=myCRS)
myFig

myFig.savefig('map.png', bbox_inches='tight', dpi=300)


