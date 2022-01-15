from io import BytesIO, TextIOWrapper
import re
from google_images_download import google_images_download
import sys
from unicodedata import normalize


def get_photos_from_google(city: str, key: str, num: int = 1):
    normalized = normalize('NFD', f'"{key}" {city}')
    key = normalized

    try:
        f = open("photos-cache", "r")
        for line in f:
            if line.split("\t")[0] == normalized:
                return line.split("\t")[1]
        f.close()
    except:
        pass

    old_stdout = sys.stdout
    sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

    response = google_images_download.googleimagesdownload()

    arguments = {
        "keywords": key,
        "limit": num,
        "print_urls": True,
        "no_download": True
    }
    paths = response.download(arguments)

    sys.stdout.seek(0)
    output = sys.stdout.read()

    sys.stdout.close()
    sys.stdout = old_stdout

    result = []
    for line in output.split("\n"):
        if line.startswith("Image URL:"):
            result.append(line.replace("Image URL: ", ""))

    if result:
        f = open("photos-cache", "a")
        f.write(normalized + "\t" + result[0] + "\n")
        f.close()
        return result[0]

    return ""


if __name__ == "__main__":
    print(get_photos_from_google("Renesansowy lamus", "Kraków"))
