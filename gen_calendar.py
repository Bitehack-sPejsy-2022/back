"""
Example of working calendar csv:

Subject, Start Date, All Day Event, Start Time, End Time, Location, Description
Kraków - Wycieczka,02/01/2022,TRUE,,,Kraków,Kraków - Wycieczka
Dom Zwierzyniecki,02/01/2022,FALSE,9:00 AM, 10:00 AM
Park Wola - Rodzinny Park Rozrywki Kraków,02/01/2022,FALSE,11:00 AM,12:00 PM
Galeria Sztuki Polskiej XIX wieku,02/01/2022,FALSE,13:00 PM,14:00 PM
Fabryka Emalia Oskara Schindlera,02/01/2022,FALSE,15:00 PM,16:00 PM
Muzeum Sztuki i Techniki Japońskiej Manggha,02/01/2022,FALSE,17:00 PM,18:00 PM
"""

from typing import List


def gen_calendar_csv(city: str, day_start: str, events: List[List[str, str, str, str]]) -> str:
    txt = "Subject, Start Date, All Day Event, Start Time, End Time, Location, Description\n"
    txt += f"{city} - Wycieczka, {day_start}, TRUE, , , {city}, {city} - Wycieczka\n"
    for event in events:
        place = event[0]
        hour_start = event[1]
        hour_end = event[2]
        address = event[3].replace(",", " ")
        txt += f"{place},{day_start},FALSE,{hour_start},{hour_end},{address}\n"
    return txt


if __name__ == "__main__":
    csv = gen_calendar_csv(
        "Kraków", "02/01/2022", [
            ["Galeria Sztuki Polskiej XIX wieku", "13:00 PM",
                "15:00 PM", "30-059 Kraków, Aleja Adama Mickiewicza 30"]
        ]
    )
    print(csv)
