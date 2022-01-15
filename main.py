from typing import List, Optional, Dict, Any

from fastapi import FastAPI

from mockup_poi import generate_poi
from models import Poi, ListOfPois

app = FastAPI()


@app.get('/')
async def root():
    return {"message": "ściągi kurwa tej?"}


@app.get('/poi/city/{city}', response_model=ListOfPois)
async def poi_city(city: str):
    # TODO query 3rd party API for poi
    # for now generate random pois
    pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [poi for poi in pois]}

@app.get('/poi/country/{country}', response_model=ListOfPois)
async def poi_country(country: str):
    # TODO query 3rd party API for poi
    # for now generate random pois
    pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [poi for poi in pois]}

@app.get('/poi/region/{region}', response_model=ListOfPois)
async def poi_region(region: str):
    # TODO query 3rd party API for poi
    # for now generate random pois
    pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [poi for poi in pois]}   

@app.post('/generate_pois', response_model=ListOfPois)
async def generate_pois(chosen_pois: ListOfPois):
    # TODO query pois nearby already chosen pois

    pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [poi for poi in pois]}
