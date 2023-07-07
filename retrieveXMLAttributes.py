import requests
from bs4 import BeautifulSoup

# XML URL
url = 'https://www.sec.gov/Archives/edgar/data/1722731/000149315223015479/fdct-20221231_pre.xml'

# define headers
headers = {
    'user-agent':'self m_smith627@hotmail.com'
        }

# Send a GET request to fetch the XML content
response = requests.get(url=url, headers=headers)
xml_content = response.content

#print(xml_content)

# Create a BeautifulSoup object to parse the XML
soup = BeautifulSoup(xml_content, 'xml')

# Find all elements with the xlink:labels attribute
titleElements = soup.find_all(attrs={'xlink:title': True})


# Find all elements with the xlink:labels attribute
labelElements = soup.find_all(attrs={'xlink:label': True})

print(titleElements)

print(labelElements)

# # Extract and print the values assigned to each xlink:labels item
# for element in titleElements:
#     xlink_titles = element['xlink:title']
#     print(xlink_titles)

# # Extract and print the values assigned to each xlink:labels item
# for element in labelElements:
#     xlink_labels = element['xlink:label']
#     print(xlink_labels)

#

# # Extract and print the parent xlink:title and xlink:labels values
# for element in titleElements:
#     xlink_title = element.find_parent('xlink:title')
#     #xlink_labels = element['xlink:label']
#     print(f"Parent xlink:title: {xlink_title}")
#     #print(f"xlink:labels: {xlink_labels}")
#     print()