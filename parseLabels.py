import attrs
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
import xmltojson
import pandas as pd
import warnings
warnings.filterwarnings("ignore")




# url = 'https://www.sec.gov/Archives/edgar/data/1722731/000149315223015479/fdct-20221231.xsd'

# # define our parameters dictionary
# param_dict = {'action':'getcompany',
#               'CIK':'1265107',
#               'type':'10-k',
#               'dateb':'20190101',
#               'owner':'exclude',
#               'start':'',
#               'output':'',
#               'count':'100'}

# define headers
headers = {
    'user-agent':'self m_smith627@hotmail.com'
        }

# response = requests.get(url=url, headers=headers)
#
# soup = BeautifulSoup(response.content, 'xml')
#
# #print(response.url)
# #print(response.text)
#
# links = soup.find_all('link:definition')
#
#
# for index, value in enumerate(reversed(links)):
#     if index > -1:
#         link = value
#         print(link.contents[0])
#         # dir(link)
# #print(links)

responsepres = requests.get(url='https://www.sec.gov/Archives/edgar/data/1722731/000149315223015479/fdct-20221231_pre.xml', headers=headers)


#print(links)

souppres = BeautifulSoup(responsepres.content, 'xml')
#linklocs = souppres.'link:presentationLink'
linklocs = souppres.find_all('link:presentationLink')

# Find all elements with the xlink:labels attribute
elements = souppres.find_all()
#elements = souppres.find_all(attrs={'xlink:label':True})

elementDict = {}
label = ''
accessionNumber = responsepres.url.split('/')[6]
json_lib = []

# print(elements.tag.name)
for element in elements:
    # if element.name == 'link:presentationLink':
    # print(element)
    if element.name == 'presentationLink':
        # json_lib = []
        #print('___' * 20)
        # try:
        #     print(element.attrs['xlink:title'])
        # except KeyError:
        #     pass
        #print('_' * 20)
        #contents = element.content
        content_list = element.contents

        for content in content_list:
            json_str = []
            if content != '''\n''':
                # json_str = []
                # print('hello')
                try:
                    # used to print the xlink:label attribute.
                    # print(content.attrs['xlink:label'])
                    # splitting on the '_' in examples like: 'https://xbrl.sec.gov/dei/2022/dei-2022.xsd#dei_DocumentRegistrationStatement'
                    # in order to get the actual metric name to be used in subsequent tasks only pulling the name from the array
                    # print(content.attrs['xlink:href'].split('_')[1])
                    elementDict["cik_number"] = responsepres.url.split('/')[6]
                    elementDict["section"] = element.attrs['xlink:title']
                    elementDict["element"] = content.attrs['xlink:href'].split('_')[1]
                    # print(elementDict)

                    #Attempting to place this outside of the try in order to clear out the elementDict so I do not get duplicative elements.
                    # json_stuff = json.dumps(elementDict, indent=4)


                    # print(json_object)
                except KeyError:
                    pass

                json_stuff = json.dumps(elementDict, indent=4)
                #json_str.append(json_stuff)
                # elementDict = {}

                json_lib.append(json_stuff)

# print(json_lib)
#enable after figuring out how to put all of the json dictionaries together.
#de-dup list
json_lib_dedup = pd.Series(json_lib).drop_duplicates().to_list()
json_lib_str = '<root>' + str(json_lib_dedup) + '</root>'
print(json_lib_str)
# Encode/Serialize the JSON
with open("Contexts.html", "w") as html_file:
    html_file.write(str(json_lib_str))

with open("Contexts.html", "r") as html_file:
    html = html_file.read()
    jsonstr = xmltojson.parse(html)
# jsonstr = xmltojson.parse(tag_list)

# accessionNumber = i.split('/')[7]
# print(accessionNumber[7])

with open("JSONLabFile" + accessionNumber + ".json", "w") as json_file:
    json_file.write(jsonstr)

print('created: JSONLabFile' + accessionNumber + '.json')

            #print('___' * 20)
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
