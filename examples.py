from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re


pages = set()


def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title


def get_links_recursive(url):
    global pages
    html = urlopen("http://en.wikipedia.org" + url)
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id="mw-content-text").find_all_next("p")[0])
        print(bsObj.find(id="ca-edit").find_next("span").find_next("a")['href'])
    except AttributeError:
        print("This page is missing something! No worries though!")
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # We have encountered a new page
                newPage = link.attrs['href']
                print("----------------\n" + newPage)
                pages.add(newPage)
                get_links_recursive(newPage)


def print_images(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    images = bsObj.findAll("img", {"src": re.compile("\.\.\/img\/gifts/img.*\.jpg")})
    for image in images:
        print(image["src"])


def print_links(url):
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
    for link in bsObj.find("div", {"id": "bodyContent"}).find_all_next("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            print(link.attrs['href'])


if __name__ == '__main__':
    title = get_title("http://www.pythonscraping.com/pages/page1.html")
    if title == None:
        print("Title could not be found")
    else:
        print(title)