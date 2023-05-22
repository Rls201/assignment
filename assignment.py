import pandas as pd
import geopandas as gpd
import folium
from geopy.geocoders import Nominatim
from shapely.geometry import Point
import fiona
import shapely

# calculate lat & lon from inputted location
loc = Nominatim(user_agent="GetLoc")
getLoc = loc.geocode("Brighton")

# print location & coordinates
#print(getLoc.address)
#print("latitude = ", getLoc.latitude)
#print("Longitude = ", getLoc.longitude)

m = folium.Map(location=(getLoc.latitude, getLoc.longitude), zoom_start=7, tiles="cartodb positron")

loc = Point(getLoc.latitude, getLoc.longitude)
print(loc)

pt = gpd.GeoDataFrame({
    'lat': [getLoc.latitude],
    'lon': [getLoc.longitude],
    'name': [getLoc.address],
},
    geometry=gpd.points_from_xy([getLoc.longitude], [getLoc.latitude]),  # add geometry to user location
    crs='epsg:2770',  # 4326
)
# dtype=str)

#print(pt)

# Point((getLoc.latitude, getLoc.longitude))

for i in range(0, len(pt)):
    folium.Marker(
        location=[pt.iloc[i]['lat'], pt.iloc[i]['lon']],
        popup=pt.iloc[i]['name'],
    ).add_to(m)

# airports = gpd.read_file('data_files/UK_Outline.shp')
# m = airports.explore( cmap='viridis')

df = pd.read_csv('data_files/Airports.csv')  # read the csv data

# create a new geodataframe
airports = gpd.GeoDataFrame(df[['name', 'category', 'lon', 'lat']],
                            # use the csv data, but only the name/website columns
                            geometry=gpd.points_from_xy(df['lon'], df['lat']),  # set the geometry using points_from_xy
                            crs='epsg:2770',
                            )
# set the CRS using a text representation of the EPSG code for WGS84 lat/lon
# dtype=str)


airports['distance'] = airports['geometry'].distance(loc)
airports.sort_values(by='distance', ascending=True, inplace=True)

airports.set_crs(epsg=4326, allow_override=True, inplace=True)
print(airports.head(4))  # show the new geodataframe

# add the airport points to the existing map
airports.explore('category',
                 m=m,  # add the markers to the same map we just created
                 marker_type='circle',  # use a marker for the points, instead of a circle
                 popup=True,  # show the information as a popup when we click on the marker
                 legend=True,  # don't show a separate legend for the point layer
                 )

m.save('map.html')
