from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())


# Retrieves a list of all Internal links found on a page
def get_internal_links(bsObj, include_url):
    internalLinks = []
    # Finds all links that begin with a "/"
    for link in bsObj.findAll("a", href=re.compile("^(/|.*" + include_url + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks


# Retrieves a list of all external links found on a page
def get_external_links(bsObj, excludeUrl):
    externalLinks = []
    # Finds all links that start with "http" or "www" that do not contain the current URL
    for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!" + excludeUrl + ").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def split_address(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts


def get_random_external_link(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = get_external_links(bsObj, split_address(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = get_internal_links(startingPage)
        return get_external_links(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]


# Collects a list of all external URLs found on the site
allExtLinks = set()
allIntLinks = set()


def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html)
    internalLinks = get_internal_links(bsObj,split_address(siteUrl)[0])
    externalLinks = get_external_links(bsObj,split_address(siteUrl)[0])
    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)
    for link in internalLinks:
        if link not in allIntLinks:
            print("About to get link: "+link)
            allIntLinks.add(link)
            getAllExternalLinks(link)


def follow_external_only(startingSite):
    externalLink = get_random_external_link("http://oreilly.com")
    print("Random external link is: " + externalLink)
    follow_external_only(externalLink)


follow_external_only("http://oreilly.com")
