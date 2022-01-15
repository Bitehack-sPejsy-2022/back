# Temat: "Oszczędzanie" - aplikacja o oszczedzaniu czegoś ogólnego

## Running an app:

### CLone repo
```
git clone https://github.com/Bitehack-sPejsy-2022/back.git
cd back
```
### Use uvicorn to run the app
```
uvicorn main:app --reload
```

## Endpoints:
### GET
"/" - home (idk if we return anything here)

"/poi/city/\<city\>" - points of interest in \<city\>

"/poi/country/\<country\>" - points of interest in \<country\>

"/poi/region/\<region\>" - points of interest in \<region\>

### POST

"/generate_pois" - it requires JSON in form of ListOfPois (look at models.py) and returns list of pois generated nearby ones that were already selected