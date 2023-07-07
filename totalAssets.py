import requests
from bs4 import BeautifulSoup

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


# # Define the URL of the balance sheet for the company you are interested in
# endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"
# #url = 'https://www.sec.gov/Archives/edgar/data/0000320193/000032019320000096/aapl-20200926.htm'
#
#
# # request the url, and then parse the response.
# response = requests.get(url = endpoint, params = param_dict, headers=headers)
# soup = BeautifulSoup(response.content, 'html.parser')

#
# # Define the URL of the balance sheet for the company you are interested in
url = 'https://www.sec.gov/Archives/edgar/data/0000320193/000032019320000096/aapl-20200926.htm'

# Send a request to download the HTML content of the balance sheet
response = requests.get(url = url, headers = headers)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table element that contains the total assets value

#print(response.content)  # print the raw HTML content
#print('-----'*1000)
print(soup.prettify())   # print the parsed HTML content in a more readable format

table = soup.find('table', attrs={'class': 'bsTable'})
#table =

print(soup.find_all('tr'))

# # Locate the row that contains the total assets value
# rows = table.find_all('tr')
# for row in rows:
#     cells = row.find_all('td')
#     if len(cells) > 1 and 'Total Assets' in cells[0].text:
#         total_assets = cells[1].text.strip().replace(',', '')
#         break
#
# # Print the total assets value
# print('Total assets:', total_assets)
