import sys
from flatten_json import flatten, unflatten_list
from selenium import webdriver
from bs4 import BeautifulSoup
import json

discard_url_in_output = True

if len(sys.argv) > 1 and sys.argv[1].lower() == 'false':
    discard_url_in_output = False

def separate_flattened_json_into_dicts(flattened_json):
    def is_float(element) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    separated_json = {}
    for key, value in flattened_json.items():
        split_key = key.split('_')

        separate_last_x_items = 1
        if is_float(split_key[-1]):
            separate_last_x_items = 2

        parent_key = split_key[:-separate_last_x_items]
        parent_key = '_'.join(parent_key)

        child_key = split_key[-separate_last_x_items:]
        child_key = '_'.join(child_key)

        if parent_key not in separated_json:
            separated_json[parent_key] = {}

        separated_json[parent_key][child_key] = value

    return separated_json

def create_driver():
   chrome_options = webdriver.ChromeOptions()
   chrome_options.add_argument("--headless")
   return webdriver.Chrome(options=chrome_options)

def get_info(dict_obj):
    driver = create_driver()
    driver.get(dict_obj['url'])
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    def find_element(selector, instance=0):
        return soup.select(selector)[instance].text

    for key, value in dict_obj.items():
        if key == 'url':
            continue
        if key[-2:] == '_1':
            continue

        if '_' in key:
            split_key = key.split('_')
            dict_obj[key] = find_element(value, dict_obj[f"{split_key[0]}_1"])
        else:
            dict_obj[key] = find_element(value)

    if discard_url_in_output:
        del dict_obj['url']

    driver.quit()
    return dict_obj

with open('input.json') as input_data:
    input_json = json.load(input_data)

flattened_input = flatten(input_json)
separated_flattened_json = separate_flattened_json_into_dicts(flattened_input)

for key, value in separated_flattened_json.items():
    separated_flattened_json[key] = get_info(value)

flattened_output = flatten(separated_flattened_json)
output = unflatten_list(flattened_output)
with open('output.json', 'w') as outfile:
    json.dump(output, outfile)