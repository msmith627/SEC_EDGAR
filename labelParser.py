import attrs
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


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


for index, value in enumerate(reversed(links)):
    if index > -1:
        link = value
        print(link.contents[0])
        # dir(link)
#print(links)

responsepres = requests.get(url='https://www.sec.gov/Archives/edgar/data/1722731/000149315223015479/fdct-20221231_pre.xml', headers=headers)


#print(links)

souppres = BeautifulSoup(responsepres.content, 'xml')
#linklocs = souppres.'link:presentationLink'
linklocs = souppres.find_all('link:presentationLink')

# Find all elements with the xlink:labels attribute
elements = souppres.find_all()
#elements = souppres.find_all(attrs={'xlink:label':True})

label = ''

# print(elements.tag.name)
for element in elements:
    # if element.name == 'link:presentationLink':
    # print(element)
    if element.name == 'presentationLink':
        print('___' * 20)
        try:
            print(element.attrs['xlink:title'])
        except KeyError:
            pass
        print('_' * 20)
        #contents = element.content
        content_list = element.contents
        for content in content_list:
            if content != '''\n''':
                # print('hello')
                try:
                    print(content.attrs['xlink:label'])
                except KeyError:
                    pass
        print('___' * 20)
                # print(label)
        # print(element.contents)

    # print(element.name)
    # print('___' * 20)
    # print(element)
    # print('___' * 40)
    # print(element.label)

# parents = souppres.find_parents(attrs={'xlink:label': True})
# print(parents)
# print(elements)

# print(links.name)

#soup2 = BeautifulSoup()

# for index, value in enumerate(reversed(links)):
#     if index > -1:
#         definition = value.text
# #         print(linklocs)
# #         for index1, value1 in enumerate(reversed(linklocs)):
# #             if index1 > -1:
# #                 linklocs = value1.text
# #                 print(linklocs)
#         print(definition)
#         print(definition.text.split(' ')[0])
#         print(soup.definition.text)

# print(['link']['definition'])
#
# for link in links:
#     print(['links']['documents'])
# else:
#     print("no")