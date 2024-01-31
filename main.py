from fastkml import kml
from geopy.distance import geodesic 
from markupsafe import escape
from flask import Flask, request
from functools import lru_cache

app = Flask(__name__)

#Write tests to confirm caching works and concurrent requests with same params dont process. TODO.

stations=[] #global variable for list of stations.

def parseSEPTAKMLfile():
    with open("./SEPTARegionalRailStations2016.kml", 'rt', encoding="utf-8") as myfile:
        doc=myfile.read()
    k = kml.KML()
    k.from_string(doc.encode('utf-8'))
    documentfeatures = list(k.features())
    folderfeature = list(documentfeatures[0].features())
    placemarkfeatures = list(folderfeature[0].features())
    #print("Number of stations in KML file: ",len(placemarkfeatures))
    stations = []
    for placemark in placemarkfeatures:
        station_name = placemark.extended_data.elements[0]._data[9]['value']
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
    #print("Nearest Station Response as GeoJSON: ",response)
    return response

@lru_cache(maxsize=None) #This is temp cache. Change to external caching mechanism.
def getClosestStation(currentCoordinates): 
    #To pass list to a cached function - convert to tuple. TODO.
    global stations #use global stations variable in this function
    print("Not cached. Searching for closest station.")
    nearest_station = min(stations, key=lambda station: geodesic(currentCoordinates, station["coordinates"]).miles)
    print("Nearest Station as Object: ",nearest_station)
    formattedResponse = formatStationResponse(nearest_station)
    return formattedResponse

@app.route('/closestStation')
def returnClosestStationResponse():
    #Handle case where parameters are not given. TODO.
    lat  = request.args.get('lat', None)
    long = request.args.get('long', None)
    currentCoords = (lat, long)
    print("Coords to get closest station for: ",currentCoords)
    closestStationResponse = getClosestStation(currentCoords)
    return closestStationResponse

#Handle default URLs. TODO.
def main():
    global stations
    stations = parseSEPTAKMLfile() #setup stations list for API.
    print("Stations Loaded. Setup Complete.")
    app.run(debug=True)
main()