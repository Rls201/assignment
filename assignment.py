import pandas as pd
import geopandas as gpd
import folium
from geopy.geocoders import Nominatim
import geopy.distance
import shapely
from shapely import Point

# calculate lat & lon from inputted location
loc = Nominatim(user_agent="GetLoc")
getLoc = loc.geocode("Morpeth")  # enter location for distance to be calculated

# print location & coordinates
print(getLoc.address)
print("latitude = ", getLoc.latitude)
print("Longitude = ", getLoc.longitude)

# Create folium map centered on selected location
m = folium.Map(location=(getLoc.latitude, getLoc.longitude), zoom_start=7, tiles="cartodb positron")

# save user location for distance calculation
user_location = Point(getLoc.latitude, getLoc.longitude)
print(user_location)

# create a GeoDataFrame
pt = gpd.GeoDataFrame({
    'lat': [getLoc.latitude],  # save as lat
    'lon': [getLoc.longitude],  # save as lon
    'name': [getLoc.address],  # store point's address as name
},
    # Select 27700 British National Grid as crs
    crs='epsg:27700',
    geometry=gpd.points_from_xy([getLoc.longitude], [getLoc.latitude]),  # add geometry to user location
    # 4326
)

# add pt as marker to folium map, using lat and lon for location
for i in range(0, len(pt)):
    folium.Marker(
        location=[pt.iloc[i]['lat'], pt.iloc[i]['lon']],
        popup=pt.iloc[i]['name'],  # displays marker name when clicked

    ).add_to(m)  # add marker to current map

# add Airport csv data file to script
df = pd.read_csv('data_files/Airports.csv')  # read the csv data

# create a new geodataframe for airport locations
airports = gpd.GeoDataFrame(df[['name', 'category', 'lon', 'lat']],
                            # use the csv data
                            crs='epsg:27700',
                            geometry=gpd.points_from_xy(df['lon'], df['lat']),  # set the geometry using points_from_xy

                            )



# add a field called distance to airports geodataframe and populate with distance to user's location
airports['distance'] = airports['geometry'].distance(user_location)
airports.sort_values(by='distance', ascending=True, inplace=True)  # sort values by distance smallest to largest
airports.reset_index(inplace=True)


# function to show nearest airports
def nearest_airport():
    airports.set_crs(epsg=4326, allow_override=True, inplace=True)
    print(airports.head)  # show the new geodataframe
    return airports.head()


# show nearest airports
nearest_airport()

# add the airport points to the existing map
airports.explore('category',
                 m=m,  # add the markers to the current map
                 marker_type='circle',  # circle marker on map
                 # marker=folium.Circle(radius=4, fill_color='red'),
                 popup=True,  # information popup once clicked
                 legend=True,  # show legend
                 )

# save the current map as a html file
m.save('map.html')
