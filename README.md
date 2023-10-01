# Translation Script for Fallout Sonora to English

This Python script is designed to translate the content of text files from Russian to English using the Google Azure Translator. The script follows these steps:

1. **Translation from Russian to English:**
   - The script scans the content of text files located in the specified folders.
   - It identifies text lines that require translation based on predefined patterns.
   - Special characters are replaced with Unicode escape sequences to ensure accurate translation.

2. **Translation Service Fallback:**
   - The script uses the Google Azure Translator API to translate the identified text.
   - In case of a translation failure, the script falls back to using the "gpytranslate" library for a deep translation.
   - If the deep translation also fails, the script prints an error message and proceeds to the next text line.

3. **Update Original Files:**
   - The translated text is added back to the original text files, replacing the content of the identified lines.
   - The script ensures that previously translated lines are whitelisted to prevent retranslation.

4. **Profit!**
   - The script completes the translation and updating process for all text files in the specified folders.

## How to Use

1. Make sure you have the required Python libraries installed, including "gpytranslate," "requests," "unidecode," "progress," and "chardet." You can install them using pip:

   ```
   pip install gpytranslate requests unidecode progress chardet
   ```

2. Configure your Google Azure Translator API key, region, and endpoint by setting the `key`, `region`, and `endpoint` variables in the script.

3. You will require to extract your `master.dat` for your copy of Fallout Sonora, you can use [Dat Explorer by Dims](https://www.nma-fallout.com/resources/dat-explorer-by-dims.56/)

4. Once extracter move to this directios `master.dat\text\russian`, there is where you put `translatorV2.py`  

5. Run the script to translate and update the text files.

## Notes

- This script should translate in a way that make the game playable to English speaking people, there's some typos and mistakes in some words and it will not translate images, if you think you can improve this code, feel free to make a pull request
- Certain special characters may appea weir, this is due some spanish characters
- The script detects the encoding of text files to ensure proper reading and writing.
- It uses a whitelist to avoid retranslating previously translated text lines.
- If any errors occur during translation or processing, the script will print detailed error messages to help diagnose the issue.

If you use the code, please give me credit or star it, it would help me a lot
