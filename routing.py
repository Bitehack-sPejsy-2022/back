import openrouteservice
from openrouteservice.directions import directions
from openrouteservice import convert
from typing import Tuple, List


client = openrouteservice.Client(key='5b3ce3597851110001cf62485da6d011d1ca48179dbe061a80ee1fa6')

def find_route_single(start : Tuple[float, float], end : Tuple[float, float]) -> List[Tuple[float, float]]:
    dir = directions(client, ((start[1], start[0]), (end[1], end[0])))
    decoded = convert.decode_polyline(dir['routes'][0]['geometry'])
    return decoded['coordinates']

def find_route(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    path = []
    for i in range(1, len(points)):
        path += find_route_single(points[i-1], points[i])
    return path

if __name__ == "__main__":
    print(find_route([(52.552394,-1.818763), (52.563368,-1.818291), (52.563368,-1.818291), (52.552394,-1.818763)]))

'''
from asyncore import file_dispatcher
from pyroutelib3 import Router
from typing import Tuple, List

ROUTER = Router("foot") # Initialise it

def find_route_single(start : Tuple[float, float], end : Tuple[float, float]) -> List[Tuple[float, float]]:
    start = ROUTER.findNode(start[0], start[1])
    end = ROUTER.findNode(end[0], end[1])

    status, route = ROUTER.doRoute(start, end)

    if status == 'success':
        return list(map(ROUTER.nodeLatLon, route))
    else: 
        print("Adios :(")
        return []

def find_route(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    path = []
    for i in range(1, len(points)):
        path += find_route_single(points[i-1], points[i])
    return path

if __name__ == "__main__":
    print(find_route([(52.552394,-1.818763), (52.563368,-1.818291), (52.563368,-1.818291), (52.552394,-1.818763)]))
'''