# import all required libraries
from bs4 import BeautifulSoup
import requests
import sys
import warnings
import json
import xmltojson
warnings.filterwarnings("ignore")

# set header parameters required by sec request
User_Agent = "m_smith627@hotmail.com"
Accept_Encoding = "gzip, deflate"
Host = "www.sec.gov"

headers_txt = {
    "User-Agent" : User_Agent,
    "Accept-Encoding" : Accept_Encoding,
    "Host" : Host
}

# URLList = ['https://www.sec.gov/Archives/edgar/data/1730984/000173098423000064/0001730984-23-000064-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/6207/000141057823001494/0001410578-23-001494-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/1117228/000149315223025495/0001493152-23-025495-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/16160/000156276223000287/0001562762-23-000287-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/1862993/000110465923083813/0001104659-23-083813-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/1679273/000155837023012203/0001558370-23-012203-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/1852016/000119312523193294/0001193125-23-193294-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/1084765/000108476523000016/0001084765-23-000016-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/771856/000162828023025464/0001628280-23-025464-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/1339005/000114036123035663/0001140361-23-035663-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/1892747/000149315223025239/0001493152-23-025239-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/866729/000086672923000019/0000866729-23-000019-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/940944/000094094423000037/0000940944-23-000037-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/1622996/000164033423001347/0001640334-23-001347-index.htm',
#            'https://www.sec.gov/Archives/edgar/data/915358/000091535823000008/0000915358-23-000008-index.htm']
#
#
# for url in URLList:

# return the cik from the URL
FedURL = url
cik = FedURL.split('/')[6]
# print(URL)

# details on issuer, file type and date of document.
# cik = '' # cik for International business machines corp (IBM)
type = '10-k' # annual filing
dateb = '' # 2016

# cik = '0000051143' # cik for International business machines corp (IBM)
# type = '10-K' # annual filing
# dateb = '20231231' # 2016

# base URL for company filings search
base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&dateb={}"
format_url = base_url.format(cik, type, dateb)
# use requests .get method
edgar_resp = requests.get(base_url.format(cik, type, dateb), headers=headers_txt)
edgar_str = edgar_resp.text
# print(f'BASE URL : {format_url}')
# print(f'EDGAR STR URL : {edgar_str}')
doc_link = ''
soup = BeautifulSoup(edgar_str, 'html.parser')
table_tag = soup.find('table', class_='tableFile2')
rows = table_tag.find_all('tr')

# print(table_tag)
print ("done")

doc_link_list = []

for row in rows :
    cells = row.find_all('td')
    if len(cells) > 3 :
        if cells[3].text > '2015-01-01':
        #if '10-k' in cells[1].text :
            doc_link = 'https://www.sec.gov' + cells[1].a['href']
            doc_link_list.append(doc_link)
print(doc_link_list)

# filingURL = 'https://www.sec.gov/Archives/edgar/data/1730346/000173034623000030/0001730346-23-000030-index.htm'
#              https://www.sec.gov/Archives/edgar/data/1886591/000119312523193225/0001193125-23-193225-index.htm
# doc_link = filingURL

# Exit if document link couldn't be found
if doc_link == '' :
    print("Couldn't find the document link")
    sys.exit()


for i in doc_link_list:

    # Obtain HTML for document page
    print(f'DOC Link : {i}')
    doc_resp = requests.get(i, headers=headers_txt)
    doc_str = doc_resp.text

    # Find the XBRL link
    xbrl_link = ''
    soup = BeautifulSoup(doc_str, 'html.parser')
    # skip the processing if the company has not filed the xbrl data files
    if soup.find('table', class_='tableFile', summary='Data Files') != None:
        table_tag = soup.find('table', class_='tableFile', summary='Data Files')
        rows = table_tag.find_all('tr')
    else:
        print('Passing: ' + i)
        pass

    for row in rows :
        cells = row.find_all('td')
        if len(cells) > 3:
            if 'INS' in cells[1].text:
                xbrl_link = 'https://www.sec.gov' + cells[2].a['href']
                print(xbrl_link)



    # Obtain XBRL text from document
    print(f'XBRL Link : {xbrl_link}')
    xbrl_resp = requests.get(xbrl_link, headers=headers_txt)
    xbrl_str = xbrl_resp.text


    # Find and print stockholder's equity
    soup = BeautifulSoup(xbrl_str, 'lxml')
    if soup.find_all(name='xbrli:context').__len__() > 0:
        # process context tags pre-2016
        tag_list = soup.find_all(name='xbrli:context')
    else:
        # process context tags 2016 and greater
        tag_list = soup.find_all(name='context')

    # print(xbrl_str)
    # json = json.loads(xbrl_str)
    # print(json)

# This section of code creates a context table.
# The context table is a dictionary of context names keys that reference dictionary values
# containing date information for each context. For contexts with datetype of 'period' the table
# contains the start and end date. For contexts with datetype of 'instant' the context
# contains the instant date of the context. All entries include a date and dateType value.
# For contexts with datetype of period, the date is equal to the enddate of the context.

    contexts = {}
    # Concatenate json with root tag to
    tag_list_root = '<root>' + str(tag_list) + '</root>'


    #
    with open("Contexts.html", "w") as html_file:
        html_file.write(str(tag_list_root))

    with open("Contexts.html", "r") as html_file:
        html = html_file.read()
        jsonstr = xmltojson.parse(html)
    # jsonstr = xmltojson.parse(tag_list)

    accessionNumber = i.split('/')[7]
    # print(accessionNumber[7])

    with open("JSONFile" + accessionNumber + ".json", "w") as json_file:
        json_file.write(jsonstr)

    print('created: JSONFile' + accessionNumber + '.json')


    # print(jsonstr)

    for tag in tag_list:
        if 'xbrli' in tag.name or 'context' in tag.name:
        # if tag.name == 'xbrli:context' or tag.name =='context':



            # This section of code finds the start date of the context if it exists.
            start_date_tag = tag.find(name='xbrli:startdate') or tag.find(name='period')
            if start_date_tag == None :
                start_date = 'None'
            else :
                start_date = start_date_tag.text

            # This section of code finds the end date of the context if it exists.
            end_date_tag = tag.find(name='xbrli:enddate')
            if end_date_tag == None :
                end_date = None
                date = 'None'
                datetype = 'None'
            else :
                end_date = end_date_tag.text
                date = end_date_tag.text
                datetype = 'period'

            # This section of code finds the instant date of the context if it exists.
            instant_date_tag = tag.find(name='xbrli:instant') or tag.find(name='instant')
            if instant_date_tag != None :
                date = instant_date_tag.text
                datetype = 'instant'

            # build a dictionary of date information within a dictionary of context titles
            dtinfo = {'date' : date, 'year' : date[0 :4], 'datetype' : datetype, 'startdate' : start_date,
                    'enddate' : end_date}

            if tag.find(name='xbrli:entity'):
                try:
                    contexts[tag.attrs['id']] = dtinfo;
                    tag_attrs_id=tag.attrs['id'];
                    # print(f'tag_attrs[id] : {tag_attrs_id}')
                except KeyError:
                    pass
                except NameError:
                    pass

                    # print(f'tag_attrs[id] : {tag_attrs_id}')

    # Find and print stockholder's equity
    for tag in tag_list :
        if tag.name == 'us-gaap:stockholdersequity' :
            try:
                year = contexts[tag.attrs['contextref']]['year']
                contextref_txt=tag.attrs['contextref']
                # print(f'tag_attrs[contextref] : {contextref_txt}')
                context_out=contexts[tag.attrs['contextref']]
                # print(f'contexts[tag.attrs[contextref] : {context_out}')
                # print(year + " Stockholder's equity: " + tag.text)
            except KeyError:
                pass
