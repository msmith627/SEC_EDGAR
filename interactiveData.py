import requests
import js2py


# set header parameters required by sec request
user_Agent = "m_smith627@hotmail.com"
accept_Encoding = "gzip, deflate"
host = "www.sec.gov"
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


baseURL = r'https://www.sec.gov'

extension = r'/cgi-bin/viewer?action=view&amp;cik=1368622&amp;accession_number=0001558370-23-015110&amp;xbrl_type=v'

url = baseURL + extension

apicall = requests.get(url=url, headers=headers_txt)

# f = js2py.eval_js(apicall.text)
f = apicall.text# .find()
# find the script and use the eval_js on that.
print(f)
