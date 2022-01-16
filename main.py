from typing import List, Optional, Dict, Any, Tuple

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mockup_poi import generate_poi
from models import (
    Poi,
    ListOfPois,
    ListOfTimedPois,
    Trip, RecommendedTrips,
    GeoPoint,
    PlanTripRequest
)
from maps import search_for_cool_objects, user_search
from path import find_path
from matrix import get_matrix
from routing import find_route, find_route_single

app = FastAPI()

allow_origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ListOfPoi(BaseModel):
    list_of_poi: List[Poi]


@app.get('/')
async def root():
    return {"message": "ściągi kurwa tej?"}


@app.get('/poi/city/{city}', response_model=ListOfPois)
async def poi_city(city: str):
    if city == 'chuj':
        pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]
    else:
        pois: List[Dict[str, Any]] = search_for_cool_objects(city)


    return {'list_of_poi': [poi for poi in pois]}

@app.post('/generate_pois', response_model=ListOfPois)
async def generate_pois(chosen_pois: ListOfPois):
    # TODO query pois nearby already chosen pois

    pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [poi for poi in pois]}

@app.post('/search_near_point', response_model=ListOfPois)
async def search_near_point(point: GeoPoint):

    pois: List[Dict[str, Any]] = user_search(point.lat, point.lng)
    return {'list_of_poi': [poi for poi in pois]}

@app.post('/plan_trip', response_model=RecommendedTrips)
async def plan_trip(plan_trip_request: PlanTripRequest):
    # simplyfying names of arguments from request
    chosen_pois: ListOfTimedPois = plan_trip_request.chosen_pois
    start_time: str = plan_trip_request.start_time
    end_time: str = plan_trip_request.end_time 
    number_of_trips: int = plan_trip_request.number_of_trips 

    # decode time strings
    temp: str = start_time[(start_time.find('T') + 1) : start_time.find('Z') ]
    start_hour: float = float(temp[0:2]) + float(temp[3:5])/60 + float(temp[6:8])/3600

    temp: str = end_time[(end_time.find('T') + 1) : end_time.find('Z') ]
    end_hour: float = float(temp[0:2]) + float(temp[3:5])/60 + float(temp[6:8])/3600

    time_spent_in_pois: List[float] = []
    opening_hours: List[Tuple[float, float]] = []

    # nxn matrix where n is number of POIs
    transition_time_matrix: List[List[float]] = get_matrix([(poi_time.poi.longitude, poi_time.poi.latitude) for poi_time in chosen_pois.list_of_poi])

    for chosen_poi in chosen_pois.list_of_poi:
        time_spent_in_pois.append(chosen_poi.time_spent)
        opening_hours.append((chosen_poi.poi.open_hour, chosen_poi.poi.close_hour))

    trips: List[Trip] = []

    for _ in range(number_of_trips):
        path: List[int]
        starting_time: List[float]
        # TODO give deep copies
        path, starting_time = find_path(start_hour, end_hour, time_spent_in_pois, opening_hours, transition_time_matrix)

        temp_list_of_poi = [chosen_pois.list_of_poi[index] for index in path]
        list_of_poi = ListOfTimedPois(list_of_poi=temp_list_of_poi)
        
        # for n POIs there are n-1 transitions
        transit_times: List[float] = [0] * (len(path)-1)
        temp_route: List[Tuple[float, float]] = []
        for i in range(len(path) - 1):
            # get transition times between points on path
            transit_times[i] = transition_time_matrix[path[i]][path[i + 1]]

            temp_route += find_route_single((chosen_pois.list_of_poi[i].poi.latitude, chosen_pois.list_of_poi[i].poi.longitude),
                                        (chosen_pois.list_of_poi[i+1].poi.latitude, chosen_pois.list_of_poi[i+1].poi.longitude)) 
        
        route = [GeoPoint(lat=point[0], lng=point[1]) for idx,point in enumerate(temp_route) if idx % 10 == 0]
        bounds = (
                (min([route_point.lat for route_point in route]), min([route_point.lng for route_point in route])),
                (max([route_point.lat for route_point in route]), max([route_point.lng for route_point in route])),
        )

        trip = Trip(list_of_poi=list_of_poi, transit_times=transit_times, route=route, starting_time=starting_time, bounds=bounds)
        trips.append(trip)

    recommended_trips = RecommendedTrips(trips=trips)

    return recommended_trips
