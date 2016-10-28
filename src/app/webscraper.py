#!/usr/bin/python3

import sys, re
from bs4 import BeautifulSoup
import urllib

base_html = 'http://www.top8draft.com'
draft_number = 0
# cleans up links from hrefs array
def clean_link(href):
    return base_html + href['href']

# link to draft log which contains the dl link
def open_link_to_bot_draft(href):
    global draft_number

    draft_page = urllib.urlopen(href).read()
    soup = BeautifulSoup(draft_page, 'lxml')
    dl_link = soup.find('a', {'class': 'btn-primary'})
    to_dl = clean_link(dl_link)
    urllib.urlretrieve(to_dl, './scraped_drafts/draft_' + str(draft_number))
    draft_number += 1

# opens links to drafts
def open_link_to_draft(href):
    draft_page = urllib.urlopen(href).read()
    soup = BeautifulSoup(draft_page, 'lxml')
    links_to_bots_draft = soup.find_all('table')[0].find_all('a', href=True, text=re.compile('Bot*'))
    for link in links_to_bots_draft:
        clean_href = clean_link(link)
        open_link_to_bot_draft(clean_href)


def main():
    webpage = urllib.urlopen(base_html).read()
    soup = BeautifulSoup(webpage, 'lxml')
    lis = soup.find('div', {'id': 'drafts'}).find_all('li')
    #print lis
    hrefs = []
    for li in lis:
        hrefs.append(li.find('a', href=True))

    for href in hrefs:
        clean_href = clean_link(href)
        open_link_to_draft(clean_href)

if __name__ == '__main__':
    main()
