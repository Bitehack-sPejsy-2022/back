from OSMPythonTools.overpass import Overpass


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


def search_for_cool_objects(city):
    # cools found in Krakow: hotel hostel information motel gallery camp_site theme_park apartment zoo attraction guest_house museum
    COOLS = {"information", "gallery", "camp_site",
             "theme_park", "zoo", "attraction", "museum"}

    overpass = Overpass()
    result = overpass.query(f'nwr["addr:city"="{city}"]["tourism"]; out;')

    s = set({})
    for obj in result.elements():
        if not obj.tag("tourism") in COOLS:
            continue

        name = obj.tag("name")
        description = gen_description(obj)
        address = gen_address(obj)
        category = obj.tag("tourism")
        latitide, longitude = get_lat_lon(obj)
        picture_url = ""

        if None in (name, address, category, latitide, longitude, picture_url):
            continue
        s.add((name, description, address, category.capitalize(),
              latitide, longitude, picture_url))
    return s


def user_search(x: float, y: float) -> str:
    # 1° of latitude = always 111.32 km
    eps = 0.0005
    x0, x1 = x - eps, x + eps
    y0, y1 = y - eps, y + eps

    overpass = Overpass()
    result = overpass.query(f'nwr["tourism"]({x0},{y0},{x1},{y1}); out;')

    s = set({})
    for obj in result.elements():
        name = obj.tag("name")
        description = gen_description(obj)
        address = gen_address(obj)
        category = obj.tag("tourism")
        latitide, longitude = get_lat_lon(obj)

        picture_url = ""

        print((name, address, category, latitide, longitude, picture_url))

        if None in (name, address, category, latitide, longitude, picture_url):
            continue
        s.add((name, description, address, category.capitalize(),
              latitide, longitude, picture_url))
    return s


if __name__ == "__main__":
    for i in search_for_cool_objects("Kraków"):
        for j in i:
            print(j)
    print("--------------- TEST ---------------")
    print(user_search(50.06443278632467, 19.94349002838135))
