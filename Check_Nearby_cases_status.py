import urllib.request
import urllib.parse
import sys
import ssl
import bs4
import pandas as pd


def _get_content(case_number):
    url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
    values = {'appReceiptNum': case_number}
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    request = urllib.request.Request(url, data)
    with urllib.request.urlopen(request) as response:
        the_page = response.read()

    return the_page
    
##    num = 'appReceiptNum=' + case_number
##    request = urllib.request.Request(url, data=urllib.parse.urlencode(num))
##    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
##    content = urllib.request.urlopen(request, context=ctx)
##    return content.read()


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
    


start = 'WAC1720550'
change = 545
i=0

while i <= 400:
    main(start+str(change))
    change=change+1
    i=i+1
 
df.to_csv('out.csv')
