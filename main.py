from fastkml import kml
from geopy.distance import geodesic 

def parseSEPTAKMLfile():
    with open("./SEPTARegionalRailStations2016.kml", 'rt', encoding="utf-8") as myfile:
        doc=myfile.read()
    k = kml.KML()
    k.from_string(doc.encode('utf-8'))
    documentfeatures = list(k.features())
    print(documentfeatures)
    folderfeature = list(documentfeatures[0].features())
    print(folderfeature)
    placemarkfeatures = list(folderfeature[0].features())
    print(len(placemarkfeatures))
    stations = []
    for placemark in placemarkfeatures:
        # print(placemarkfeatures[0].name)
        station_name = placemark.extended_data.elements[0]._data[9]['value']
        # print(placemarkfeatures[0].extended_data.elements[0]._data[9]['value'])
        # print(placemarkfeatures[1].extended_data.elements[0]._data[9]['value'])
        # print(placemarkfeatures[2].extended_data.elements[0]._data[9]['value'])
        # print(placemarkfeatures[3].extended_data.elements[0]._data[9]['value'])
        # print(placemarkfeatures[0]._geometry.geometry._coordinates)
        # [Longitude, Latitude] given from KML file. Convert to (Lat, Long)
        coordinates = (placemark._geometry.geometry._coordinates[1], placemark._geometry.geometry._coordinates[0])
        stations.append({"name": station_name, "coordinates": coordinates})
    return stations
    

def formatStationResponse(station):
    pass

def getClosestStation(currentCoordinates, stations):
    # closestStation=""
    # minDistance=-1
    # for station in stations:
    #     stationCoords = station.coordinates
    #     stationDistance = 
    nearest_station = min(stations, key=lambda station: geodesic(currentCoordinates, station["coordinates"]).miles)
    print(nearest_station)

    return nearest_station


def main():
    print("In main function")
    stations = parseSEPTAKMLfile()
    # for i in range(10):
    #     print(stations[i])
    #     print(stations[i]['name'])
    currentCoords = (39.952925, -75.219457)
    getClosestStation(currentCoords, stations)

main()