import requests
import json
import re
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy


# Generates and parses and html page. Extracts all relevant information and returns and dataframe table.
def collect_page_data(url):
    url = url
    req = requests.get(url)
    page_soup = bs(req.content, 'html.parser')
    page_soup.prettify()

    page_soup = page_soup.find("script", {"type":
                                              "application/ld+json"})
    json_dict = json.loads(page_soup.string)
    total_time = find_total_time(json_dict)

    title = search_dict(json_dict, 'name')[0][1]
    image = search_dict(json_dict, 'image')[0][1]
    ingredients = get_ingredients(url)
    rating_val = search_dict(json_dict, 'ratingValue')[0][1]
    rating_count = search_dict(json_dict, 'ratingCount')[0][1]
    category = search_dict(json_dict, 'recipeCategory')[0][1]
    cuisine = search_dict(json_dict, 'recipeCuisine')
    diet = get_suitable_for(json_dict)
    vegan = check_vegan(get_suitable_for(json_dict))
    vegetarian = check_vegetarian((get_suitable_for(json_dict)))

    df = pd.DataFrame(
        [[title, total_time, image, ingredients, rating_val, rating_count, category, cuisine, diet, vegan, vegetarian,
          url]], columns=['title', 'total_time', 'image', 'ingredients', 'rating_val', 'rating_count',
                          'category', 'cuisine', 'diet', 'vegan', 'vegetarian', 'url'])

    return df


# Finds the prep time and cook time of recipe and returns summed value.
def find_total_time(jsonDict):
    dict = jsonDict
    prepTime = dict["prepTime"]
    prepTime = (re.findall('[0-9]+', prepTime))
    prepTime = int(prepTime[0])

    cookTime = dict["cookTime"]
    cookTime = (re.findall('[0-9]+', cookTime))
    cookTime = int(cookTime[0])

    totalTime = cookTime + prepTime

    return totalTime


# Searches dictionary (and nested) and returns all matching key/value pairs.
def search_dict(query_dict, keys, dicts=None):
    if not dicts:
        dicts = [query_dict]
        query_dict = [query_dict]

    to_check = query_dict.pop(0)
    if isinstance(to_check, dict):
        to_check = to_check.values()

    for d in to_check:
        dtype = type(d)
        if dtype is dict or dtype is list:
            query_dict.append(d)
            if dtype is dict:
                dicts.append(d)

    if query_dict:
        return search_dict(query_dict, keys, dicts)

    return [(k, v) for d in dicts for k, v in d.items() if k in keys]


# If a user wishes to make a key list for later use.
def add_keys_to_search_manual_entry():
    keys = []
    input_test = True

    while input_test:
        keys.append(input("Type a key to add to list: "))
        while True:
            answer = input("Are you finished entering Keys? Yes or No ")
            yes = "Yes"
            no = "No"

            if answer == yes:
                input_test = False
                break
            elif answer == no:
                break
            elif answer != yes or no:
                print("Please type either Yes or No ")
    return keys


# Returns the ingredients in a list form from the URL.
def get_ingredients(url):
    url = url
    ingredients_list_return = []
    soup = re.search("__reactInitialState__ = (.*);", requests.get(url).text)[1]
    soup = json.loads(soup)
    soup = soup["recipeReducer"]["recipe"]["stagesWithoutLinks"][0]['ingredients']

    for ingredients in soup:
        i = ingredients['foods'][0]['title']
        ingredients_list_return.append(i)

    return ingredients_list_return


# Returns a list of the 'suitable for' diet requirements from a JSON.
def get_suitable_for(jsonDict):
    l = search_dict(jsonDict, 'suitableForDiet')
    numpy.warnings.filterwarnings('ignore', category=numpy.VisibleDeprecationWarning)
    list_flat = list(numpy.concatenate(l).flat)
    list_to_search = list.pop(list_flat)
    list_return = []

    for i in list_to_search:
        string = i
        list_return.append(string.partition(".org/")[2])

    return list_return


# Checks if the recipe is suitable for vegans by checking the 'suitable diet' list.
def check_vegan(suitable_for_list):
    if 'VeganDiet' in suitable_for_list:
        return 'Yes'
    else:
        return 'No'


# Checks if the recipe is suitable for vegetarians by checking the 'suitable diet' list.
def check_vegetarian(suitable_for_list):
    if 'VegetarianDiet' in suitable_for_list:
        return 'Yes'
    else:
        return 'No'


def export_to_csv(df):
    return df.to_csv()


print(export_to_csv(collect_page_data("https://www.bbc.co.uk/food/recipes/coconut_pancakes_with_38938")))


