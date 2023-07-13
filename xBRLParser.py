# import all required libraries
from bs4 import BeautifulSoup
import requests
import sys
import warnings
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

# details on issuer, file type and date of document.
cik = '0000051143' # cik for International business machines corp (IBM)
type = '10-K' # annual filing
dateb = '20231231' # 2016

# base URL for company filings search
base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&dateb={}"
format_url = base_url.format(cik, type, dateb)
# use requests .get method
edgar_resp = requests.get(base_url.format(cik, type, dateb), headers=headers_txt)
edgar_str = edgar_resp.text
print(f'BASE URL : {format_url}')
print(f'EDGAR STR URL : {edgar_str}')
doc_link = ''
soup = BeautifulSoup(edgar_str, 'html.parser')
table_tag = soup.find('table', class_='tableFile2')
rows = table_tag.find_all('tr')

print(table_tag)
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
    table_tag = soup.find('table', class_='tableFile', summary='Data Files')
    rows = table_tag.find_all('tr')
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
    tag_list = soup.find_all(name='xbrli:context')

# This section of code creates a context table.
# The context table is a dictionary of context names keys that reference dictionary values
# containing date information for each context. For contexts with datetype of 'period' the table
# contains the start and end date. For contexts with datetype of 'instant' the context
# contains the instant date of the context. All entries include a date and dateType value.
# For contexts with datetype of period, the date is equal to the enddate of the context.

    contexts = {}

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

            if tag.find(name='xbrli:context'):
                try:
                    contexts[tag.attrs['id']] = dtinfo;
                    tag_attrs_id=tag.attrs['id'];
                    print(f'tag_attrs[id] : {tag_attrs_id}')
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
                print(f'tag_attrs[contextref] : {contextref_txt}')
                context_out=contexts[tag.attrs['contextref']]
                print(f'contexts[tag.attrs[contextref] : {context_out}')
                print(year + " Stockholder's equity: " + tag.text)
            except KeyError:
                pass
