from bs4 import BeautifulSoup
import urllib2

page = urllib2.urlopen('http://allrecipes.com/recipe/lasagna-alfredo/').read()
soup = BeautifulSoup(page,"lxml")

ingredient_list = soup.findAll(itemprop="ingredients")

ingredients = {}

for ingredient in ingredient_list:
	#print ingredient
	quantity = ingredient.text.split(' ',1)[0]
	#print quantity 
	item = ingredient.text.split(' ',1)[1]
	# i = []
	# i.append(quantity)
	# i.append(item)
	ingredients[item] = quantity

for ingredient in ingredients:
	print ingredients[ingredient], ingredient

direction_list = soup.findAll("span",{"class" : "recipe-directions__list--item"})

print "\n"
directions = []
for direction in direction_list:
	directions.append(direction.text)

for d in directions:
	print d