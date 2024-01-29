from fastkml import kml

def parseKMLfile():
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
    print(placemarkfeatures[0].name)
    print(placemarkfeatures[0].extended_data.elements[0]._data[9]['value'])
    print(placemarkfeatures[1].extended_data.elements[0]._data[9]['value'])
    print(placemarkfeatures[2].extended_data.elements[0]._data[9]['value'])
    print(placemarkfeatures[3].extended_data.elements[0]._data[9]['value'])
    

def getTrainDetails():
    pass
def main():
    print("In main function")
    parseKMLfile()
main()