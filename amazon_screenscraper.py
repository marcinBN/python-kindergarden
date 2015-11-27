#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import sys
from urllib.request import urlopen
from urllib.request import urlretrieve

# script takes ISBN and prints amazon ratings of given book
# 
# some ISBN examples
# "The Name of the Rose"  B003WUYPTC
# "Martin Eden"  1594562601

domains = {'USA':'com', 'UK':'co.uk', 'France':'fr', 'Germany':'de'}

def toText(d):
    with open('amazon_screenscraper_o.txt', 'w') as o:
        for country, rank in d.items():
            o.write(country+' '+rank+'\n')
        
    

def toMail(d):
    pass

def toHTML(d):
    pass

def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = '{} {}{} {} / {}'.format(percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize:
            sys.stderr.write('\n')
    else:
        sys.stderr.write('read {}\n'.format(readsofar))

def bookRank(bookISBN, country):
    bookURL = 'http://amazon.'+domains[country]+'/dp/'+bookISBN
    data = urlopen(bookURL).read()
    res = data.decode('ISO-8859-1')
    patt = r'.+'+bookISBN+r'.+?span\>(.+?) .+5'
    rank = re.findall(patt, res, re.MULTILINE)
    if len(rank) > 0:
        return(rank[0])
    else:
        return 'no result'


def main(name, bookISBN, output):
    cache = {}
    
    #progress bar - using urlretrieve
    #urlretrieve(url, 'downloaded_website.py', reporthook)
    
    for country in domains:
        rank = bookRank(bookISBN, country)
        cache[country] = rank
        print('{}: {}'.format(country, rank))

    output(cache)
    
if __name__ == '__main__':
    
    a_parm = {'text':toText, 'email':toMail, 'html':toHTML}
    parm = sys.argv
    if len(parm) < 3 or parm[2] not in a_parm:
        print('Usage: amazon_screenscraper.py [isbn] [text | email | html]')
    else:
        main(parm[0], parm[1], a_parm[parm[2]])
