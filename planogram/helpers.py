# Import the 'sub' function from the 're' module for regular expression substitution
from re import sub
import json

# Define a function to convert a string to snake case
def snake_case(s):
    # Replace hyphens with spaces, then apply regular expression substitutions for title case conversion
    # and add an underscore between words, finally convert the result to lowercase
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
        sub('([A-Z]+)', r' \1',
        s.replace('-', ' '))).split()).lower()

def flatten_list(xss):
    return [x for xs in xss for x in xs]

def get_percentage_of_whole(numerator, denominator):
    return round(numerator / denominator * 100, 2)

def get_list_from_json_file(PATH=""):
    data = []

    with open(PATH, 'r', encoding="utf-8") as f:
        data = json.load(f)

    return data

def get_dict_from_json_file(PATH=""):
    data = {}

    with open(PATH, 'r', encoding="utf-8") as f:
        data = json.load(f)

    return data
    
def dump_json_to_file(DATA, PATH=""):
    try:
        with open(PATH, 'w', encoding="utf-8") as f:
            json.dump(DATA, f)
    except:
        print("error:", PATH, "is an invalid file destination")
    