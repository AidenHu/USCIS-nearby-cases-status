import urllib2
import sys
import ssl
import bs4
import pandas as pd


def _get_content(case_number):
    url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
    num = 'appReceiptNum=' + case_number
    request = urllib2.Request(url, data=num)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    content = urllib2.urlopen(request, context=ctx)
    return content.read()


def _fetch_case_info(content):
    soup = bs4.BeautifulSoup(content, 'html.parser')
    target_div = soup.find('div', attrs={'class': 'rows text-center'})
    return target_div.find('h1').getText(), target_div.find('p').getText()

a={}
df=pd.DataFrame( columns=['Case_id', 'Status','Detail'])

def main(argv):
    global df
    case_number = argv[0:]
    content = _get_content(case_number)
    status, info = _fetch_case_info(content)
    #print('Case number: {0}\nStatus: {1}\nDetails: {2} \n'.format(case_number, status, info))
    #df_test = pd.DataFrame(case_number,status,info , index=case_number)
    #print(df_test)
    a.update({case_number:status})
    tmp=[case_number,status,info]
    df=df.append(pd.Series(tmp,index=['Case_id', 'Status','Detail']), ignore_index=True)
    


start = 'XXXXXXX'
change = 410
i=0

while i <=300:
    main(start+str(change))
    change=change+1
    i=i+1
 
df.to_csv('out.csv')
