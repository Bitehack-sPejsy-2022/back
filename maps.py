from typing import List, Dict, Any, Tuple

from OSMPythonTools.overpass import Overpass

from google_downloader import get_photos_from_bing
from models import GeoPoint, Poi


def asdf(txt, x):
    return f"<{x}>" + txt + f"</{x}>"


def yesno_to_taknie(x):
    if x == "yes":
        return "tak"
    elif x == "no":
        return "nie"
    else:
        return "b/d"


def gen_description(obj):
    txt = ""
    if not (website := obj.tag("website")) is None:
        txt += asdf(asdf("Witryna internetowa: ",
                    "strong") + website + "\n", "p")
    if not (hours := obj.tag("opening_hours")) is None:
        txt += asdf(asdf("Godziny otwarcia: ", "strong") + hours + "\n", "p")
    if not (wheelchair := obj.tag("wheelchair")) is None:
        txt += asdf(asdf("Przystosowanie dla osób niepełnosprawnych: ", "strong") +
                    yesno_to_taknie(wheelchair) + "\n", "p")
    if not (fee := obj.tag("fee")) is None:
        txt += asdf(asdf("Opłaty: ", "strong") +
                    yesno_to_taknie(fee) + "\n", "p")
    if not (phone := obj.tag("phone")) is None:
        txt += asdf(asdf("Telefon: ", "strong") + phone + "\n", "p")
    if not (address := gen_address(obj)) is None:
        txt += asdf(asdf("Adres: ", "strong") + address + "\n", "p")

    return txt


def gen_address(obj):
    r = [obj.tag("addr:postcode"), " ", obj.tag("addr:city"), ", ",
         obj.tag("addr:street"), " ", obj.tag("addr:housenumber")]
    for i in r:
        if i is None:
            return ""
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


def search_for_cool_objects(city: str) -> List[Poi]:
    # cools found in Krakow: hotel hostel information motel gallery camp_site theme_park apartment zoo attraction guest_house museum
    COOLS = {"information", "gallery", "camp_site",
             "theme_park", "zoo", "attraction", "museum"}

    overpass = Overpass()
    result = overpass.query(f'nwr["addr:city"="{city}"]["tourism"]; out;')
    objects = []
    for obj in result.elements():
        if not obj.tag("tourism") in COOLS:
            continue

        name = obj.tag("name")
        description = gen_description(obj)
        address = gen_address(obj)
        category = obj.tag("tourism")
        latitude, longitude = get_lat_lon(obj)
        picture_url = get_photos_from_bing(city, name)

        if None in (name, address, category, latitude, longitude, picture_url):
            continue

        poi = Poi(
            name=name,
            description=description,
            address=address,
            category=category.capitalize(),
            latitude=latitude,
            longitude=longitude,
            open_hour=7,
            close_hour=20,
            picture_url=picture_url
        )

        objects.append(poi)

    return objects


def user_search(lat: float, lon: float, city: str) -> List[Dict[str, Any]]:
    cool_objs = search_for_cool_objects(city)

    cool_objs.sort(key=lambda obj: (obj.latitude - lat)
                   ** 2 + (obj.longitude - lon)**2)

    if cool_objs:
        return cool_objs[0]
    return []


def polygon_search(polygon: List[GeoPoint], city: str):
    if len(polygon) == 0:
        return []

    lat0, lat1, lng0, lng1 = polygon[0].lat, polygon[0].lat, polygon[0].lng, polygon[0].lng,
    point: GeoPoint
    for point in polygon[1:]:
        lat0 = min(point.lat, lat0)
        lat1 = max(point.lat, lat1)
        lng0 = min(point.lng, lng0)
        lng1 = max(point.lng, lng1)

    print(lat0, lat1, lng0, lng1)

    cool_objs = search_for_cool_objects(city)

    r = []
    for obj in cool_objs:
        if lat0 <= obj.latitude <= lat1 and lng0 <= obj.longitude <= lng1:
            r.append(obj)

    return r


if __name__ == "__main__":
    # for i in search_for_cool_objects("Kraków"):
    #     for j in i.items():
    #         print(j)
    print("--------------- TEST ---------------")
    # print(user_search(50.06443278632467, 19.94349002838135, "Kraków"))
    print("--------------- TEST ---------------")
    a = GeoPoint(lat=50.06303278632467, lng=19.84349002838135)
    b = GeoPoint(lat=51.06503278632467, lng=20.84549002838135)

    print(polygon_search([a, b], "Kraków"))
