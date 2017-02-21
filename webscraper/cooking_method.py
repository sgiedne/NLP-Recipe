import re
import string
from bs4 import BeautifulSoup
import urllib2

page = urllib2.urlopen('http://allrecipes.com/recipe/lasagna-alfredo/').read()
soup = BeautifulSoup(page,"html.parser")

ingredient_list = soup.findAll(itemprop="ingredients")

ingredients = {}

mList = ["Amandine", "Anti-griddle", 
"Backwoods cooking", "Baghaar", "Broast", "Brown", "Boil", "Broil", "Bake", "Braise", "Barbeque", "Barbequing", "Bast",
"Candy making", "Caramelization", "Carry over cooking", "Casserole", "Charbroiling", "Chaunk", "Cheesemaking", "Chinese cooking techniques", "Clay pot cooking", "Coddling", "Concasse", "Conche", "Confit", "Cooking with alcohol", "Creaming", "Culinary triangle", "Curdling", "Curing", "Canning", "Crush", "combination cooking",
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

def get_method(directions):
	array = []
	for i in range(0, len(mList)):
		str = ".*(" + mList[i] + "|" + mList[i].lower() + ").*"
		if re.match(str, directions.text):
			array.append(mList[i])
	return array


method_list = soup.findAll("span",{"class" : "recipe-directions__list--item"})

print "===== Cooking Method Test ====="
methods = []
methods = get_method(method_list[1])

for i in methods:
	print i

