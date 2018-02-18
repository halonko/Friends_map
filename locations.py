import folium
from geopy.geocoders import ArcGIS


def find_location(place):
    '''
    :param place: a place where film was made/produced
    :return: latitude and longitude
    '''
    geolocator = ArcGIS(timeout=10)
    location = geolocator.geocode(place)
    lat = location.latitude
    long = location.longitude
    return lat, long


def map_creation(lat, long, name, fgroup, maps):
    '''

    :param lat: a latitude of some place
    :param long: a longitude of some place
    :param name: the name of the film
    :param fgroup: a group of markers, where a poins is added
    :param maps: a needed map, where this markers are shown
    :return: None
    '''
    fgroup.add_child(folium.Marker(location=[lat, long],
                                   popup=str(name).replace("'", "`"),
                                   icon=folium.Icon()))
    maps.add_child(fgroup)
    maps.save(' Map.html ')


def main(filee):
    # Creating a map and two layers - areas and populations
    mapa = folium.Map()
    fg = folium.FeatureGroup(name="Friends map")
    for i, j in filee.items():
        try:
            lat, long = find_location(j)
        except AttributeError:
            continue
        map_creation(lat, long, i, fg, mapa)
    mapa.save('templates/Map.html')
