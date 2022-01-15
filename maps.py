from typing import List, Dict, Any
import time

from OSMPythonTools.overpass import Overpass

from models import Poi

def gen_description(obj):
    txt = ""
    if not obj.tag("website") is None:
        txt += "Strona internetowa: " + obj.tag("website")

    return ""


def gen_address(obj):
    r = [obj.tag("addr:postcode"), " ", obj.tag("addr:city"), ", ",
        obj.tag("addr:street"), " ", obj.tag("addr:housenumber")]
    for i in r:
        if i is None:
            return None
    return "".join(r)


def get_lat_lon(obj):
    if not obj.lat() is None and not obj.lon() is None:
        return obj.lat(), obj.lon()
    elif len(obj.nodes()) == 0:
        return None, None
    elif not obj.nodes()[0].lat() is None and not obj.nodes()[0].lon() is None:
        return obj.nodes()[0].lat(), obj.nodes()[0].lon()
    else:
        return None, None


def search_for_cool_objects(city: str) -> List[Dict[str, Any]]:
    # cools found in Krakow: hotel hostel information motel gallery camp_site theme_park apartment zoo attraction guest_house museum
    COOLS = {"information", "gallery", "camp_site",
                "theme_park", "zoo", "attraction", "museum"}

    time_start = time.time()
    overpass = Overpass()
    result = overpass.query(f'nwr["addr:city"="{city}"]["tourism"]; out;')
    print((time.time() - time_start)/1000)
    objects = []
    for obj in result.elements():
        if not obj.tag("tourism") in COOLS:
            continue

        name = obj.tag("name")
        description = gen_description(obj)
        address = gen_address(obj)
        category = obj.tag("tourism").capitalize()
        latitide, longitude = get_lat_lon(obj)
        picture_url = ""

        if None in (name, address, category, latitide, longitude, picture_url):
            continue

        poi: Dict[str, Any] = {}
        poi['name'] = name
        poi['description'] = description
        poi['address'] = address
        poi['category'] = category
        poi['latitude'] = latitide
        poi['longitude'] = longitude
        poi['open_hour'] = 7
        poi['close_hour'] = 20
        poi['picture_url'] = picture_url

        print(time.time() - time_start)
        objects.append(poi)

    return objects


if __name__ == "__main__":
    for i in search_for_cool_objects("Kraków"):
        print(i)
