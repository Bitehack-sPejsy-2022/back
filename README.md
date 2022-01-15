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

## Endpoints:
### GET:
"/" - home (idk if we return anything here)

"/poi/city/\<city\>" - points of interest in \<city\>

### POST:

"/generate_pois" - it requires JSON in form of ListOfPois (look at models.py) and returns list of pois generated nearby ones that were already selected