'''
Notes from Eureka:
-measurements spelled incorrectly in "common_meausurements"
'''

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

prep_list = [
	"acidic", "aromatic", 
	"bitter", "bland", "blended", "browned", "burnt", "buttery", "baked", "blazed", "boiled", 
	"chalky", "cheesy", "chewy", "chocolaty", "cinnamony", "citrusy", "cool", "creamy", "crispy", "crumbly", "crunchy", "crusty", "caked", "candied",
	"caramelized", "char-boiled", "cheesy", "chilled", "chunked", "classy", "cold", "crafted", "creamed", "cured", 
	"doughy", "dry", "dull", "deep-fried", "dressed", "drizzled", 
	"earthy", "eggy", "encrusted", 
	"fatty", "fiery", "fishy", "fizzy", "flaky", "flat", "flavourful", "flavourless", "fleshy", "fluffy", "fruity", "furry", "fetid",
	"flavored", "fresh", "freshly", "fine", "finely", "frosty", "frosted", 
	"garlicky", "gelatinous", "grainy", "greasy", "golden", "gooey", "gritty", "gingery", "glazed", "grilled", "gustatory", 
	"hearty", "heavy", "honeyed", "hot", "half", "harsh", "honeyed", "honey-glazed", "hot", "heat", "heated", 
	"icy", "intense", "ice-cold", "incisive", "infused", 
	"juicy", "jumbo", 
	"light", "leathery", "lemony", "lukewarm", "layered", "large", "lavish", "lean", "lemon-less", "lightly", "lively", "low", "luscious", "lush",  
	"meaty", "mashed", "mild", "milky", "minty", "moist", "mushy", "marinated", "mellow", "minty", "moist", "moisted", "melt", "melted", 
	"nutmeggy", "nutty", 
	"oily", "oniony", "overpowering", "organic", 
	"peppery", "pickled", "plain", "pleasant", "powdery", "pulpy", "pureed", "piquant", "pounded", "prickly", 
	"rancid", "rank", "raw", "refreshing", "rich", "ripe", "roasted", "rotten", "rubbery", "runny", "refresh", 
	"salty", "satiny", "savoury", "seasoned", "sharp", "silky", "sizzling", "slimy", "smelly", "smoky", "smooth", "soggy", "sour", "spicy",
	"spongy", "stale", "sticky", "stinging", "stringy", "strong", "succulent", "sugary", "sweet", "sour", "syrupy", "saporous", "satin", 
	"sauteed", "silky", "simmered", "sizzling", "small", "smoked", "soothing", "spiced", "spiral-cut", "spongy", "sprinkled", "steamed",
	"sticky", "sugary", "sugarless", "syrupy", "spread", "salted", 
	"tangy", "tantalizing", "tart", "tasteless", "tasty", "tepid", "toasted", "tough", "thick", "thin", "toothsome", "topped", "tossed", "tough", "treacly", "treat", 
	"unflavored", "unsavory", "unseasoned", 
	"vanillary", "velvety", "vinegary", 
	"warm", "watery", "waxy", "whipped", "woody", 
	"yeasty", 
	"zesty", "zingy"
]

protein_list = [
	"anchovy", "anchovies",
	"beef",
	"chicken", 
	"duck", 
	"egg", "eggs", 
	"fillet", "fish", 
	"mussels"
	"lamb", 
	"oyster", "oysters",
	"pigeon", "pork", "prawn", "prawns",
	"rabbit", "rib", "ribs"
	"salmon", "sardine", "sardines", "sausage", "shrimp", "shrimps",
	"trout", "tuna", "turkey", 
	"veal", "venison"   
]

herb_list = [
	"basil", "bay",
	"cayenne", "chives", "cilantro", "coriander",
	"fennel",
	"marjoram",
	"nutmeg",
	"oregano", 
	"paprika", "parsley", "pepper",
	"rosemary",
	"thyme"
]

sauce_list = [
	"cheese", 
	"paste"
]

cooked_carb_list = [
	"lasagna",
	"noodles",
	"pasta",
	"rice", "rigatoni", 
	"spaghetti", 
	"vermicelli"
]


state_list = ["broth", "soup"]


def getrecipe(url):
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page,"lxml")

	ingredient_list = soup.findAll(itemprop="ingredients")

	ingredients = []

	for ingredient in ingredient_list:
		quantity = ingredient.text.split(' ',1)[0]
		item = ingredient.text.split(' ',1)[1]
		temp = []
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

	# added
	direction_list = getrecipe(url)[1]


	
	for i in raw_ingredients:
		#ingredient is a list containing -> Quantity, Measurements[], Descriptors/Preparation[], Ingredient name
		ingredient = []
		measures = []
		prep = []
		desc = []
		type_ingredient = []
		
		
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
				desc.append(chunk[0])
				item = item.replace(chunk[0],"").replace(',','').strip()

		# added
		item = item.lstrip(' ');
		item2 = word_tokenize(item)
		for j in direction_list:
			if item in j:
				# desc_list = []
				index = 0;
				selected = 0;
				prep_chunks = pos_tag(word_tokenize(j))

				for d in prep_chunks:
					if d[0].lower() == item2[0].lower():
						selected = index
						break
					index = index + 1	

				if selected > 0:
					if prep_chunks[index-2][0].lower() in prep_list:
						prep.append(prep_chunks[index-2][0])

					if prep_chunks[index-1][0].lower() in prep_list:
						prep.append(prep_chunks[index-1][0])
		
		#Check what type of ingredient it is
		is_protein = False
		is_herb = False
		is_sauce = False
		is_cooked_carb = False
		words = word_tokenize(item)
		for word in words:
			if word.lower() in protein_list:
				is_protein = True
			if word.lower() in herb_list:
				is_herb = True
			if word.lower() in sauce_list:
				is_sauce = True
			if word.lower() in cooked_carb_list:
				is_cooked_carb = True
		if is_protein:
			type_ingredient.append("protein")
		elif is_herb:
			type_ingredient.append("herb")
		elif is_sauce:
			type_ingredient.append("sauce")
		elif is_cooked_carb:
			type_ingredient.append("cooked_carb")
		else:
			type_ingredient.append("other")
					
		ingredient.append(desc)
		ingredient.append(item)
		ingredient.append(prep)
		ingredient.append(type_ingredient)
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
				json_data.update({'desc': categ})
			elif intern_count == 4:
				json_data.update({'item': categ})
			elif intern_count == 5:
				json_data.update({'prep': categ})
			elif intern_count == 6:
				json_data.update({'type of ingredient': categ})
			intern_count+=1
		temp = {extern_count : json_data}	
		ingredient_json.update(temp)
		extern_count+=1

	for key in ingredient_json:
		print key
		print ingredient_json[key]

	return ingredient_json

# getIngredients('http://allrecipes.com/recipe/22478/cheesy-vegetable-lasagna/')
# ingredient_list1=getIngredients('http://allrecipes.com/recipe/lasagna-alfredo/')
ingredient_list2=getIngredients('http://allrecipes.com/recipe/234312/how-to-make-focaccia/')
ingredient_list3=getIngredients('http://allrecipes.com/recipe/222680/bon-appetits-meatballs')
ingredient_list4=getIngredients('http://allrecipes.com/recipe/246528/stracciatella-soup/')
#ingredient_list5=getIngredients('http://allrecipes.com/recipe/126942/ricotta-gnocchi/') Get ingredient function error (ppp: two eggs)
ingredient_list6=getIngredients('http://allrecipes.com/recipe/21412/tiramisu-ii/')
ingredient_list7=getIngredients('http://allrecipes.com/recipe/246628/spaghetti-cacio-e-pepe/')
ingredient_list8=getIngredients('http://allrecipes.com/recipe/246866/rigatoni-alla-genovese/')
ingredient_list9=getIngredients('http://allrecipes.com/recipe/17167/sicilian-spaghetti/')
ingredient_list10=getIngredients('http://allrecipes.com/recipe/7245/jays-signature-pizza-crust/')
ingredient_list11=getIngredients('http://allrecipes.com/recipe/23600/worlds-best-lasagna/')
ingredient_list12=getIngredients('http://allrecipes.com/recipe/8887/chicken-marsala/')
ingredient_list13=getIngredients('http://allrecipes.com/recipe/20669/double-tomato-bruschetta/')
ingredient_list14=getIngredients('http://allrecipes.com/recipe/25321/eggplant-parmesan-ii/')
ingredient_list15=getIngredients('http://allrecipes.com/recipe/70522/garlic-cheddar-chicken/')
ingredient_list5=getIngredients('http://allrecipes.com/recipe/85389/gourmet-mushroom-risotto/')
