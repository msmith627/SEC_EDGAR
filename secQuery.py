import sec_api
from sec_api import QueryApi
from sec_api import FullTextSearchApi
from bs4 import BeautifulSoup


api_key = '6a381a7422c427a2db61446a8b926bf8ed358969e39563e90e0ef98cde6da36c'


queryApi = QueryApi(api_key=api_key)

query = {
  "query": { "query_string": {
      "query": "ticker:MSFT AND filedAt:{2022-01-01 TO 2022-12-31} AND formType:\"10-K\""
    } },
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)

print(filings)

print("-" * 160)

query = {
  "query": { "query_string": {
      "query": "formType:\"8-K\" AND description:\"9.01\""
    } },
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

filings = queryApi.get_filings(query)

print(filings)

print("-" * 160)


fullTextSearchApi = FullTextSearchApi(api_key=api_key)

query = {
  "query": '"LPCN"',
  "formTypes": ['10-K', '10-Q'],
  "startDate": '2021-01-01',
  "endDate": '2021-06-14',
}

filings = fullTextSearchApi.get_filings(query)

print(filings)

soup = BeautifulSoup(filings, 'lxml')



list(soup.children)