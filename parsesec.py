# import our libraries
import re
import requests
import unicodedata
# import BeautifulSoup
from bs4 import BeautifulSoup

def restore_windows_1252_characters(restore_string):
    """
    Replace C1 control characters in the Unicode string s by the
    characters at the corresponding code points in Windows-1252,
    where possible.
    """

    def to_windows_1252(match):
        try:
            return bytes([ord(match.group(0))]).decode('windows-1252')
        except UnicodeDecodeError:
            # No character at the corresponding code point: remove it.
            return ''

    return re.sub(r'[\u0080-\u0099]', to_windows_1252,restore_string)


# define headers
headers = {
    'user-agent':'self m_smith627@hotmail.com'
        }

# define the url to specific html_text file
new_html_text = r"https://www.sec.gov/Archives/edgar/data/1166036/000110465904027382/0001104659-04-027382.txt"

# grab the response
response = requests.get(new_html_text)

# parse the reponse
soup = BeautifulSoup(response.content, 'lxml')
