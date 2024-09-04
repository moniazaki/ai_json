
import os

JSON_FILE_PATH = r'C:\Users\monia.fawzi\Downloads\ai json\llama3-1\sample.json'


if os.path.isfile(JSON_FILE_PATH):
    print("File exists.")
else:
    print("File does not exist.")
