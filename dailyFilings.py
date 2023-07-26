import bs4
from bs4 import BeautifulSoup
import requests
import sys

# set header parameters required by sec request
user_Agent = r"m_smith627@hotmail.com"
accept_Encoding = r"gzip, deflate"
host = r"www.sec.gov"
baseURL = r"https://www.sec.gov"
extension = r"/cgi-bin/browse-edgar"
# Params to get the latest company filings
params = {'Company': '',
          'CIK': '',
          'type': '10-k',
          'owner': 'include',
          'count': '100',
          'action': 'getcurrent'}

headers_txt = {
    "User-Agent": user_Agent,
    "Accept-Encoding": accept_Encoding,
    "Host": host
}

url = baseURL + extension
print(url)

# response = requests.get(url='https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent',headers=headers_txt, params=params)
response = requests.get(url=url, headers=headers_txt, params=params)

html = response.text

soup = BeautifulSoup(html, 'html.parser')

tableTags = soup.find_all('table')
# rows = tableTags.find_all('tr')
# cells = soup.find_all('td')

forms = soup.find_all('form')

# for form in forms:
#     if form.contents.__len__() > 0:
#         if form.attrs['type'] == "button":
#             print(forms)

# print(forms)
# print(soup)
# print(tableTags)
# print(tableTags[6])

def get_xbrlList():

    xbrlList = []

    for table_tag in tableTags:
        headers = table_tag.parent.find_all('th')
        if table_tag != None:
            if headers != None:
                rows = table_tag.find_all('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) > 3:
                        if cells[1].contents[0] is not None:
                            # print(cells[1].contents[0].contents[0]
                            try:
                                # print(cells[1].contents[0].attrs['href'])
                                if 'html' in cells[1].contents[0].text:  # attrs['href']:
                                    xbrlList.append(baseURL + cells[1].contents[0].attrs['href']);
                            except KeyError:
                                pass
                            except AttributeError:
                                pass
        else:
            print('There are None')
    # print(xbrlList)



    return xbrlList


# print(response.text)
# print(forms)
print("done")
