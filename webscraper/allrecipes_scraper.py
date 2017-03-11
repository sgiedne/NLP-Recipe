from bs4 import BeautifulSoup
import urllib2
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import json
import unicodedata

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
	p = re.compile('^[0-9]\s[0-9]\/[0-9]|^[0-9]\/[0-9]|^[0-9][0-9]|^[0-9]')

	for ingredient in ingredient_list:
		if(p.match(ingredient.text)):
			quantity = p.search(ingredient.text).group()
		else:
			quantity = '0'
		if(quantity!='0'):
			item = ingredient.text.split(quantity + ' ',1)[1]
		else:
			item = ingredient.text
#		item = ingredient.text.split(' ',1)[1]
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
		#ingredient is a list containing -> Quantity, Measurements[], Descriptors/Preparation[], Ingredient name
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
		ingredient_item = []
		for chunk in item_chunks:
			if(chunk[1]=='VBD' or chunk[1]=='RB'):
				prep.append(chunk[0])
				item = item.replace(chunk[0],"").replace(',','').strip()

			it = []
			if(chunk[1] in ['NN','NNS','JJ','NNP']):
				it.append(chunk[0])
			ingredient_item.append(' '.join(it))

		ingredient.append(prep)
		ingredient.append(filter(None,ingredient_item))
		ingredients.append(ingredient)

	ingredient_json = {}
	extern_count = 1
	for line in ingredients:
		intern_count = 1
		json_data = {}
		for categ in line:
			if intern_count == 1:
				json_data.update({'quantity': categ})
			elif intern_count == 2:
					json_data.update({'measures': categ})
			elif intern_count == 3:
				json_data.update({'prep': categ})
			elif intern_count == 4:
				json_data.update({'item': categ})
			intern_count+=1
		temp = {extern_count : json_data}	
		ingredient_json.update(temp)
		extern_count+=1

	for key in ingredient_json:
		print key
		print ingredient_json[key]
	return ingredient_json

getIngredients('http://allrecipes.com/recipe/22478/cheesy-vegetable-lasagna/')
print '--------------'
getIngredients('http://allrecipes.com/recipe/234312/how-to-make-focaccia/')
print '--------------'
getIngredients('http://allrecipes.com/recipe/222680/bon-appetits-meatballs')
print '--------------'
getIngredients('http://allrecipes.com/recipe/246528/stracciatella-soup/')
print '--------------'
getIngredients('http://allrecipes.com/recipe/21412/tiramisu-ii/')
print '--------------'
getIngredients('http://allrecipes.com/recipe/246866/rigatoni-alla-genovese/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/126942/ricotta-gnocchi/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/21412/tiramisu-ii/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/246628/spaghetti-cacio-e-pepe/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/246866/rigatoni-alla-genovese/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/17167/sicilian-spaghetti/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/7245/jays-signature-pizza-crust/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/23600/worlds-best-lasagna/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/8887/chicken-marsala/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/20669/double-tomato-bruschetta/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/25321/eggplant-parmesan-ii/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/70522/garlic-cheddar-chicken/')
# print '--------------'
# getIngredients('http://allrecipes.com/recipe/85389/gourmet-mushroom-risotto/')
