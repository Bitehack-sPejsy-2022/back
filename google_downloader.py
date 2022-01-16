import re
import re
import dryscrape
from bs4 import BeautifulSoup

session = dryscrape.Session()


def get_photos_from_bing(city: str, key: str):
    key = f'"{key}" {city}'

    key = key.lower().replace("ó", "o").replace("ż", "z").replace("ź", "z").replace(
        "ś", "s").replace("ć", "c").replace("ą", "a").replace("ę", "e").replace("ł", "l").replace("ń", "n")

    try:
        with open("cache-photos", "r") as f:
            for line in f:
                line = line.split("\t")
                if line:
                    if line[0] == key:
                        return line[1].strip()
            else:
                pass
    except:
        pass

    print(key)

    session.visit(
        f'https://www.bing.com/images/search?q={key}&form=HDRSC2&first=1&tsc=ImageBasicHover')
    response = session.body()
    soup = BeautifulSoup(response)

    for i in soup.find_all("a", {"class": "iusc"}):
        a = re.search('\"murl\":\"[^\"]+\.[a-z]+\"', str(i))
        if a:
            with open("cache-photos", "a") as f:
                f.write(key + "\t" + a.group(0)[8:-1] + "\n")
            return a.group(0)[8:-1].strip()
            break

    with open("cache-photos", "a") as f:
        f.write(key + "\t" + " " + "\n")
        return ""
    return ""


if __name__ == "__main__":
    print(get_photos_from_bing("Renesansowy lamus", "Kraków"))
