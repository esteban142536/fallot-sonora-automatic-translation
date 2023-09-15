
#1- take the content of text folder and translate it from russia to english using google azure translator
#2- add it back to the game folder
#3 ???
#4- profit
import os
import re
from progress.bar import Bar
import requests
import chardet
import ast
import traceback
from gpytranslate import Translator
import asyncio
from unidecode import unidecode

key = '<key>'
region = '<Location>'
endpoint = '<endpoint>'

# file_list = os.listdir('./')
# file_list.remove('translatorV2.py')
# file_list.remove('whitelist.txt')
directories =  ["game","dialog"]


#     # remove from whitelist in 
# open(f'whitelist.txt', 'w').write(str([]))
# whitelist = open(f'whitelist.txt', 'r').read()
# whitelist_list = ast.literal_eval(whitelist)
# file_list_filter = [item for item in file_list if item not in whitelist]
# file_list_filter.sort()

# funcion that translate everything
    
def extract_value(input_string):
    number_match = re.match(r'\{(\d+)\}\{\}\{(.+?)\}', input_string)
    if number_match:
        number = int(number_match.group(1))
        text = number_match.group(2)
        return [number, text]

    text_match = re.match(r'\{(\d+)\}\{\}\{(.*)\}', input_string)
    if text_match:
        number = int(text_match.group(1))
        return [number, None]

def translate(text):
    # Use the Translator translate function
    url = endpoint + '/translate'
    # Build the request
    params = {
        'api-version': '3.0',
        'from': 'ru',
        'to': 'en'
    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json'
    }
    body = [{
        'text': text
    }]

    try:
        # Send the request and get response
        request = requests.post(url, params=params, headers=headers, json=body)
        response = request.json()
        # Get translation
        translation = response[0]["translations"][0]["text"]
        # Return the translation
    except Exception as error:
        print("\nerror in translate")
        full_traceback = traceback.format_exc()
        print("An error occurred:\n")
        print(response,'\n')
        print(full_traceback)
    return translation

async def deep_translate(text):
    t = Translator()
    translation = await t.translate(text, sourcelang="ru", targetlang="en")
    return translation.text



def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

def replace_special_characters(text):
    # Replace special characters with Unicode escape sequences
    return unidecode(text)

def white_list(file_name):
   whitelist = open(f'whitelist.txt', 'r').read()
   whitelist_list = ast.literal_eval(whitelist)
   whitelist_list.append(file_name)
   open(f'whitelist.txt', 'w').write(str(whitelist_list))

def translation_fallback(text, trigger_first=False):
    try:
        if trigger_first:
            raise Exception("trigger first")
        return translate(text)
    except Exception as error1:
        print(f"\nerror in translation_fallback: {text} \n {error1}")
        try:
            return asyncio.run(deep_translate(text))
        except Exception as error2:
            print(f"\nerror in translation_fallback: {text} \n {error2}")
            quit()


for directory in directories:
    files = os.listdir(directory)

    whitelist = open(f'whitelist.txt', 'r').read()
    whitelist_list = ast.literal_eval(whitelist)
    file_list_filter = [item for item in files if item not in whitelist]
    file_list_filter.sort()

    for filename in file_list_filter:

        file_path = os.path.join(directory, filename)

        file_encoding = detect_file_encoding(file_path)
        document = ""
        fileContent = open(file_path, 'r', encoding=file_encoding).readlines()
        with Bar('working in ' + file_path, max=len(fileContent)) as bar2:
            try:
                for text in fileContent:
                    values = extract_value(text)
                    if str(values) == 'None' or values is None:
                        document += '\n'
                        bar2.next()
                        continue
                    if values[1] is None:
                        document += "{" + str(values[0]) + "}{" + "}{" + "}\n"
                        bar2.next()
                        continue

                    # simple_text = replace_special_characters(values[1])  # Replace special characters

                    try:
                        translated_text = translation_fallback(values[1])
                    except Exception:
                        print(f"\nSwitching to specials")
                        simple_text = replace_special_characters(values[1])  # Replace special characters
                        translated_text = translation_fallback(simple_text, True)
                    
                    document += "{" + str(values[0]) + "}{}{" + translated_text + "}\n"
                    # os.system('cls')
                    bar2.next()
            except Exception as error:
                print("\nerror in " + file_path)
                full_traceback = traceback.format_exc()
                print("An error occurred:\n")
                print(full_traceback)
                break
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(document)
            white_list(filename)
            bar2.next()
    
