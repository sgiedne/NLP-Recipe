from bs4 import BeautifulSoup
import urllib2
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

common_meausurements = ['package','cup','cups','teaspoon','teaspoons',
						'tablespoon','tablespoons','clove','cloves','ounce',
						'ounces','liter','liters','ml','pint',
						'pints','quart','quarts','pound','pounds',
						'slice','slices','can','cans','container',
						'containers']

def getrecipe(url):
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page,"lxml")

	ingredient_list = soup.findAll(itemprop="ingredients")

	ingredients = []

	for ingredient in ingredient_list:
		quantity = ingredient.text.split(' ',1)[0]
		item = ingredient.text.split(' ',1)[1]
		temp  = []
		temp.append(quantity)
		temp.append(item)
		ingredients.append(temp)

	direction_list = soup.findAll("span",{"class" : "recipe-directions__list--item"})

	directions = []
	for direction in direction_list:
		directions.append(direction.text)

	recipe = []
	recipe.append(ingredients)
	recipe.append(directions)

	return recipe

def getIngredients(url):

	p1 = re.compile('\([0-9]* ounce(|s)\)')
	raw_ingredients = getrecipe(url)[0]
	ingredients = []
	for i in raw_ingredients:
		#ingredient is a list containing -> Quantity, Measurements, Descriptors/Preparation, Ingredient name
		ingredient = []
		measures = []
		prep = []

		#get quantity
		ingredient.append(i[0])
		
		item = i[1]

		#get measures
		split_word = ''
		if(p1.match(item)):
			measures.append(p1.search(item).group())
			item = item.split(p1.search(item).group())[1]

		for word in item.split():
			for measure in common_meausurements:
				if(word == measure):
					measures.append(measure)
					split_word = measure
		ingredient.append(measures)
		if(split_word != ''):
			item = item.split(split_word)[1]

		#get descriptors/preparation
		item_chunks = pos_tag(word_tokenize(item))
		for chunk in item_chunks:
			if(chunk[1]=='VBD' or chunk[1]=='RB'):
				prep.append(chunk[0])
				item = item.replace(chunk[0],"").replace(',','').strip()
		ingredient.append(prep)
		ingredient.append(item)
		ingredients.append(ingredient)

	for i in ingredients:
		print i

getIngredients('http://allrecipes.com/recipe/22478/cheesy-vegetable-lasagna/')