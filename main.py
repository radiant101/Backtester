from bs4 import BeautifulSoup
import requests


#function for getting headline
def get_headlines(url,tag):
        response=requests.get(url)
        print("the response code is:",response.status_code)
        if response.status_code==200:
          soup=BeautifulSoup(response.content,'html.parser')
          headlines=soup.find_all(tag)
          return [headline.text.strip() for headline in headlines]
        else:
             return[]
    
#list of sites
sites=[
      {'url' : 'https://www.livemint.com/', 'tag' : 'h2'},
      {'url' : 'https://www.livemint.com/', 'tag' : 'h3'}
]

for site in sites:
     headlines=get_headlines(site['url'],site['tag'])
     print(f"Headlines from {site['url']} with tag {site['tag']}:\n")
     for headline in headlines:
         print(headline, "\n")
