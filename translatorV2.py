
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
# the directory of where the files are storage, can be change
directories =  ["game","dialog"]


#     # remove from whitelist in 
# open(f'whitelist.txt', 'w').write(str([]))
# whitelist = open(f'whitelist.txt', 'r').read()
# whitelist_list = ast.literal_eval(whitelist)
# file_list_filter = [item for item in file_list if item not in whitelist]
# file_list_filter.sort()

# funcion that translate everything

# By using regex, it will extract the text and the number from the files, if the file is {100}{}{hello word}, it will return a list of 2 items: [100]["Hello word"]
# if the input is {100}{}{}, it will return [100][None]
# if there's no match, will not return nothing

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

# This translate using any API as external request, can be change to any other, by default its use Azure Translate
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

# This translate using gpytranslate, can be change to any other
async def deep_translate(text):
    t = Translator()
    translation = await t.translate(text, sourcelang="ru", targetlang="en")
    return translation.text


# This will keep the file encoding the same to any modified file, due to the files are in Russian, there's some encoding that are different
def detect_file_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

# Replace special characters with Unicode escape sequences, this is for special characters
# This works only with any Google Translate API, Azure dont support it
def replace_special_characters(text):
    return unidecode(text)

# Each time that a file is transalte, it will be add it to a whitelist to avoid re-translate it
# This file must be reated before the code run, keep the name the same and the content must be an empty list "[]"
def white_list(file_name):
   whitelist = open(f'whitelist.txt', 'r').read()
   whitelist_list = ast.literal_eval(whitelist)
   whitelist_list.append(file_name)
   open(f'whitelist.txt', 'w').write(str(whitelist_list))

# This manage the translation, if one of the translation API fail, it will switch to the other and so on, in order to keep it automatic
# Can add as much layer that you want, there's also an option to throw an intencional error to use a specific translation API
def translation_fallback(text, trigger_first=False):
    try:
        if trigger_first:
            raise Exception("trigger first")
        return asyncio.run(deep_translate(text))
    except Exception as error1:
        print(f"\nerror in translation_fallback: {text} \n {error1}")
        try:
            return translate(text)
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
    
