from typing import List, Optional

from pydantic import BaseModel

class Poi(BaseModel):
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    category: str
    latitude: float
    longitude: float
    picture_url: str
class ListOfPois(BaseModel):
    list_of_poi: List[Poi]

class TimedPoi(BaseModel):
    poi: Poi
    time: float