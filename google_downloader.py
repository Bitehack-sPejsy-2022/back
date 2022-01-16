import re
import re
import dryscrape
from bs4 import BeautifulSoup

session = dryscrape.Session()

def get_photos_from_bing(city: str, key: str):
    key = f'"{key}" {city}'

    key = key.lower().replace("ó", "o").replace("ż", "z").replace("ź", "z").replace(
        "ś", "s").replace("ć", "c").replace("ą", "a").replace("ę", "e").replace("ł", "l").replace("ń", "n")

    print(key)

    session.visit(
        f'https://www.bing.com/images/search?q={key}&form=HDRSC2&first=1&tsc=ImageBasicHover')
    response = session.body()
    soup = BeautifulSoup(response)

    for i in soup.find_all("a", {"class": "iusc"}):
        a = re.search('\"murl\":\"[^\"]+\"', str(i))
        if a:
            return a.group(0)[8:-1]
            break
    return ""


if __name__ == "__main__":
    print(get_photos_from_bing("Renesansowy lamus", "Kraków"))
