# Hachathon theme: "Saving" 

## Idea
An appliaction to save time while planning trips and while travelling.
The app will allow for easy travel planning, proposing interesting spots
and managaing moving between them. 
You need only few mouse clicks to generate multiple trip plans to choose from.

## Running an app:

### Clone repo
```
git clone https://github.com/Bitehack-sPejsy-2022/back.git
cd back
```
### Use uvicorn to run the app
```
uvicorn main:app --reload
```

### Setup the front
[Front repository](https://github.com/Bitehack-sPejsy-2022/front)

## Endpoints:
### GET:
"/" - home (idk if we return anything here)

"/poi/city/\<city\>" - points of interest in \<city\>

### POST:

"/search_near_point" - it searches for points in 50m epsilon around click on the map

"/search_polygon" - search points in boundaries of polygon

"/plan_trip" - takes request with POIs required by user and generates trip plans

<!-- "/generate_pois" - it requires JSON in form of ListOfPois (look at models.py) and returns list of pois generated nearby ones that were already selected -->

