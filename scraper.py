import re
import sys
from bs4 import BeautifulSoup
import requests
def scrap_page(url):
    content=requests.get(url)
    parser=BeautifulSoup(content.text,"html.parser")

    # Fetching title of the page 
    if parser.title:
        print("Title of the page:")
        print(parser.title.string)
    else:
        print("Title is not found")
    
    # Fetching body content of the page 
    if parser.body:
        print("Body content of the page:")
        body_text=(parser.body.get_text(separator=" ",strip=True))
        print(body_text)
    else:
        print("body not found")

    # Fetching all link of the page points link to
    if parser.a:
        print("Getting all url:")
        for links in parser.find_all('a'):
            href=links.get('href')
            if href:
                print(href)
    else:
        print("No link is pointing to this page")

url=sys.argv[1]
scrap_page(url)

    
    