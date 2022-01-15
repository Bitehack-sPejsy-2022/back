from typing import List, Optional, Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mockup_poi import generate_poi
from models import Poi, ListOfPois
from maps import search_for_cool_objects

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
    return {"message": "ściągi kurwa tej?"}


@app.get('/poi/city/{city}', response_model=ListOfPois)
async def poi_city(city: str):
    pois: List[Dict[str, Any]] = search_for_cool_objects(city)

    if city == 'chuj':
        pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [poi for poi in pois]}

@app.post('/generate_pois', response_model=ListOfPois)
async def generate_pois(chosen_pois: ListOfPois):
    # TODO query pois nearby already chosen pois

    pois: List[Dict[str, Any]] = [generate_poi() for _ in range(3)]

    return {'list_of_poi': [poi for poi in pois]}
