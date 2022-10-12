# import our libraries
import requests
import pandas as pd
import bs4
from bs4 import BeautifulSoup

# base URL for the SEC EDGAR browser
endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"

# define the user-agent

# define our parameters dictionary
param_dict = {'action':'getcompany',
              'CIK':'1265107',
              'type':'10-k',
              'dateb':'20190101',
              'owner':'exclude',
              'start':'',
              'output':'',
              'count':'100'}

# define headers
headers = {
    'user-agent':'self m_smith627@hotmail.com'
        }

# request the url, and then parse the response.
response = requests.get(url = endpoint, params = param_dict, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Let the user know it was successful
print('Request Successful')
print(response.url)
print(response.text)

# base URL for the SEC EDGAR browser
endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"

# define our parameters dictionary
param_dict = {'action':'getcompany',
              'owner':'exclude',
              'company':'McDonalds'}

# define headers
# headers = {
#     'user-agent':'self m_smith627@hotmail.com'
#         }

# request the url, and then parse the response.
response = requests.get(url=endpoint, params=param_dict, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Let the user know it was successful.
print('Request Successful')
print(response.url)
print(response.text)

# find the document table with our data
doc_table = soup.find_all('table' , class_='tableFile2')

# define a base url that will be used for link building.
base_url_sec = r"https://www.sec.gov"

master_list = []

print(soup)

# loop through each row in the table.
for row in doc_table[0].find_all('tr')[0:3]:

    # find all the columns
    cols = row.find_all('td')

    print(cols[0])

    # if there are no columns move on to the next row.
    if len(cols) != 0:

        # grab the text
        filing_type = cols[0].text.strip()
        filing_date = cols[3].text.strip()
        filing_numb = cols[4].text.strip()

        # find the links
        filing_doc_href = cols[1].find('a', {'href': True, 'id': 'documentsbutton'})
        filing_int_href = cols[1].find('a', {'href': True, 'id': 'interactiveDataBtn'})
        filing_num_href = cols[4].find('a')

        # grab the the first href
        if filing_doc_href != None:
            filing_doc_link = base_url_sec + filing_doc_href['href']
        else:
            filing_doc_link = 'no link'

        # grab the second href
        if filing_int_href != None:
            filing_int_link = base_url_sec + filing_int_href['href']
        else:
            filing_int_link = 'no link'

        # grab the third href
        if filing_num_href != None:
            filing_num_link = base_url_sec + filing_num_href['href']
        else:
            filing_num_link = 'no link'

        # create and store data in the dictionary
        file_dict = {}
        file_dict['file_type'] = filing_type
        file_dict['file_number'] = filing_numb
        file_dict['file_date'] = filing_date
        file_dict['links'] = {}
        file_dict['links']['documents'] = filing_doc_link
        file_dict['links']['interactive_data'] = filing_int_link
        file_dict['links']['filing_number'] = filing_num_link

        # let the user know it's working
        print('-' * 100)
        print("Filing Type: " + filing_type)
        print("Filing Date: " + filing_date)
        print("Filing Number: " + filing_numb)
        print("Document Link: " + filing_doc_link)
        print("Filing Number Link: " + filing_num_link)
        print("Interactive Data Link: " + filing_int_link)

        # append dictionary to master list
        master_list.append(file_dict)