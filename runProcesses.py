
# Lookup Daily 10-k filings
with open("dailyFilings.py") as a:
    exec (a.read())
    # urls = a.read()

print('--' * 20)

with open("xBRLParser.py") as b:
    for url in xbrlList:
        exec (b.read())
        print(url)
# print(a.read())
