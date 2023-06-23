import json
import re
import requests
from bs4 import BeautifulSoup

# Spoofs headers to ensure that our request is accepted from the URL
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

print(" \033[2;33;40m Task 1.1, 1.2  \033[0;0m", end='\n')
print(" \033[2;33;40m See source code lines 18 to 21 \033[0;0m")

url = "https://www.bbc.co.uk/food/recipes/avocado_pasta_with_peas_31700"
req = requests.get(url)
page_soup = BeautifulSoup(req.content, 'html.parser')
page_soup.prettify()

print(" \033[2;33;40m \n Task 2.1 2.2 \033[0;0m", end='\n')
print(page_soup.find("script", {"type":
                                    "application/ld+json"}))

cookingRec = page_soup.find("script", {"type":
                                           "application/ld+json"})

print(" \033[2;33;40m \n Task 2.3 \033[0;0m", end='\n')
print(" \033[2;33;40m Also see source code lines 33 to 36 \033[0;0m", end='\n')

cookingRec = json.loads(cookingRec.string)
cookingToPrint = cookingRec
cookingToPrint = json.dumps(cookingToPrint, sort_keys=True, indent=4)
print(cookingToPrint)

print(" \033[2;33;40m \n Task 2.4  \033[0;0m", end='\n')
print(" \033[2;33;40m Also see source code lines 41 to 50 \033[0;0m", end='\n')

prepTime = cookingRec["prepTime"]
prepTime = (re.findall('[0-9]+', prepTime))
prepTime = int(prepTime[0])

cookTime = cookingRec["cookTime"]
cookTime = (re.findall('[0-9]+', cookTime))
cookTime = int(cookTime[0])

totalTime = cookTime + prepTime
print(str(totalTime) + ' minutes')

print(" \033[2;33;40m \n Task 2.5  \033[0;0m", end='\n')
print(" \033[2;33;40m Also see source code lines 56 to 84 \033[0;0m", end='\n')


# searches dict and nested dicts for matching keys and print key value pairs and returns list
def search_dict(query_dict, keys, dicts=None):  # query_dict is dict to be searched, keys to be searched for, dicts for
    # recursive feature
    if not dicts:  # if this is the first iteration of function (i.e dicts=None)
        dicts = [query_dict]  # adds the dict to be searched to dicts
        query_dict = [query_dict]  # adds the dict to be searched to dicts

    to_check = query_dict.pop(0)  # Takes first key value pair
    if isinstance(to_check, dict):  # Checks if it is dict type
        to_check = to_check.values()  # If so, adds value to to_check list

    for d in to_check:
        dtype = type(d)  # assigns data type to dtype
        if dtype is dict or dtype is list:  # Checks if data type is a dict or a list
            query_dict.append(d)  # if so add it to the query list
            if dtype is dict:  # if it is a dict type (i.e. needs to be checked again)
                dicts.append(d)  # add it to dicts to recursively search through

    if query_dict:
        return search_dict(query_dict, keys, dicts)  # recursively runs the function, allows for all query_dict to be
        # added to dict eventually

    return [(k, v) for d in dicts for k, v in d.items() if k in keys]  # Creates a list where keys and values in
    # the dicts are added to


keys = ['name', 'image', 'ratingCount', 'ratingValue', 'recipeCategory', 'recipeCuisine', 'recipeIngredient',
        'suitableForDiet']
print(search_dict(cookingRec, keys))

print(" \033[2;33;40m \n Task 3.1 \033[0;0m", end='\n', flush=True)

print(page_soup.findAll(text=re.compile(r'window\.__reactInitialState__ = ({.*});')))

print(" \033[2;33;40m \n Task 3.2  \033[0;0m", end='\n')

print(page_soup.findAll(text=re.compile(r'window\.__reactInitialState__=({.*});')))  # Returns empty with spaced
# removed?

print(" \033[2;33;40m \n Task 3.3  \033[0;0m", end='\n')
print(" \033[2;33;40m See source code lines 98 to 100 \033[0;0m", end='\n')

ingredientsList = re.search("__reactInitialState__ = (.*);", requests.get(url).text)[1]
ingredientsList = json.loads(ingredientsList)
ingredientsList = ingredientsList["recipeReducer"]["recipe"]["stagesWithoutLinks"][0]['ingredients']

print(" \033[2;33;40m \n Task 3.4  \033[0;0m", end='\n')

ingredientsToPrint = []
for ingredients in ingredientsList:
    i = ingredients['foods'][0]['title']
    ingredientsToPrint.append(i)
print(ingredientsToPrint)
