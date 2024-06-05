import os
import csv

folder_path = 'data/csv'  # Replace with the path to your folder

# Get all the .csv files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Iterate over each .csv file
for file in csv_files:
  file_path = os.path.join(folder_path, file)
  
  # Read the file in 'utf-8' format
  with open(file_path, 'r', encoding='euc-kr') as csv_file:
    csv_data = csv_file.read(encodeing='euc-kr') 
  
  # Convert the file format to 'CP949'
  with open(file_path, 'w', encoding='CP949') as csv_file:
    csv_file.write(csv_data, encoding='CP949')