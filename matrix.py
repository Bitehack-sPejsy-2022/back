import openrouteservice
from openrouteservice.distance_matrix import distance_matrix

client = openrouteservice.Client(key='5b3ce3597851110001cf62485da6d011d1ca48179dbe061a80ee1fa6')

def get_matrix(latlons):
    global client
    output = distance_matrix(client, latlons)

    # Z sekund na godziny
    matrix = output['durations']
    for i in len(matrix):
        for j in len(matrix):
            matrix[i][j] /= 3600

    return matrix

    # Uwaga!