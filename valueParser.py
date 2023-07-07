import attrs
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json


url = 'https://www.sec.gov/Archives/edgar/data/1722731/000149315223015479/form10-ka_htm.xml'

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

response = requests.get(url=url, headers=headers)

soup = BeautifulSoup(response.content, 'xml')

#print(response.url)
#print(response.text)

links = soup.find_all()

#print(links)

for link in links:
    #if link.attrs['xlink:title']
    #print(link.prefix)
    #print(link.name)
    if link.prefix == 'us-gaap':# and link.name == 'Assets':
        # print(link.value)
        # print(link.name)
        # print(link.attrs)
        #https: // xbrl.fasb.org / us - gaap / 2022 / elts / us - gaap - 2022.xsd  # us-gaap_CommonStockSharesOutstanding
        try:
            if link.attrs['unitRef'] == 'USD':
                if link.contents.__len__() > 0:
                    # print(link.contents[0])
                    # Append the value as a key:value pair to the attrs dictionary
                    link.attrs['value']=link.contents[0]
                    link.attrs['metric']=link.name
                    json_object = json.dumps(link.attrs, indent=4)
                    print(json_object)
                    # Print out the attrs dictionary after appending the
                    print(link.attrs)
                else:
                    link.attrs['value'] = 0
                    link.attrs['metric'] = link.name
                    # Print out the attrs dictionary after appending the
                    json_object = json.dumps(link.attrs, indent=4)
                    print(json_object)
                    print(link.attrs)
                    # print(0)
        except KeyError:
            pass

    #if link.value = 'loc_us:gaapLiabilities'