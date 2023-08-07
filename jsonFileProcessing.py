import os
import json
import pandas as pd
from sqlalchemy import create_engine
import re

# Function to read and deserialize a JSON file
def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Function to parse the number from the string
def parse_number_from_string(input_string):
    pattern = r'\d+'
    match = re.search(pattern, input_string)
    if match:
        return match.group()
    else:
        return None

# Function to process JSON files from a directory and insert data into SQL Server
def process_json_files(directory_path):
    # SQL Server connection parameters
    server = 'SMITH-BUSI-LAPT\FINSMITH'
    database = 'FinRecords'
    username = 'PyUser'
    password = 'PyPush102'
    table_name = 'CONTEXT'
    schema = 'dbo'


    # Create an sqlalchemy engine for SQL Server
    # conn = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
    # engine = create_engine(conn)

    # # Create a connection to SQL Server
    # conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    # conn = pyodbc.connect(conn_str)

    # Loop through each file in the specified directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            print(f"Processing file: {filename}")

            # Deserialize the JSON file and get the root element
            data = read_json_file(file_path)
            root = data['root']

            # Accessing individual data points from the 'xbrli:context' key
            contexts = root['xbrli:context']

            # Lists to store data for DataFrame
            context_ids = []
            entity_identifiers = []
            start_dates = []
            end_dates = []
            instant_dates = []

            # Processing each context data point and extracting data for the DataFrame
            for context in contexts:
                context_id = context['@id']
                entity_identifier = context['xbrli:entity']['xbrli:identifier']['#text']
                period_data = context['xbrli:period']

                # Extract the number from the string
                acc_number = parse_number_from_string(filename)

                if 'xbrli:startdate' in period_data:  # Date range context
                    start_date = period_data['xbrli:startdate']
                    end_date = period_data['xbrli:enddate']
                    instant_date = None
                elif 'xbrli:instant' in period_data:  # Instant context
                    instant_date = period_data['xbrli:instant']
                    start_date = None
                    end_date = None
                else:
                    start_date = None
                    end_date = None
                    instant_date = None

                # Append data to the lists
                context_ids.append(context_id)
                entity_identifiers.append(entity_identifier)
                start_dates.append(start_date)
                end_dates.append(end_date)
                instant_dates.append(instant_date)

            # Create a dictionary with the extracted data
            data_dict = {
                'ACCESSION_NUMBER' : acc_number,
                'CONTEXT_ID': context_ids,
                'ENTITY_IDENTIFIER': entity_identifiers,
                'START_DATE': start_dates,
                'END_DATE': end_dates,
                'INSTANT_DATE': instant_dates
            }

            # Create a pandas DataFrame from the dictionary
            df = pd.DataFrame(data_dict)

            # Push data from DataFrame to SQL Server table
            try:
                df.to_sql(table_name, conn, index=False, if_exists='append', schema=schema)
                print("Data inserted into SQL Server successfully!")
            except Exception as e:
                print(f"Error: {e}")

    # Close the connection
    # conn.close()

# Your JSON files directory path
json_files_directory = r'C:\Users\smithm7\PyRepo\SEC_EDGAR\sec_edgar'

# Process JSON files and insert data into SQL Server
process_json_files(json_files_directory)
