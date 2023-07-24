import pandas as pd
import json

# Function to read and deserialize the JSON file
def read_json_file(filename):
    with open(r'C:\Users\marcu\PycharmProjects\sec_edgar\JSONFile000104746915001106.json', 'r') as file:
        data = json.load(file)
    return data

# Your JSON file path
json_file_path = 'data.json'

# Deserialize the JSON file and get the root element
data = read_json_file(json_file_path)
root = data['root']

# Accessing individual data points from the 'xbrli:context' key
contexts = root['xbrli:context']

# Processing each context data point
for context in contexts:
    context_id = context['@id']
    entity_identifier = context['xbrli:entity']['xbrli:identifier']['#text']
    period_data = context['xbrli:period']

    if 'xbrli:startdate' in period_data:  # Date range context
        start_date = period_data['xbrli:startdate']
        end_date = period_data['xbrli:enddate']
        print("Context ID:", context_id)
        print("Entity Identifier:", entity_identifier)
        print("Start Date:", start_date)
        print("End Date:", end_date)
    elif 'xbrli:instant' in period_data:  # Instant context
        instant_date = period_data['xbrli:instant']
        print("Context ID:", context_id)
        print("Entity Identifier:", entity_identifier)
        print("Instant Date:", instant_date)
    else:
        print("Invalid context format!")

    print("--------")

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
    'Context ID': context_ids,
    'Entity Identifier': entity_identifiers,
    'Start Date': start_dates,
    'End Date': end_dates,
    'Instant Date': instant_dates
}

# Create a pandas DataFrame from the dictionary
df = pd.DataFrame(data_dict)

# Display the DataFrame
print(df)
