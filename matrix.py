from typing import List, Tuple

import openrouteservice
from openrouteservice.distance_matrix import distance_matrix

client = openrouteservice.Client(key='5b3ce3597851110001cf62485da6d011d1ca48179dbe061a80ee1fa6')

def get_matrix(latlons: List[Tuple[float, float]]):
    global client
    output = distance_matrix(client, tuple(latlons), profile='foot-walking')

    # Z sekund na godziny
    matrix = output['durations']
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix[i][j] /= 3600

    return matrix

    # Uwaga!

if __name__ == '__main__':
    test_data = [(19.927975, 50.056150),
        (19.903234, 50.068007),
        (19.945146, 50.069448)]
    print(get_matrix(test_data))