from bs4 import BeautifulSoup
from urllib.request import urlopen




completeKitchenWare= []
kitchenWareIncluded= []
filename="kitchware.txt"

############ For TXT without the newline character####
##with open("kitchware.txt") as f:
##     completeKitchenWare= f.readlines()

completeKitchenWare = [line.rstrip('\n') for line in open(filename)]

     
page = urlopen('http://allrecipes.com/recipe/lasagna-alfredo/').read()
soup = BeautifulSoup(page,"lxml")


def getrecipe(url):
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page,"lxml")

	ingredient_list = soup.findAll(itemprop="ingredients")

ingredients = {}


for ingredient in ingredients:
	print (ingredients[ingredient], ingredient)

	for ingredient in ingredient_list:
		quantity = ingredient.text.split(' ',1)[0]
		item = ingredient.text.split(' ',1)[1]
		ingredients[item] = quantity


direction_list = soup.findAll("span",{"class" : "recipe-directions__list--item"})


print ("\n")
directions = []
for direction in direction_list:
	directions.append(direction.text)

##for d in directions:
##	print (d)



     
for direction in directions:      
   for kitchenWare in completeKitchenWare:              
        if kitchenWare.lower() in direction.lower():
                     #print("true")
                     kitchenWareIncluded.append(kitchenWare)
      

print ("The tool included in this receipt are:")
if len(kitchenWareIncluded) ==0:
        print ("none")
#print(kitchenWareIncluded)
else:
        for kitchenWare in kitchenWareIncluded:
                print(kitchenWare)


