from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import time


def find_all_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--ignore-certificate-errors")
    scraper_driver = webdriver.Chrome(options=options)
    scraper_driver.get(url)
    all_html = scraper_driver.page_source
    scraper_driver.quit()
    return all_html


def parse_html(all_html):
    my_soup_object = BeautifulSoup(all_html, "html.parser")
    return my_soup_object


def get_title(soup):
    if soup.title:
        return soup.title.get_text(strip=True)
    else:
        return "title is not available"


def get_body_text(soup):
    for tag in soup(["style", "script", "noscript"]):
        tag.decompose()

    main_content = soup.find("main")
    if main_content:
        text = main_content.get_text(separator="\n", strip=True)
    else:
        text = soup.body.get_text(separator="\n", strip=True)

    return text




def get_all_links(soup, base_url):

    links = set()
    anchor_tags = soup.find_all("a")
    for tag in anchor_tags:

        href = tag.get("href")

        if href == None:
            continue

        full_url = urljoin(base_url, href)
        if full_url.startswith("http://"):
            links.add(full_url)

        elif full_url.startswith("https://"):
            links.add(full_url)

    return links




    
url = sys.argv[1]

if not url[0:4]=="http":
    url = "https://" + url

print("Extracting all html..")
all_html = find_all_html(url) 
my_soup_object = parse_html(all_html)
title = get_title(my_soup_object) 
body = get_body_text(my_soup_object)
outlinks = get_all_links(my_soup_object, url)

print("title:")
print(title)
time.sleep(2)
print("\nBody Text:")
print(body)
time.sleep(2)
print("\nOutlinks:")
for link in outlinks:
    print(link)

