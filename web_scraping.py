from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import re

file_links = list()
download_links = list()


def get_links(url):
    global file_links
    html = urlopen(url)
    bs_html = BeautifulSoup(html, features="html.parser")
    for link in bs_html.find_all('a', href=re.compile(".*\.pdf")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in file_links:
                new_link = link.attrs['href']
                print("[INFO]: ", new_link)
                file_links.append(new_link)
                download_links.append(url+new_link)


def get_links_1(url):
    global file_links
    html = urlopen(url)
    bs_html = BeautifulSoup(html, features="html.parser")
    for link in bs_html.find_all('a', rel="bookmark"):
        if 'href' in link.attrs and 'rel' in link.attrs and "title" in link.attrs:
            if link.attrs['href'] not in file_links:
                new_link = link.attrs['href']
                print("[INFO]: ", new_link)
                file_links.append(new_link)
                #download_links.append(url+new_link)


def download_files():
    for i, link in enumerate(download_links[:2]):
        print("[INFO]: Downloading ", link)
        urlretrieve(link, "{}.pdf".format(i))


if __name__ == '__main__':
    #get_links_1('https://www.programmer-books.com/category/software-development-languages/python-language/')
    for i in range(2, 8):
        url = 'https://www.programmer-books.com/category/software-development-languages/python-language/' + "page/{}/".format(i)
        #print(url)
        get_links_1(url)

"""    for lk in download_links[:]:
        if "python" not in lk.lower():
            download_links.remove(lk)

    download_files()"""
