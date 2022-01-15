from typing import Dict, Any
import random

def generate_poi() -> Dict[str, Any]:
    poi: Dict[str, Any] = {}
    poi['name'] = random.choice(['Muzeum', 'Pałac', 'MS AGH'])
    poi['description'] = random.choice(['Muzeum', 'Pałac', 'MS AGH'])
    poi['address'] = random.choice(['Morska', 'Nowa', 'Wysoka']) + " " + str(random.randint(5,30))
    poi['category'] = random.choice(['Zwiedzanie', 'Jedzenie'])
    poi['latitude'] = random.uniform(50, 51)
    poi['longitude'] = random.uniform(19, 20)
    poi['open_hour'] = random.randint(6, 10)
    poi['closehour'] = random.uniform(18, 22)
    poi['picture_url'] = 'google.com'

    return poi