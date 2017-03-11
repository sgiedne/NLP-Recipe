from bs4 import BeautifulSoup
import urllib2
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import json
import unicodedata

measurement_list = ['package','cup','cups','teaspoon','teaspoons',
						'tablespoon','tablespoons','clove','cloves','ounce',
						'ounces','liter','liters','ml','pint',
						'pints','quart','quarts','pound','pounds',
						'slice','slices','can','cans','container',
						'containers']

preparation_list = [
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

method_list = ["Amandine", "Anti-griddle", 
"Backwoods cooking", "Baghaar", "Broast", "Brown", "Boil", "Broil", "Bake", "Braise", "Barbeque", "Barbequing", "Bast",
"Cook", "Candy making", "Caramelization", "Carry over cooking", "Casserole", "Charbroiling", "Chaunk", "Cheesemaking", "Chinese cooking techniques", "Clay pot cooking", "Coddling", "Concasse", "Conche", "Confit", "Cooking with alcohol", "Creaming", "Culinary triangle", "Curdling", "Curing", "Canning", "Crush", "combination cooking",
"Deep frying", "Deglazing", "Degreasing", "Dough sheeting", "Dredging", "Dry roasting", "Drying", "Dum pukht", "Dutch oven cooking", "Drain", "dry heat",
"Earth oven", "Egg wash", "En papillote", "En vessie", "Engastration", "Engine Cooking",
"Fermentation", "Flambe", "Flattop grill", "Foam", "Food preservation", "Fondue", "Fruit preserves", "Frying",
"Gentle frying", "Glaze", "Grilling",
"Hangi", "Hibachi", "High-altitude cooking", "Homogenization", "Hot salt frying", "Huff paste",
"Indirect grilling", "Infusion",
"Jugging", "Juicing",
"Kalua", "Karaage", "Kho", "Kinpira", 
"Liquid nitrogen", "Low-temperature cooking",
"Maceration", "Marination", "Meat cooking techniques", "Microwave cooking", "Mongolian barbecue", "Mince", "moist heat",
"Nappage", "Nixtamalization",
"Outdoor cooking",
"Pan frying", "Parbaking", "Parboiling", "Pascalization", "Paste", "Pasteurization", "Pellicle", "Pickling", "Pig roast", "Poaching","Pre-ferment", "Pressure cooking", "Pressure frying", "Proofing", "Puree", "Pan frying",
"Reduction", "Rendering", "Ricing", "Rillettes", "Roasting", "Robatayaki", "Rotisserie", "Red cooking",
"Saute", "Schwenker", "Cured fish", "Searing", "Seasoning", "Separating eggs", "Shallow frying", "Shirred eggs", "Shrivelling", "Simmering", "Slow cooker", "Smoking cooking", "Smothering", "Souring", "Sous-vide", "Spatchcock", "Spherification", "Steaming", "Steeping", "Stew", "Stir frying", "Straight dough", "Stuffing", "Sugar panning", "Supreme", "Sweating", "Swissing", "Syringe", "Shaking, Squeeze",
"Tandoor", "Tataki", "Tempering", "Tenderizing", "Teriyaki", "Thermal cooking", "Thermization", "Thickening", "Transglutaminase", "Turbo cooking", "Turkey fryer",
"Vietnamese cooking techniques", "Wok cooking"]

def getRecipe(url):
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
	raw_ingredients = getRecipe(url)[0]
	direction_list = getRecipe(url)[1]
	ingredients = []
	
	for i in raw_ingredients:
		ingredient = []
		measures = []
		prep = []
		desc = []
		
		# get quantity
		if not i[0].isdigit():
			i[0] = '1'
		ingredient.append(i[0])
		item = i[1]

		#get measures
		split_word = ''
		if(p1.match(item)):
			measures.append(p1.search(item).group())
			item = item.split(p1.search(item).group())[1]

		for word in item.split():
			for measure in measurement_list:
				if(word == measure):
					measures.append(measure)
					split_word = measure
		ingredient.append(measures)
		if(split_word != ''):
			item = item.split(split_word)[1]

		# get descriptor
		item_chunks = pos_tag(word_tokenize(item))
		for chunk in item_chunks:
			if(chunk[1]=='VBD' or chunk[1]=='RB'):
				desc.append(chunk[0])
				item = item.replace(chunk[0],"").replace(',','').strip()

		# get preparation
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
					if prep_chunks[index-2][0].lower() in preparation_list:
						prep.append(prep_chunks[index-2][0])

					if prep_chunks[index-1][0].lower() in preparation_list:
						prep.append(prep_chunks[index-1][0])
		
		ingredient.append(desc)
		ingredient.append(item)
		ingredient.append(prep)
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
			intern_count+=1
		temp = {extern_count : json_data}	
		ingredient_json.update(temp)
		extern_count+=1

	# for key in ingredient_json:
	# 	print key
	# 	print ingredient_json[key]

	return ingredient_json

def getMethods(url):
	direction_list = getRecipe(url)[1]
	
	# for i in direction_list:
	# 	print i
	array = []
	
	for i in range(0, len(method_list)):
		for j in range(0, len(direction_list)):
			if method_list[i] in direction_list[j] or method_list[i].lower() in direction_list[j]:
				array.append(method_list[i])
	return array

def getTools(url):
	completeKitchenWare= []
	kitchenWareIncluded= []
	filename="kitchware.txt"
	completeKitchenWare = [line.rstrip('\r''\n') for line in open(filename)]
     
	page = urllib2.urlopen('http://allrecipes.com/recipe/lasagna-alfredo/').read()
	soup = BeautifulSoup(page,"lxml")

	direction_list = soup.findAll("span",{"class" : "recipe-directions__list--item"})

	# Create a list with all of the directions, broken down by word
	directions = []
	for direction in direction_list:
		print direction.text
		words = word_tokenize(direction.text)
		directions.append(words)

	# # Check if each word in directions_str is in the kitchenware list
	# for word in directions_str: 
	# 	if word.lower() in (tool.lower() for tool in completeKitchenWare):
	# 	    kitchenWareIncluded.append(word)

	# return kitchenWareIncluded

	# print ("The tools included in this receipt are:")
	# if len(kitchenWareIncluded) == 0:
	#     print ("none")
	# else:
	#     for kitchenWare in kitchenWareIncluded:
	#         print(kitchenWare)





def getSteps(url):
	return getRecipe(url)[1]

def getAllData(ingredients, tools, methods, steps):
	print "===== Recipe Data Representation ====="
	# print ingredients
	# print methods
	all_json = {}
	extern_count = 1

	all_json.update({'ingredients':ingredients})
	all_json.update({'methods':methods})
	all_json.update({'steps':steps})
	all_json.update({'tools':tools})
	print all_json

	print "===== Extracting methods ====="
	print all_json["methods"]
	print "===== Extracting ingredients ====="
	print all_json["ingredients"]
	print "===== Extracting steps ====="
	print all_json["steps"]
	print "===== Extracting tools ====="
	print all_json["tools"]


# getIngredients('http://allrecipes.com/recipe/22478/cheesy-vegetable-lasagna/')
ingredient_list1=getIngredients('http://allrecipes.com/recipe/lasagna-alfredo/')
method_list1=getMethods('http://allrecipes.com/recipe/lasagna-alfredo/')
step_list1=getSteps('http://allrecipes.com/recipe/lasagna-alfredo/')
tool_list1=getTools('http://allrecipes.com/recipe/lasagna-alfredo/')

getAllData(ingredient_list1, tool_list1, method_list1, step_list1)


# ingredient_list2=getIngredients('http://allrecipes.com/recipe/234312/how-to-make-focaccia/')
# ingredient_list3=getIngredients('http://allrecipes.com/recipe/222680/bon-appetits-meatballs')
# ingredient_list4=getIngredients('http://allrecipes.com/recipe/246528/stracciatella-soup/')
# # ingredient_list5=getIngredients('http://allrecipes.com/recipe/126942/ricotta-gnocchi/') #Get ingredient function error (ppp: two eggs)
# ingredient_list6=getIngredients('http://allrecipes.com/recipe/21412/tiramisu-ii/')
# ingredient_list7=getIngredients('http://allrecipes.com/recipe/246628/spaghetti-cacio-e-pepe/')
# ingredient_list8=getIngredients('http://allrecipes.com/recipe/246866/rigatoni-alla-genovese/')
# ingredient_list9=getIngredients('http://allrecipes.com/recipe/17167/sicilian-spaghetti/')
# ingredient_list10=getIngredients('http://allrecipes.com/recipe/7245/jays-signature-pizza-crust/')
# ingredient_list11=getIngredients('http://allrecipes.com/recipe/23600/worlds-best-lasagna/')
# ingredient_list12=getIngredients('http://allrecipes.com/recipe/8887/chicken-marsala/')
# ingredient_list13=getIngredients('http://allrecipes.com/recipe/20669/double-tomato-bruschetta/')
# ingredient_list14=getIngredients('http://allrecipes.com/recipe/25321/eggplant-parmesan-ii/')
# ingredient_list15=getIngredients('http://allrecipes.com/recipe/70522/garlic-cheddar-chicken/')
# ingredient_list5=getIngredients('http://allrecipes.com/recipe/85389/gourmet-mushroom-risotto/')



# check kind of the unit of main protein (5 cousine each 2 recipe)

# Egyptian Lentil Soup - 3 cups water
# Kofta - 1 pound ground beef
# Curry Pineapple Fried Rice - 1 1/2 cups uncooked white rice
# Thai Ginger Chicken (Gai Pad King) - 1 pound skinless, boneless chicken breast halves - cut into thin strips
# Fairy Bread - 8 slices white bread, with crusts trimmed
# Lamb Madras Curry - 2 1/4 pounds lamb meat, cut into 1 1/2 inch cubes
# Canadian Pork Loin Chops - 6 boneless pork loin chops, 1/2 inch thick
# Butternut Squash Soup II - 2 tablespoons butter
# Swedish Meatballs (Svenska Kottbullar) - 2/3 pound ground beef
# Italian Vegetable Soup - 2 cups water
