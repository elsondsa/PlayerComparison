from urllib.request import Request, urlopen
import urllib.parse, urllib.error
import ssl
from bs4 import BeautifulSoup






def retrieve_player_data(player):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    params = dict()
    query = player+ ' stats cricbuzz'

    params['q'] = query

    print(query)

    serviceurl = 'http://www.google.com/search?'

    url = serviceurl + urllib.parse.urlencode(params)

    print(url)

    uh = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    uhl = urlopen(uh, context=ctx)
    data = uhl.read().decode()
    soup = BeautifulSoup(data, 'html.parser')

    tags = soup('a')

    for i in range(0,len(tags)):
        target = tags[i].get('href', None)
        a = target.find('cricbuzz.com/profiles')
        if a!=-1:
            break

    url = 'http://www.google.com'+target

    print(url)
    
    uh = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    uhl = urlopen(uh, context=ctx)
    data = uhl.read().decode()
    soup = BeautifulSoup(data, 'html.parser')

    
    tablediv = soup.findAll('table',{'class':'cb-plyr-thead'})

    
    action = ['batting','bowling']
    data = {}
    divis = -1
    for table in tablediv:
        divis = divis + 1
        headings=table.find_all('th')[1:]
        allformat = table.find_all('tr')
        teststr = allformat[1].find_all('td')[1:]
        odistr = allformat[2].find_all('td')[1:]
        t20str = allformat[3].find_all('td')[1:]
        iplstr = allformat[4].find_all('td')[1:]
        testjson = {}
        odijson = {}
        t20json = {}
        ipljson = {}
        for test in range(0,len(teststr)):
            testjson[headings[test].text]=teststr[test].text
        for odi in range(0,len(odistr)):
            odijson[headings[odi].text]=odistr[odi].text
        for t20 in range(0,len(t20str)):
            t20json[headings[t20].text]=t20str[t20].text
        for ipl in range(0,len(iplstr)):
            ipljson[headings[ipl].text]=iplstr[ipl].text
        datasmall={}
        datasmall['test']=testjson
        datasmall['odi']=odijson
        datasmall['t20']=t20json
        datasmall['ipl']=ipljson
        data[action[divis]]=datasmall
    return data


player1 =input('Enter player1')
player2 = input('Enter player2')
data1 = retrieve_player_data(player1)            
data2 = retrieve_player_data(player2)

print("Batting stats\n")

for format in data1['batting']:
    print(format,"\n")
    for atts in data1['batting'][format]:
        print(atts,":")
        print(data1['batting'][format][atts],":::",data2['batting'][format][atts])
    print("\n\n\n")

for format in data1['bowling']:
    print(format,"\n")
    for atts in data1['bowling'][format]:
        print(atts,":")
        print(data1['bowling'][format][atts],":::",data2['bowling'][format][atts])
    print("\n\n\n")
