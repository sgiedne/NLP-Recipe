from bs4 import BeautifulSoup
import urllib2


def getrecipe(url):
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page,"lxml")

	ingredient_list = soup.findAll(itemprop="ingredients")

	ingredients = {}

	for ingredient in ingredient_list:
		quantity = ingredient.text.split(' ',1)[0]
		item = ingredient.text.split(' ',1)[1]
		ingredients[item] = quantity

	direction_list = soup.findAll("span",{"class" : "recipe-directions__list--item"})

	directions = []
	for direction in direction_list:
		directions.append(direction.text)

	recipe = []
	recipe.append(ingredients)
	recipe.append(directions)

	return recipe