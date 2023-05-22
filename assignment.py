import pandas as pd
import geopandas as gpd
import folium
from geopy.geocoders import Nominatim
from shapely.geometry import Point
from math import cos, sin, asin, sqrt, radians
import pyproj
import fiona
import shapely


# calculate lat & lon from inputted location
loc = Nominatim(user_agent="GetLoc")
getLoc = loc.geocode("washington") # enter location for distance to be calculated

# print location & coordinates
print(getLoc.address)
print("latitude = ", getLoc.latitude)
print("Longitude = ", getLoc.longitude)

m = folium.Map(location=(getLoc.latitude, getLoc.longitude), zoom_start=7, tiles="cartodb positron")

user_location = Point(getLoc.latitude, getLoc.longitude)
print(user_location)

pt = gpd.GeoDataFrame({
    'lat': [getLoc.latitude],
    'lon': [getLoc.longitude],
    'name': [getLoc.address],
},
    geometry=gpd.points_from_xy([getLoc.longitude], [getLoc.latitude]),  # add geometry to user location
    crs='epsg:2770',  # 4326
)
# dtype=str)

# print(pt)

# Point((getLoc.latitude, getLoc.longitude))

for i in range(0, len(pt)):
    folium.Marker(
        location=[pt.iloc[i]['lat'], pt.iloc[i]['lon']],
        popup=pt.iloc[i]['name'],
    ).add_to(m)

# airports = gpd.read_file('data_files/UK_Outline.shp')
# m = airports.explore( cmap='viridis')

df = pd.read_csv('data_files/Airports.csv')  # read the csv data

# create a new geodataframe for airport locations
airports = gpd.GeoDataFrame(df[['name', 'category', 'lon', 'lat']],
                            # use the csv data
                            geometry=gpd.points_from_xy(df['lon'], df['lat']),  # set the geometry using points_from_xy
                            crs='epsg:2770',
                            )
# set the CRS using a text representation of the EPSG code for WGS84 lat/lon
# dtype=str)


airports['distance'] = airports['geometry'].distance(user_location)
airports.sort_values(by='distance', ascending=True, inplace=True)
airports.reset_index(inplace=True)


def nearest_airport():
    airports.set_crs(epsg=4326, allow_override=True, inplace=True)
    print(airports.head)  # show the new geodataframe
    return airports.head()


nearest_airport()

# add the airport points to the existing map
airports.explore('category',
                 m=m,  # add the markers to the current map
                 marker_type='circle',  # circle marker on map
                 popup=True,  # information popup once clicked
                 legend=True,  # show legend
                 )

m.save('map.html')
