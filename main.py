from fastkml import kml
from geopy.distance import geodesic 

def parseSEPTAKMLfile():
    with open("./SEPTARegionalRailStations2016.kml", 'rt', encoding="utf-8") as myfile:
        doc=myfile.read()
    k = kml.KML()
    k.from_string(doc.encode('utf-8'))
    documentfeatures = list(k.features())
    #print(documentfeatures)
    folderfeature = list(documentfeatures[0].features())
    #print(folderfeature)
    placemarkfeatures = list(folderfeature[0].features())
    print("Number of stations in KML file: ",len(placemarkfeatures))
    stations = []
    for placemark in placemarkfeatures:
        # print(placemarkfeatures[0].name)
        station_name = placemark.extended_data.elements[0]._data[9]['value']
        # print(placemarkfeatures[0].extended_data.elements[0]._data[9]['value'])
        # print(placemarkfeatures[1].extended_data.elements[0]._data[9]['value'])
        # print(placemarkfeatures[2].extended_data.elements[0]._data[9]['value'])
        # print(placemarkfeatures[3].extended_data.elements[0]._data[9]['value'])
        # print(placemarkfeatures[0]._geometry.geometry._coordinates)
        # [Longitude, Latitude] given from KML file. Convert to (Lat, Long) for geopy
        coordinates = (placemark._geometry.geometry._coordinates[1], placemark._geometry.geometry._coordinates[0])
        stations.append({"name": station_name, "coordinates": coordinates})
    print("Number of stations in array: ",len(stations))
    return stations
    

def formatStationResponse(station):
    # for response convert (Lat, Long) tuple back to [Longitude, Latitude]
    response = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [station["coordinates"][1], station["coordinates"][0]]
        },
        "properties": {
            "name": station["name"]
        }
    }
    print("Nearest Station Response as GeoJSON: ",response)
    return response

def getClosestStation(currentCoordinates, stations):
    nearest_station = min(stations, key=lambda station: geodesic(currentCoordinates, station["coordinates"]).miles)
    print("Nearest Station as Object: ",nearest_station)
    formattedResponse = formatStationResponse(nearest_station)
    return formattedResponse


def main():
    print("In main function")
    stations = parseSEPTAKMLfile()
    # for i in range(10):
    #     print(stations[i])
    #     print(stations[i]['name'])
    currentCoords = (39.952925, -75.219457) # coordinates to find closest station.
    print("Coords to get closest station for: ",currentCoords)
    getClosestStation(currentCoords, stations)

main()