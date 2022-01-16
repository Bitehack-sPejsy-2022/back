from typing import List, Optional, Dict, Any, Tuple
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

from models import (
    Poi,
    TimedPoi,
    ListOfPois,
    ListOfTimedPois,
    Polygon,
    Trip, RecommendedTrips,
    GeoPoint,
    PlanTripRequest
)
from maps import search_for_cool_objects, user_search, polygon_search
from path import find_path
from matrix import get_matrix
from routing import find_route_single

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


@app.get('/poi/city/{city}', response_model=ListOfPois)
async def poi_city(city: str):
    pois: List[Poi] = search_for_cool_objects(city)

    return {'list_of_poi': pois}


@app.post('/search_near_point', response_model=ListOfPois)
async def search_near_point(point: GeoPoint):
    START = time.time()
    pois: List[Poi] = user_search(point.lat, point.lng, "Kraków")
    print("Near point", (time.time() - START))
    print(type(pois))
    return ListOfPois(list_of_poi=pois)


@app.post('/search_polygon', response_model=ListOfPois)
async def search_polygon(polygon: Polygon):
    START = time.time()
    pois: List[Poi] = polygon_search(
        polygon.list_of_points, "Kraków")
    print("Polygon", (time.time() - START))
    return {'list_of_poi': pois}


@app.post('/plan_trip', response_model=RecommendedTrips)
async def plan_trip(plan_trip_request: PlanTripRequest):
    START = time.time()
    # simplyfying names of arguments from request
    chosen_pois: ListOfTimedPois = plan_trip_request.chosen_pois
    start_time: str = plan_trip_request.start_time
    end_time: str = plan_trip_request.end_time
    number_of_trips: int = plan_trip_request.number_of_trips

    # decode time strings to float typed hours
    temp: str = start_time[(start_time.find('T') + 1): start_time.find('Z')]
    start_hour: float = float(temp[0:2]) + \
        float(temp[3:5])/60 + float(temp[6:8])/3600

    temp: str = end_time[(end_time.find('T') + 1): end_time.find('Z')]
    end_hour: float = float(temp[0:2]) + \
        float(temp[3:5])/60 + float(temp[6:8])/3600

    trips: List[Trip] = []

    for _ in range(number_of_trips):
        path: List[int]
        starting_time: List[float]

        # Generate data separately for each trip
        # append extra pois to chosen pois
        extra_pois: List[TimedPoi] = [TimedPoi(poi=poi, time_spent=random.uniform(
            1, 2)) for poi in search_for_cool_objects(plan_trip_request.city)]

        random.shuffle(extra_pois)
        extended_chosen_pois = chosen_pois.list_of_poi.copy()
        extended_chosen_pois.extend(extra_pois[:3])

        # nxn matrix where n is number of POIs
        transition_time_matrix: List[List[float]] = get_matrix(
            [(poi_time.poi.longitude, poi_time.poi.latitude) for poi_time in extended_chosen_pois])

        print("Macierz tranzycji", (time.time() - START))
        START = time.time()

        extended_time_spent_in_pois = []
        extended_opening_hours = []

        for chosen_poi in extended_chosen_pois:
            extended_time_spent_in_pois.append(chosen_poi.time_spent)
            extended_opening_hours.append(
                (chosen_poi.poi.open_hour, chosen_poi.poi.close_hour))

        path, starting_time = find_path(
            start_hour, end_hour, extended_time_spent_in_pois, extended_opening_hours, transition_time_matrix)

        print("Find Path", (time.time() - START))
        START = time.time()

        temp_list_of_poi = [extended_chosen_pois[index] for index in path]
        list_of_poi = ListOfTimedPois(list_of_poi=temp_list_of_poi)

        # for n POIs there are n-1 transitions
        transit_times: List[float] = [0] * (len(path)-1)
        temp_route: List[Tuple[float, float]] = []
        for i in range(len(path) - 1):
            # get transition times between points on path
            transit_times[i] = transition_time_matrix[path[i]][path[i + 1]]

            temp_route += find_route_single((extended_chosen_pois[path[i]].poi.latitude, extended_chosen_pois[path[i]].poi.longitude),
                                            (extended_chosen_pois[path[i+1]].poi.latitude, extended_chosen_pois[path[i+1]].poi.longitude))

        print("Route", (time.time() - START))
        START = time.time()

        # beware of werid indexing of point!!! It is a "feature" of routing library
        route = [GeoPoint(lat=point[1], lng=point[0])
                 for idx, point in enumerate(temp_route) if idx % 1 == 0]

        bounds = (
            (min([route_point.lat for route_point in route]),
             min([route_point.lng for route_point in route])),
            (max([route_point.lat for route_point in route]),
             max([route_point.lng for route_point in route])),
        )

        trip = Trip(list_of_poi=list_of_poi, transit_times=transit_times,
                    route=route, starting_time=starting_time, bounds=bounds)
        trips.append(trip)

    recommended_trips = RecommendedTrips(trips=trips)

    return recommended_trips
