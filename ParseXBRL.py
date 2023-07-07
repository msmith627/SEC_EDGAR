import requests
from bs4 import BeautifulSoup


url = 'https://www.sec.gov/Archives/edgar/data/1722731/000149315223015479/fdct-20221231.xsd'

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

response = requests.get(url=url, headers=headers)

soup = BeautifulSoup(response.content, 'xml')

#print(response.url)
#print(response.text)

links = soup.find_all('link:definition')

#print(links)

responsepres = requests.get(url='https://www.sec.gov/Archives/edgar/data/1722731/000149315223015479/fdct-20221231_pre.xml', headers=headers)

#print(responsepres.text)

souppres = BeautifulSoup(responsepres.content, 'xml')
linklocs = souppres.find_all(attrs={'xlink:label': True})
tagList = souppres.find_all(getattr())

print(tagList)

for tag in tagList:
    if tag.name == 'link:presentationLink':
        print(tag.name)

#print(linklocs)

#soup2 = BeautifulSoup()
#
# for index, value in enumerate(reversed(links)):
#     if index > -1:
#         definition = value.text
#         print(linklocs)
#         for index1, value1 in enumerate(reversed(linklocs)):
#             if index1 > -1:
#                 linklocs = value1.text
#                 print(linklocs)
#         print(definition)
#         #print(definition.text.split(' ')[0])
#         #print(soup.definition.text)

# print(['link']['definition'])
#
# for link in links:
#     print(['links']['documents'])
# else:
#     print("no")
