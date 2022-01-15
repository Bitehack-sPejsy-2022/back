from typing import List, Optional, Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

from mockup_poi import generate_poi

app = FastAPI()

class Poi(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    category: str
    latitude: float
    longitude: float
    picture_url: str

class ListOfPoi(BaseModel):
    list_of_poi: List[Poi]


@app.get('/')
async def root():
    return {"poi": "hello world!"}


@app.get('/poi/city/{city}', response_model=ListOfPoi)
async def poi_city():
    # TODO query 3rd party API for poi
    # for now generate random pois
    pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [ poi for poi in pois ] }

@app.get('/poi/country/{country}')
async def poi_country():
    return {"message": "hello world!"}

@app.get('/poi/region/{region}')
async def poi_region():
    return {"message": "hello world!"}   