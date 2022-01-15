from typing import List, Optional, Dict, Any

from fastapi import FastAPI

from mockup_poi import generate_poi
from models import Poi, ListOfPoi

app = FastAPI()


@app.get('/')
async def root():
    return {"message": "ściągi kurwa tej?"}


@app.get('/poi/city/{city}', response_model=ListOfPoi)
async def poi_city():
    # TODO query 3rd party API for poi
    # for now generate random pois
    pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [poi for poi in pois]}

@app.get('/poi/country/{country}')
async def poi_country():
    # TODO query 3rd party API for poi
    # for now generate random pois
    pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [poi for poi in pois]}

@app.get('/poi/region/{region}')
async def poi_region():
    # TODO query 3rd party API for poi
    # for now generate random pois
    pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [poi for poi in pois]}   