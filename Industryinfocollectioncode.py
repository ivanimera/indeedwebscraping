# coding: utf-8

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from time import sleep
import csv

f = open('companyname.txt','r')
companylist = f.read()
thelist=[]
thelist=companylist.split('\n')

mycsv = csv.writer(open("company industry.csv", 'w'))

theresultlist=[]
for cname in thelist:
    mylist = cname.split(' ')
    companysearchname = '+'.join(mylist)

    indeedcomp ="https://www.indeed.com/cmp?from=search&q=%s" % companysearchname

    try:

        content = BeautifulSoup(urlopen(indeedcomp), 'html.parser')
        for row in content.find_all('div', attrs={"cmp-company-tile-content"}):
            if row == None:
                theresultlist.append("?")
            else:
                c = list(row)
                if c:
                    d = c[-1]
                    e = str(d)
                    e = e.replace("</div>", "")
                    e = e.replace("<div>", "")
                    if len(e)<=50:
                        # print(e)
                        print(cname)
                        theresultlist.append(cname)
                        print(e)
                        theresultlist.append(e)
                        mycsv.writerow(theresultlist)
                        theresultlist=[]
    except:
        pass
