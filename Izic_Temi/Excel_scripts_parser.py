import pandas as pd
import json
import xlrd
import openpyxl

# User uploads file to a database which returns the file name
file = pd.ExcelFile(input("Drag and drop file here: "))
print('Input received from the user')

# Parse the sheets
sheets = file.sheet_names
if len(sheets) == 1:
    file = file.parse(sheets)
    print(file)
# If file contains more than one sheet, list of sheets is displayed and user selects sheets to parse.
else:
    print('File contains more than one sheet. Select the one you want')
    print(sheets)
    file = file.parse(input('File contains more than one sheet. Select the ones you want: '))
# File is displayed
    print(file)
# JSON returned
file.to_json('File.json')