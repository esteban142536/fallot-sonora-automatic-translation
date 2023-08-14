
#1- take the content of text folder and translate it from russia to english using chatgpt
    #its need to take all the files from this directory and merge together in mastercuts.txt
#2- add it back to the game folder
#3 ???
#4- profit
import os
import re
import dl_translate as dlt

mt= dlt.TranslationModel()

max_chars_per_file = 9999999999
englishDocument = ""

file_list = os.listdir('./')
file_list.remove('translator.py')

# funcions here
def write_to_master(file_content):
    master_file.write(file_content + '\n~\n')

def extract_value(input_string):
    match = re.match(r'\{(\d+)\}\{\}\{(.+?)\}', input_string)
    if match:
        return [match.group(1),match.group(2)]
    return None

file_count = 1
char_count = 0

master_file = open(f'mastercuts_{file_count}.txt', 'a')

for file_name in file_list:
    with open(file_name, 'r') as file:
        content = file.read()
        
        if char_count + len(content) > max_chars_per_file:
            master_file.close()
            file_count += 1
            char_count = 0
            master_file = open(f'mastercuts_{file_count}.txt', 'a')
        
        write_to_master(content)
        
        char_count += len(content) + 2  # Account for newline and '~' characters

        print(f'Done with {file_name}!')

master_file.close()

print('Done with all files!')
input('Awaiting order of translation...')

#translation from russian to english here
text = open(f'mastercuts_1.txt', "r")
print('translating '+len(text.readlines())+' lines')
for i in range(1, len(text.readlines()) + 1):
    extractText = extract_value(text.readline())

    if extractText is None:
        englishDocument += '\n'
        continue

    content = extractText[1]
    number = extractText[0]

    english = mt.translate(content, source=dlt.lang.RUSSIAN, target=dlt.lang.ENGLISH)
    englishDocument += '{' + number + '}{}{' + english + '}\n'
    print('line {i} done')
print(englishDocument)

input('Awaiting splitting...')

# Merge and split mastercuts files
merged_content = ""
merged_file_list = []
split_content = []

for i in range(1, file_count + 1):
    with open(f'mastercuts_{i}.txt', 'r') as file:
        content = file.read()
        merged_content += content
        merged_file_list.append(f'mastercuts_{i}.txt')

split_content = merged_content.split('\n~\n')

# Write split content to individual files
for i, file_name in enumerate(file_list):
    with open(file_name, 'w') as file:
        file.write(split_content[i])

print('Content split and written to individual files.')
