from bs4 import BeautifulSoup

import requests



#url = raw_input("Enter a website to extract the URL's from: ")

r  = requests.get("http://allrecipes.com/recipe/53731/chap-chee-noodles/?internalSource=staff%20pick&referringId=86&referringContentType=recipe%20hub&clickId=cardslot%202" )

data = r.text

soup = BeautifulSoup(data)

rst=soup.find("ul", "breadcrumbs breadcrumbs").find_all('li')

final_rst= rst[len(rst)-1].text.strip()
print final_rst

#
#for link in soup.find_all('a'):
#    print(link.get('href'))
