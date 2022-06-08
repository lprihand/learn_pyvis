import zipfile
import os

cur_path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# open the zip file in reading mode and extract all files to the current working directory.
with zipfile.ZipFile(f'{cur_path}/zip_test.zip', mode='r') as myzip:
    myzip.extractall(cur_path)

# create a new zip file.
with zipfile.ZipFile(f'{cur_path}/zip_test.zip', mode='w') as myzip:
    myzip.write(f'{cur_path}/zip_text.txt')
