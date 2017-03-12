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

tool_list = [
'Air fryer', 'Angel food cake pan', 'Apple corer', 'Apple cutter', 
'Bachelor griller', 'Baking pan', 'Balloon whisk', 'Barbecue grill', 'Barbecue', 'Basket skimmer', 'Baster', 'Basting brush', 'Beanpot', 'Beehive oven', 
'Bell whisk', 'Bench knife', 'Bench scraper', 'Biscuit cutter', 'Biscuit mould', 'Biscuit press', 'Blow torch', 'Blowlamp', 'Blowtorch', 'Boil over preventer', 
'Bottle opener', 'Bowl', 'Brasero', 'Brazier', 'Bread knife', 'Bread machine', 'Brown Bobby', 'Browning bowl', 'Browning plate', 'Browning tray', 
'Bundt cake pan', 'Burjiko', 'Burr grinder', 'Burr mill', 'Butane torch', 'Butcher\'s twine', 'Butter curler', 
'Cake and pie server', 'Cake shovel', 'Can opener', 'Candy thermometer', 'Cheese grater', 'Cheese knife', 'Cheesecloth', 'Cheesemelter', 'Chef\'s knife', 
'Cherry pitter', 'Chinois', 'Chinoise', 'Chip pan', 'Chocolatera', 'Chorkor oven', 'Cleaver', 'Clome oven', 'Colander', 'Comal', 'Combi steamer', 'Communal oven', 
'Convection microwave', 'Convection oven', 'Cookie cutter', 'Cookie mould', 'Cookie press', 'Cookie sheet', 'Cooking pot', 'Cooking twine', 'Corkscrew', 
'Corn roaster', 'Crab cracker', 'Crepe maker', 'Crepe pan', 'Cutting board', 
'Deep fryer', 'Double boiler', 'Doufeu', 'Dough scraper', 'Drum sieve', 'Dutch oven', 
'Earth oven', 'Edible tableware', 'Egg piercer', 'Egg poacher', 'Egg separator', 'Egg slicer', 'Egg timer', 'Electric cooker', 'Energy regulator', 'Espresso machine', 
'Field kitchen', 'Fillet knife', 'Fire pot', 'Fish scaler', 'Fish slice', 'flat coil whisk', 'flat whisk', 'Flattop grill', 'Flour sifter', 'Food mill', 
'Food processor', 'Food steamer', 'Frying pan', 'Fufu Machine', 'Funnel', 
'Garlic press', 'Grapefruit knife', 'Grater', 'Gravy separator', 'Gravy strainer', 'gravy whisk', 'Griddle', 
'Halogen oven', 'Haybox', 'Herb chopper', 'Honey dipper', 'Horno', 'Hot Box', 'Hot plate', 
'Ice cream scoop', 
'Kamado', 'Karahi', 'Kazan', 'Kettle', 'Kettle', 'Kitchen scales', 'Kitchen scissors', 'Kitchen string', 'Kitchen twine', 'Kitchener range', 
'Kugelhopf pan', 'Kujiejun', 'Kyoto box', 
'Ladle', 'Lame', 'Lemon reamer', 'Lemon squeezer', 'Lobster cracker', 'Lobster fork', 'Lobster pick', 
'Mandoline', 'Masonry oven', 'Mated colander pot', 'Measuring cup', 'Measuring jar', 'Measuring jug', 'Measuring spoon', 'Meat grinder', 'Meat tenderiser', 
'Meat thermometer', 'Melon baller', 'Mess kit', 'Mezzaluna', 'Microwave oven', 'Milk guard', 'Milk watcher', 'Mincer', 'Molcajete', 'Mortar and pestle', 'Multicooker', 
'Nutcracker', 'Nutmeg grater', 
'Olive stoner', 'Oven glove', 'Oven mitt', 'Oven', 
'Pan', 'Pancake machine', 'Panini sandwich grill', 'Pastry bag', 'Pastry blender', 'Pastry brush', 'Pastry wheel', 'Peel', 'Peeler', 'Pepper grinder', 
'Pepper mill', 'Pie bird', 'Pie cutter', 'Pie funnel', 'Pie vent', 'Pizza cutter', 'Pizza shovel', 'Pizza slicer', 'Popcorn maker', 'Pot minder', 
'Pot', 'Potato masher', 'Potato peeler', 'Potato ricer', 'Pot holder', 'Poultry shears', 'Pressure cooker', 'Pressure cooker', 'Pressure fryer', 
'Ramekin', 'Reflector oven', 'Remoska', 'Rice cooker', 'Rice polisher', 'Ricer', 'Roasting jack', 'Roasting pan', 'Roasting rack', 'Rocket mass heater', 'Roller docker', 
'Rolling pin', 'Rotisserie', 'Russian oven', 'Sabbath mode', 
'Salamander broiler', 'Salt shaker', 'Samovar', 'Sandwich toaster', 'Saucepan', 'Saucier', 'Sautj pan', 'Scales', 'Scissors', 'Scoop', 'Scraper', 
'Self-cleaning oven', 'Set-n-Forget cooker', 'Sheet pan', 'Shichirin', 'Shredder', 'Sieve', 'Sieve', 'Sifter', 'Skillet', 'Skimmer', 'Slotted spoon', 
'Slow cooker', 'Solar cooker', 'Soufflj dish', 'Sous-vide cooker', 'Soy milk maker', 'Spatula', 'Spatula', 'Spider', 'Splayed Sautj pan', 'spoon sieve', 
'spoon skimmer', 'Springform pan', 'Stockpot', 'Stove', 'Strainer', 'Sugar thermometer', 'Susceptor', 
'Tabun oven', 'Tajine', 'Tamis', 'Tandoor', 'Tangia', 'Tava', 'tava', 'Tawa', 'Thermal immersion circulator', 'Tin opener', 'Toaster and toaster ovens', 
'Tomato knife', 'Tongs', 'Trussing needle', 'Tube pan', 'Turkey fryer', 'Turner', 'Twine', 
'Urokotori', 
'Vacuum fryer', 
'Waffle iron', 'Weighing scales', 'Wet grinder', 'Whisk', 'Wok', 'Wonder Pot', 'Wooden spoon', 'Wood-fired oven', 
'Zester']

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
"veal", "venison"]

herb_list = [
"basil", "bay",
"cayenne", "chives", "cilantro", "coriander",
"fennel",
"marjoram",
"nutmeg",
"oregano", 
"paprika", "parsley", "pepper",
"rosemary",
"thyme"]

sauce_list = [
"cheese", 
"paste"]

cooked_carb_list = [
"lasagna",
"noodles",
"pasta",
"rice", "rigatoni", 
"spaghetti", 
"vermicelli"]

soup_list = [
"broth", 
"soup"]


def getRecipe(url):
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
	raw_ingredients = getRecipe(url)[0]
	direction_list = getRecipe(url)[1]
	ingredients = []
	
	for i in raw_ingredients:
		ingredient = []
		measures = []
		prep = []
		desc = []
		types = []

		# get quantity
		# if not i[0].isdigit():
		# 	i[0] = '1'
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
		ingredient_item = []
		for chunk in item_chunks:
			if(chunk[1]=='VBD' or chunk[1]=='RB'):
				desc.append(chunk[0])
				item = item.replace(chunk[0],"").replace(',','').strip()

			it = []
			if(chunk[1] in ['NN','NNS','JJ','NNP']):
				it.append(chunk[0])
			ingredient_item.append(' '.join(it))

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
					if len(item2) > 0:
						if d[0].lower() == item2[0].lower():
							selected = index
							break
						index = index + 1	

				if selected > 0:
					if prep_chunks[index-2][0].lower() in preparation_list:
						prep.append(prep_chunks[index-2][0])

					if prep_chunks[index-1][0].lower() in preparation_list:
						prep.append(prep_chunks[index-1][0])
		
		# get types
		words = word_tokenize(item)
		for word in words:
			if word.lower() in protein_list:
				types.append("protein")
			elif word.lower() in herb_list:
				types.append("herb")
			elif word.lower() in sauce_list:
				types.append("sauce")
			elif word.lower() in cooked_carb_list:
				types.append("cooked_carb")
			elif word.lower() in soup_list:
				types.append("soup")

		ingredient.append(desc)
		# ingredient.append(item)
		ingredient.append(filter(None,ingredient_item))
		ingredient.append(prep)
		ingredient.append(types)
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
				json_data.update({'type': categ})
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
	direction_list = getRecipe(url)[1]
	directions = []
	tool = []
	for direction in direction_list:
		for item in tool_list:
			if item in direction or item.lower() in direction:
				tool.append(item)
	return tool

def getSteps(url):
	return getRecipe(url)[1]

def getAllData(url):
	print "########## Recipe Data Representation (" + url + ") ##########"
	all_json = {}
	ingredients=getIngredients(url)
	methods=getMethods(url)
	tools=getTools(url)

	all_json.update({'ingredients':ingredients})
	all_json.update({'methods':methods})
	all_json.update({'tools':tools})
	
	print all_json
	# print "##### Extracting ingredients #####"
	# print all_json["ingredients"]
	# print "##### Extracting methods #####"
	# print all_json["methods"]
	print "##### Extracting tools #####"
	print all_json["tools"]
	# print ""
	return all_json

def transform(orig, sel):
	
	print "########## Recipe Transformation ##########"
	orig["tools"] = ['AAA', 'BBB']

	got_garlic = False
	got_onion = False
	got_sauce = False
	got_mushroom = False
	got_fresh_herb = False

	transformation_notes = []

	#DIY TO EASY TRANSFORMATION 
	if sel == "easy":
		for key in orig["ingredients"]:
			this_ingredient = orig["ingredients"][key]

			#Change all fresh herbs to dried herbs
			if "herb" in this_ingredient["type"]:
				got_fresh_herb = True
				i = 0
				while i < len(this_ingredient["item"]):
					if "fresh" in str(this_ingredient["item"][i]):
						this_ingredient["item"][i]	= u'dried'
					i += 1
				
				if "freshly" in str(this_ingredient["desc"]):
					this_ingredient["desc"] = u'dried'

			#Change all uncooked pasta to cooked pasta
			if "cooked_carb" in this_ingredient["type"]:
				this_ingredient["desc"] = u'cooked'
				name_of_ingredient = ""
				for i in this_ingredient["item"]:
					name_of_ingredient += str(i)
					name_of_ingredient += " "
				transformation_notes.append("You can skip cooking the " + name_of_ingredient)

			#Change all raw chicken to cooked chicken
			if "protein" in this_ingredient["type"]:
				i = 0
				while i < len(this_ingredient["item"]):
					if "chicken" in str(this_ingredient["item"][i]):
						this_ingredient["item"][i]	= u'cooked chicken'
						transformation_notes.append("When using cooked chicken, you can skip cooking the chicken or cook for less time")
					i += 1

		#Check if there is there is garlic, onion, mushroom, or sauce mentioned in the steps
		for step in getRecipe(url)[1]:
			if "garlic" in step:
				got_garlic = True
			if "sauce" in step:
				got_sauce = True
			if "onion" in step:
				got_onion = True
			if "mushroom" in step:
				got_mushroom = True

		#Add tips to the notes section
		if got_fresh_herb:
			transformation_notes.append("You can use dried instead of fresh herbs")
		if got_garlic:
			transformation_notes.append("You may be able to get pre-minced garlic in the store")
		if got_sauce:
			transformation_notes.append("You may be able to find pre-made sauce in the store")
		if got_onion:
			transformation_notes.append("You may be able to find pre-cut onions in the store")
		if got_mushroom:
			transformation_notes.append("You may be able to find pre-sliced mushrooms in the store")

		#Print all of the new ingredients, steps, and notes
		print "##### New Ingredients #######"
		for key in orig["ingredients"]:
			print orig["ingredients"][key]

		print "##### New Steps #######"
		print "--NOTES--"
		for i in transformation_notes:
			print i
		print "--STEPS--"
		for step in getRecipe(url)[1]:
			print step

	#DIY TO SUPER EASY TRANSFORMATION
	if sel == "super easy":
		print "Just go to a restaurant already!"

# original_recipe = getAllData('http://allrecipes.com/recipe/lasagna-alfredo/')
# original_recipe = getAllData('http://allrecipes.com/recipe/8732/poppy-seed-chicken')
original_recipe = getAllData('http://allrecipes.com/recipe/214029/lamb-shawarma')
# original_recipe = getAllData('http://allrecipes.com/recipe/216879/mediterranean-meat-pies-sfeeha')

# original_recipe = getAllData('http://allrecipes.com/recipe/27253/canadian-cedar-planked-salmon')


# getAllData('http://allrecipes.com/recipe/234312/how-to-make-focaccia/')
# getAllData('http://allrecipes.com/recipe/222680/bon-appetits-meatballs/')
# # getAllData('http://allrecipes.com/recipe/126942/ricotta-gnocchi/')
# getAllData('http://allrecipes.com/recipe/21412/tiramisu-ii/')
# getAllData('http://allrecipes.com/recipe/246628/spaghetti-cacio-e-pepe/')
# getAllData('http://allrecipes.com/recipe/246866/rigatoni-alla-genovese/')
# getAllData('http://allrecipes.com/recipe/17167/sicilian-spaghetti/')
# getAllData('http://allrecipes.com/recipe/7245/jays-signature-pizza-crust/')
# getAllData('http://allrecipes.com/recipe/23600/worlds-best-lasagna/')
# getIngredients('http://allrecipes.com/recipe/lasagna-alfredo/')

# sel = "0"
# while 1:
# 	sel = raw_input("What kind of transformation do you want? ")
# 	if sel == "1" or sel == "2" or sel == "3" or sel == "4" or sel == "5":
# 		print "You chose " + sel
# 		break;




# transform(original_recipe, sel)


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
