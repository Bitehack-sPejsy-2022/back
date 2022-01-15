from io import BytesIO, TextIOWrapper
from google_images_download import google_images_download
import sys
from unicodedata import normalize


def get_photos_from_google(city: str, key: str, num: int = 1):
    normalized = normalize('NFD', f'"{key}" {city}')
    key = normalized

    old_stdout = sys.stdout
    sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

    response = google_images_download.googleimagesdownload()

    arguments = {
        "keywords": key,
        "limit": num,
        "print_urls": True,
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
    return result


if __name__ == "__main__":
    print(get_photos_from_google("Renesansowy lamus", "Kraków"))
