from bs4 import BeautifulSoup
import urllib2
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import json
import unicodedata
import requests
from fractions import Fraction
import random 

protein_rpc_list =['veggie deli slices',
'veggie burgers',
'veggie meatballs',
'veggie sausage links and patties',
'veggie bacon',
'soy chicken patties and nuggets',
'veggie meatloaf and Salisbury steak',
'veggie jerky','tofu']

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
"Fermentation", "Flambe", "Flattop grill", "Foam", "Food preservation", "Fondue", "Fruit preserves", "Frying", "Fry",
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

vegi_sauce = ["Alfredo sauce", "Apricot Cherry Compote sauce", "Arugula Pesto sauce", 
"Bechamel sauce", "Berry sauce", "Bottle hot pepper sauce", "Cashew Bechamel sauce", "Cashew Cream sauce", "Chili garlic sauce", "Chily Soy Dipping sauce", 
"Chimichurri sauce", "Cranberry sauce", "Canned tomato sauce", 
"Fresh Tomato sauce", "Fruity BBQ sauce", 
"Goat Cheese sauce", "Gravy sauce", "Grilled Tomato sauce", "Garlic sauce", 
"Herby Wine sauce", "Hot Pepper sauce", 
"Italian Tomato sauce", 
"Jar tomato pasta sauce", 
"Kiss the Cook Tomato sauce", "Korean-Inspired Dipping sauce", 
"Mushroom sauce", "Mushroom-Miso Gravy sauce", 
"Pasta with Squash sauce", "Pea Pesto sauce", "Peanut sauce", "Pesto sauce", "Pico de Gallo Salsa sauce", "Pistou sauce", 
"Quick BBQ sauce", 
"Raw Marinara sauce", "Red Chile sauce", "Red Pepper Coulis sauce", 
"Sage Gravy sauce", "Salsa a la huancaina sauce", "Seitan Bolognese sauce", "Seitan Broth Gravy sauce", "Sherry sauce", "Spicy Tomato Cream sauce", 
"Sun-Dried Tomato Pesto sauce", 
"Tahini sauce", "Tartar sauce", "Tomato sauce", "Tomato Garlic sauce", "Tomato-based chili sauce", "Tzatziki Cucumber Dip sauce", "Teriyaki marinade sauce", 
"Teriyaki sauce", 
"Unsweetened Apple sauce", "Walnut sauce", "Whole cranberry sauce", 
"Zabaglione sauce"]

vegan_sauce = ["Vegan Cheese sauce", "Savory Vegan sauce", "Fresh Tomato Dipping sauce"]

non_veg_sauce = ["Apple sauce", "Adobo sauce", "Asian fish sauce", 
"Barbecue sauce", "Browning sauce", "Brown Sugar sauce", "Black soy sauce", 
"Caramel sauce", "Chile sauce", "Chili bean sauce", "Chile-garlic sauce", 
"Dash hot sauce", "Dash hot pepper sauce", "Dark soy sauce", "Duck sauce", "Dipping sauce", "Dry enchilada sauce", "Drops hot pepper sauce", 
"Dash soy sauce", 
"Enchilada sauce", 
"Fish sauce", 
"Hot sauce", "Hoisin sauce", 
"Green chile enchilada sauce", "Gluten-free soy sauce", 
"Jars spaghetti sauce", "Jars pasta sauce", "Jar picante sauce", "Jar taco sauce", "Jalapeno sauce", 
"Lite soy sauce", "Lamb sauce", "Low sodium soy sauce", 
"Marinara sauce", "Mango hot sauce", 
"Oyster sauce", 
"Prepared marinara sauce", "Prepared barbecue sauce", "Prepared hollandaise sauce", "Pizza sauce", "Parsley sauce", "Pesto sauce", "Processed cheese sauce", 
"Quick Thai Dipping sauce", 
"Roasted Garlic sauce", "Raspberry Apple sauce", "Reduced-sodium soy sauce", "Red enchilada sauce", "Red pimento sauce", 
"soy sauce", "Steak sauce", "Sriracha hot sauce", "Salted Caramel sauce", "Seasoned Soy sauce", "Sofrito sauce", "Spaghetti sauce", "Sriracha hot sauce", 
"Thai chili sauce", "Thai peanut sauce", "Tonkatsu sauce", "Taco sauce", "Thicken sauce", "Thick soy sauce", "Tahini sauce", 
"Vegetarian Worcestershire sauce", 
"Wweet and sour sauce", "Wweet soy sauce", "White Chocolate Brandy sauce", "Worcestershire sauce"]


african_main_dishes = ["hot sauce", "soy sauce", "chipotle pepper in adobo sauce", "adobo sauce from chipotle peppers", "tomato sauce", 
"Worcestershire sauce", "dash Worcestershire sauce"]
african_side_dishes = ["tomato sauce", "red pimento sauce"]
african_soups_stews = ["mackerel in tomato sauce", "tomato sauce", "Worcestershire sauce", "soy sauce"]
east_african = ["Worcestershire sauce", "soy sauce"]
north_african = ["chipotle pepper in adobo sauce", "adobo sauce from chipotle peppers", "tomato sauce", "tahini sauce", "soy sauce", "Sauce:", 
"red pimento sauce", "hot sauce"]
south_african = ["Sauce", "Worcestershire sauce", "soy sauce", "Sauce:", "Sauce:", "dash Worcestershire sauce"]
chinese = ["soy sauce", "chili sauce", "oyster sauce (optional)", "reduced-salt soy sauce", "dash hot pepper sauce", "oyster sauce", 
"dark soy sauce", "light soy sauce", "hoisin sauce", "teriyaki sauce", "bottles black bean sauce", "chile-garlic sauce (such as Sriracha)", 
"sweet and sour sauce for dipping", "black bean sauce", "fish sauce"]
filipino = ["oyster sauce", "soy sauce", "tomato sauce", "spaghetti sauce", "soy sauce, or to taste", "sambal chili paste, or other hot pepper sauce to taste", 
"fish sauce", "Worcestershire sauce", "peanut butter or  needed to thicken sauce", "soy sauce to taste", "fish sauce for sprinkling, if desired (optional)", 
"sweet chili sauce", "dash hot pepper sauce (e.g. Tabasco??", "hot pepper sauce (such as Tabasco) (optional)", "dark soy sauce", 
"fish sauce (optional)", "soy sauce (optional)"]
indian = ["tomato sauce", "hot sauce (such as Tabasco), or to taste", "hot pepper sauce (such as Tabasco)"]
japanese = ["soy sauce", "Worcestershire sauce", "dark soy sauce", "low sodium soy sauce", "dash hot pepper sauce", "low-sodium soy sauce", 
"hoisin sauce", "reduced-sodium soy sauce", "soy sauce, or to taste", "light soy sauce", "Sauce", "tonkatsu sauce or barbeque sauce", 
"chili garlic sauce"]
korean = ["soy sauce", "fish sauce (optional)", "Sauce:", "fish sauce", "low-sodium soy sauce", "soy sauce (such as Kikkoman)", 
"chile-garlic sauce (such as sambal), or to taste", "dark soy sauce", "light soy sauce", "gluten-free soy sauce (tamari)", 
"reduced-sodium soy sauce", "barbeque sauce", "chile-garlic sauce (such as Sriracha) (optional)", "chili bean sauce (toban djan)", 
"Asian fish sauce (nuoc mam or nam pla)", "low sodium soy sauce", "Worcestershire sauce", "sriracha hot sauce, or to taste", "hoisin sauce", 
"Dipping Sauce:", "Seasoned Soy Sauce:", "Kikkoman Teriyaki Marinade & Sauce", "hot pepper sauce", "sweet red chili sauce, or to taste"]
thai = ["soy sauce", "Quick Thai Dipping Sauce:", "light soy sauce", "chili sauce", "fish sauce", "hot sauce", "prepared Thai peanut sauce", 
"oyster sauce", "fish sauce, or to taste", "Sauce", "hoisin sauce", "sweet chili sauce", "dash soy sauce", "red chile sauce", "peanut sauce", 
"Asian fish sauce", "dark soy sauce", "chile-garlic sauce (such as Sriracha), or more to taste", "dash chili sauce", "Asian chile pepper sauce", 
"thick soy sauce", "hot pepper sauce", "Thai peanut sauce", "jar peanut sauce", "lite soy sauce", "tomato sauce", "Worcestershire sauce", 
"teriyaki sauce", "Thai pepper garlic sauce", "black soy sauce", "low-sodium soy sauce", "low-sodium teriyaki sauce"]
australian_newzealand = ["White Chocolate Brandy Sauce:", "teriyaki sauce"]
canadian = ["Thai chili sauce", "soy sauce", "sriracha hot sauce, or more to taste", "tomato sauce", "Worcestershire sauce", 
"dash hot sauce, or to taste", "applesauce", "prepared hollandaise sauce", "sweet chili sauce", "fish sauce", "unsweetened applesauce", 
"prepared barbecue sauce"]
canadian_occasions = ["soy sauce", "hot sauce", "barbeque sauce", "tomato sauce", "browning sauce (such as Kitchen Bouquet), or as desired", 
"hot pepper sauce", "dashes hot pepper sauce (such as Tabasco)", "Worcestershire sauce", "reduced-sodium soy sauce", "hoisin sauce", 
"chili garlic sauce", "dash Worcestershire sauce, or to taste", "dash hot pepper sauce (such as Tabasco), or to taste", "applesauce"]
toronto = ["soy sauce", "barbecue sauce", "dark soy sauce", "lite soy sauce", "Worcestershire sauce", "teriyaki sauce", "fish sauce", 
"hot pepper sauce", "barbeque sauce", "dash hot pepper sauce, or to taste", "steak sauce, (e.g. Heinz 57)", "sweet and sour sauce", 
"hoisin sauce", "tomato sauce"]
quebec = ["hot pepper sauce (such as Frank's RedHot)", "applesauce", "prepared hollandaise sauce", "Worcestershire sauce", 
"pizza sauce, or as needed", "soy sauce"]
vancouver = ["barbeque sauce", "tomato sauce", "soy sauce", "Worcestershire sauce", "dash hot pepper sauce, or to taste", "dark soy sauce", 
"chile-garlic sauce", "jar spaghetti sauce", "Berry Sauce:", "applesauce", "reduced-sodium soy sauce", "hoisin sauce", "chili garlic sauce", 
"chipotle peppers in adobo sauce", "chili sauce", "fish sauce"]
# belgian = []
# austrian = []
eastern_europe = ["soy sauce", "Worcestershire sauce", "dashes hot pepper sauce", "hot pepper sauce", "drops hot sauce", 
"processed cheese sauce", "tomato sauce", "chili sauce"]
dutch = ["For the Lamb Sauce:", "For the Garlic Sauce:", "Worcestershire sauce", "soy sauce to taste"]
german = ["tomato-based chili sauce", "whole cranberry sauce", "vegetarian Worcestershire sauce", "soy sauce", "tomato sauce", 
"chili sauce", "barbecue sauce", "Worcestershire sauce", "drops hot pepper sauce"]
french = ["Worcestershire sauce", "dash hot pepper sauce (e.g. Tabasco??"]
greek = ["tomato sauce", "Tzatziki Sauce (cucumber sauce):", "soy sauce", "Sauce:"]
italian = ["canned tomato sauce", "pesto sauce", "jar tomato pasta sauce", "tomato sauce", "prepared marinara sauce", "jar spaghetti sauce", 
"taco sauce", "jars spaghetti sauce", "jars pasta sauce", "spaghetti sauce", "Sauce:", "dry Alfredo sauce mix", "SAUCE", "jar Alfredo sauce"]
portuguese = ["tomato sauce", "chipotle chiles in adobo sauce", "hot pepper sauce", "Portuguese hot pepper sauce (pimenta)"]
scandinavian = ["tomato sauce", "Worcestershire sauce", "soy sauce"]
spanish = ["tomato sauce", "hot pepper sauce", "jar chili sauce", "Worcestershire sauce", "Dipping Sauce:", "sardines in tomato sauce", "dashes Worcestershire sauce, or to taste"]
uk_ireland = ["Worcestershire sauce", "tomato sauce", "browning sauce (such as Kitchen Bouquet), or as desired", "drops hot pepper sauce (such as Tabasco) (optional)", 
"soy sauce", "Heinz Worcestershire Sauce"]
swiss = ["Worcestershire sauce", "steak sauce (such as A1)"]
caribbean = ["soy sauce", "jar picante sauce", "duck sauce", "marinara sauce", "mango hot sauce", "tomato sauce", "sofrito sauce", 
"Dipping Sauce:", "hot sauce", "sweet soy sauce", "Hot sauce, to taste", "hot pepper sauce to taste", "hot pepper sauce (e.g. Tabasco?? (optional)", 
"teriyaki marinade sauce", "dashes hot pepper sauce", "unsweetened applesauce"]
south_american = ["soy sauce", "Sauce:", "tomato sauce", "pepper sauce (such as Frank's Red Hot)", "barbeque sauce", "dash soy sauce to taste", 
"jalapeno sauce (optional)", "Worcestershire sauce"]
mexican = ["tomato sauce", "green chile enchilada sauce", "soy sauce", "taco sauce", "enchilada sauce", "dry enchilada sauce mix", "drops hot pepper sauce", 
"dash hot pepper sauce", "jar taco sauce", "red enchilada sauce", "bottle hot pepper sauce", "hot sauce to taste", "Worcestershire sauce", 
"adobo sauce from chipotle peppers"]
israeli = ["dashes hot pepper sauce (such as Tabasco)"]
lebanese = ["tomato sauce", "Parsley Sauce", "Tahini Sauce"]
persian = ["tomato sauce"]
turkish = ["For the Lamb Sauce:", "For the Garlic Sauce:", "Tzatziki Sauce:"]

all_cuisine_list = [african_main_dishes, african_side_dishes, african_soups_stews, east_african, north_african, south_african, chinese, 
filipino, indian, japanese, korean, thai, australian_newzealand, canadian, canadian_occasions, toronto, quebec, vancouver, eastern_europe, 
dutch, german, french, greek, italian, portuguese, scandinavian, spanish, uk_ireland, swiss, caribbean, south_american, mexican, israeli, 
lebanese, persian, turkish]
all_cuisine_list_text = ["african_main_dishes", "african_side_dishes", "african_soups_stews", "east_african", "north_african", "south_african", "chinese", 
"filipino", "indian", "japanese", "korean", "thai", "australian_newzealand", "canadian", "canadian_occasions", "toronto", "quebec", "vancouver", "eastern_europe", 
"dutch", "german", "french", "greek", "italian", "portuguese", "scandinavian", "spanish", "uk_ireland", "swiss", "caribbean", "south_american", "mexican", "israeli", 
"lebanese", "persian", "turkish"]

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

state_list = ["broth", "soup"]

def removeLeadingBlank(ingredientList):
    updated_ingredientList=[]
    for ingredient in ingredientList:
        updated_ingredientList.append(ingredient.lstrip(' '))
    return updated_ingredientList

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

def getDirections(url):    
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page,"lxml")

    ingredient_list = soup.findAll(itemprop="ingredients")

    ingredients = []

    for ingredient in ingredient_list:
        splited_ingredient=ingredient.text.split(' ',1)
        if len(splited_ingredient)==1:
            pass
        else:
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

    return directions


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



		if item.lower() in vegi_sauce or item in vegi_sauce:
			types.append("vegitarian")
		elif item.lower() in vegan_sauce or item in vegan_sauce:
			types.append("vegan")
		elif item.lower() in non_veg_sauce or item in non_veg_sauce:
			types.append("nonveg")

		# # get types
		# words = word_tokenize(item)
		# for word in words:
		# 	if word.lower() in protein_list:
		# 		types.append("protein")
		# 	elif word.lower() in herb_list:
		# 		types.append("herb")
		# 	elif word.lower() in sauce_list:
		# 		types.append("sauce")
		# 	elif word.lower() in cooked_carb_list:
		# 		types.append("cooked_carb")
		# 	elif word.lower() in state_list:
		# 		types.append("state")

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

def getType(recipe):
	# print "##### getType #####"
	# print recipe["ingredients"][1]["item"]
	for i in recipe["ingredients"]:
		# for j in recipe["ingredients"][i]:
		if len(recipe["ingredients"][i]["type"]) > 0:
			if recipe["ingredients"][i]["type"][0] == "nonveg":
				return "non vegetarian"

	return "vegetarian"

	# print orig["ingredients"][1]["item"]
	# print orig["ingredients"][2]["item"]
	# print orig["ingredients"][3]["item"]
	# for i in orig:
	# 	for j in orig[i]:
	# 		if i == "tools":
	# 			print "##### Tools to Use #####"
	# 			for k in orig[i][j]:
	# 				print k
	# 		if i == "methods":
	# 			print "##### Methods to Use #####"
	# 			for k in orig[i][j]:
	# 				print k
	# 		if i == "ingredients":
	# 			print "##### Ingredient List " + str(j) + " #####"
	# 			for k in orig[i][j]:
	# 				print orig[i][j][k]

def getCuisine(url):
	# r  = requests.get("http://allrecipes.com/recipe/53731/chap-chee-noodles/?internalSource=staff%20pick&referringId=86&referringContentType=recipe%20hub&clickId=cardslot%202" )
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "lxml")
	rst=soup.find("ul", "breadcrumbs breadcrumbs").find_all('li')
	final_rst= rst[len(rst)-1].text.strip()
	# print final_rst
	return final_rst

def getAllData(url):
	print "########## Recipe Data Representation (" + url + ") ##########"
	all_json = {}
	ingredients=getIngredients(url)
	methods=getMethods(url)
	tools=getTools(url)
	cuisine=getCuisine(url)

	directions_list=[]
	directions = getDirections(url)
	index=1

	all_json.update({'ingredients':ingredients})
	temp = {1 : methods}
	# all_json.update({'methods':methods})
	all_json.update({'methods':temp})
	temp = {1 : tools}
	# all_json.update({'tools':tools})
	all_json.update({'tools':temp})
	

	temp = {1 : cuisine}
	all_json.update({'cuisine':cuisine})


	for direction in directions:
	    new_dir = removeLeadingBlank(direction.split("."))
	    new_dir = filter(None, new_dir) # fastest
	    for element in new_dir: 
	        new_element=element+"."
	        # print str(index)+". "+new_element
	        directions_list.append(str(index)+". "+new_element)         
	        index=index+1

	# print "===== STEP!!!!! ====="
	# print directions_list
	# print "===== STEP!!!!! ====="

	all_json.update({'step':directions_list})
	# print all_json
	# print "##### Extracting ingredients #####"
	# print all_json["ingredients"]
	# print "##### Extracting methods #####"
	# print all_json["methods"]
	# print "##### Extracting tools #####"
	# print all_json["tools"]
	# print ""
	
	types=getType(all_json)
	temp = {1 : types}
	all_json.update({'types':temp})

	# print all_json
	return all_json

def diytoeasy(orig, sel, url):
	print "########## DIY TO EASY ##########"
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

def transform(orig, sel):
	print "########## Recipe Transformation ##########"
	if sel == "1":
		print "you chose 1"
	a = 0
	b = 0
	# print orig["ingredients"][1]["item"]
	# print orig["ingredients"][2]["item"]
	# print orig["ingredients"][3]["item"]
	for i in orig:
		for j in orig[i]:
			# if i == "tools":
			# 	print "##### Tools to Use #####"
			# 	for k in orig[i][j]:
			# 		print k
			# if i == "methods":
			# 	print "##### Methods to Use #####"
			# 	for k in orig[i][j]:
			# 		print k
			if i == "types":
				# print "##### Types of Ingredient #####"
				if orig[i][j] == "non vegetarian":
					print "Vegetarian Source List"
					for l in vegi_sauce:
						print "-" + l
					
					while 1:
						sauce_sel = raw_input("Which sauce do you want to use? ")
						if sauce_sel in vegi_sauce:
							print "Okay"
							break
						else:
							print "You typed wrong sauce!"
					# print vegi_sauce
					# print orig[i][j]

			if i == "ingredients":
				# print "- Ingredient List " + str(j)
				for k in orig[i][j]:
					if k == "type":
						if len(orig[i][j][k]) > 0:
							if orig[i][j][k][0] == "nonveg":
								# print orig[i][j]
								# del orig[i][j]
								# print "-----"
								a = i
								b = j
								# print orig[i][j]

						# print ' '.join(str(p) for p in orig[i][j][k]) 
						# print orig[i][j][k]
	temp1 = []
	temp1.append("vegetarian")
	orig["types"][1] = "vegetarian"
	temp2 = []
	temp2.append(sauce_sel)
	orig[a][b]["item"] = temp2
	orig[a][b]["type"] = ["vegetarian"]
    
   glb_ingredients_dic           =orig["ingredients"]
   glb_ingredients_list          =[]
#   glb_ingredients_quantity_list =[]
#   glb_tools_list                =list(orig["tools"])
#   glb_methods_list              =list(orig["methods"]) 
    #PPS: Get ingredient name
    for index, value in glb_ingredients_dic.iteritems(): 
        merged_item=" ".join(value["item"])
        glb_ingredients_list.append(merged_item)
    
    for protein in protein_list:
        for index,vaule in enumerate(glb_ingredients_list):
        try:
            lower_ingredient= vaule.encode("utf-8").lower()
            if protein in lower_ingredient:
                #Update ingredient name list
                protein_rpc_list_len=len(protein_rpc_list)
                random_index=random.randint(0, protein_rpc_list_len-1)
                new_ingredient=  lower_ingredient.replace(protein,protein_rpc_list[random_index])
                glb_ingredients_list[index]=lower_ingredient
    
        except:
            pass
    print glb_ingredients_list
	return orig


def transformfromVegToNonVeg(orig, sel):
	print "########## Recipe Transformation ##########"
	if sel == "1":
		print "you chose 1"
	a = 0
	b = 0
	# print orig["ingredients"][1]["item"]
	# print orig["ingredients"][2]["item"]
	# print orig["ingredients"][3]["item"]
	for i in orig:
		for j in orig[i]:
			# if i == "tools":
			# 	print "##### Tools to Use #####"
			# 	for k in orig[i][j]:
			# 		print k
			# if i == "methods":
			# 	print "##### Methods to Use #####"
			# 	for k in orig[i][j]:
			# 		print k
			if i == "types":
				# print "##### Types of Ingredient #####"
				if orig[i][j] == "vegetarian": #Need check syntax
					print "non_veg_sauce Source List"
					for l in non_veg_sauce:
						print "-" + l
					
					while 1:
						sauce_sel = raw_input("Which sauce do you want to use? ")
						if sauce_sel in non_veg_sauce:
							print "Okay"
							break
						else:
							print "You typed wrong sauce!"
					# print vegi_sauce
					# print orig[i][j]

#			if i == "ingredients":
#				# print "- Ingredient List " + str(j)
#				for k in orig[i][j]:
#					if k == "type":
#						if len(orig[i][j][k]) > 0:
#							if orig[i][j][k][0] == "nonveg":
#								# print orig[i][j]
#								# del orig[i][j]
#								# print "-----"
#								a = i
#								b = j
#								# print orig[i][j]
#
#						# print ' '.join(str(p) for p in orig[i][j][k]) 
#						# print orig[i][j][k]
#	temp1 = []
#	temp1.append("vegetarian")
#	orig["types"][1] = "vegetarian"
#	temp2 = []
#	temp2.append(sauce_sel)
#	orig[a][b]["item"] = temp2
#	orig[a][b]["type"] = ["vegetarian"]
    
   glb_ingredients_dic           =orig["ingredients"]
   glb_ingredients_list          =[]
   glb_type_list                 =[]
#   glb_ingredients_quantity_list =[]
#   glb_tools_list                =list(orig["tools"])
#   glb_methods_list              =list(orig["methods"]) 
    #PPS: Get ingredient name
    for index, value in glb_ingredients_dic.iteritems(): 
        merged_item=" ".join(value["item"])
        glb_ingredients_list.append(merged_item)
        
        merged_type=" ".join(value["type"])
        glb_type_list.append(merged_type)
    
    for protein in protein_rpc_list:
        for index,vaule in enumerate(glb_ingredients_list):
        try:
            lower_ingredient= vaule.encode("utf-8").lower()
            if protein in lower_ingredient:
                #Update ingredient name list
                protein_list_len=len(protein_list)
                random_index=random.randint(0, protein_list_len-1)
                new_ingredient=  lower_ingredient.replace(protein,protein_list[random_index])
                glb_ingredients_list[index]=new_ingredient
                glb_type_list[index]="nonveg"                    
    
        except:
            pass
    print glb_ingredients_list
    print glb_type_list
	return orig



def transform2(orig, sel):
	print "########## Recipe Transformation 2 ##########"
	# if sel == "1":
	# 	print "you chose 1"
	sauce_sel = "AAABBB"
	a = 0
	b = 0
	# print orig["ingredients"][1]["item"]
	# print orig["ingredients"][2]["item"]
	# print orig["ingredients"][3]["item"]
	for i in orig:
		for j in orig[i]:
			# if i == "tools":
			# 	print "##### Tools to Use #####"
			# 	for k in orig[i][j]:
			# 		print k
			# if i == "methods":
			# 	print "##### Methods to Use #####"
			# 	for k in orig[i][j]:
			# 		print k


			# commented
			# if i == "types":
			# 	# print "##### Types of Ingredient #####"
			# 	if orig[i][j] == "non vegetarian":
			# 		print "Vegetarian Source List"
			# 		for l in vegi_sauce:
			# 			print "-" + l
					
			# 		while 1:
			# 			sauce_sel = raw_input("Which sauce do you want to use? ")
			# 			if sauce_sel in vegi_sauce:
			# 				print "Okay"
			# 				break
			# 			else:
			# 				print "You typed wrong sauce!"
			


					# print vegi_sauce
					# print orig[i][j]

			if i == "ingredients":
				# print "- Ingredient List " + str(j)
				for k in orig[i][j]:
					if k == "item":
						# if len(orig[i][j][k]) > 0:
						# 	if orig[i][j][k][0] == "nonveg":
						# 		# print orig[i][j]
						# 		# del orig[i][j]
						# 		# print "-----"
						# 		a = i
						# 		b = j
						# 		# print orig[i][j]

						titem = ' '.join(str(p) for p in orig[i][j][k])
						print titem
						if titem in vegi_sauce or titem in vegan_sauce or titem in non_veg_sauce:
							# print "-----"
							# print orig[i][j]
							# del orig[i][j]
							a = i
							b = j
						# print orig[i][j][k]
	# temp1 = []
	# temp1.append("vegetarian")
	# orig["types"][1] = "vegetarian"
	temp2 = []
	temp2.append(sel)
	orig[a][b]["item"] = temp2
	orig[a][b]["type"] = ["vegetarian"]
	print "check here"
	print orig[a][b]["item"]
	return orig

def showRecipe(orig):
	print "##### Cuisine #####"
	print orig["cuisine"]

	for i in orig:
		for j in orig[i]:
			if i == "tools":
				print "##### Tools to Use #####"
				for k in orig[i][j]:
					print k
			if i == "methods":
				print "##### Methods to Use #####"
				for k in orig[i][j]:
					print k
				print "##### Ingredient List #####"			
			if i == "types":
				print "##### Types of Ingredient #####"
				print orig[i][j]
			if i == "ingredients":
				print "- Ingredient List " + str(j)
				for k in orig[i][j]:
					if k == "item":
						print ' '.join(str(p) for p in orig[i][j][k]) 
					if k == "type":
						print ' '.join(str(p) for p in orig[i][j][k]) 
	
	print "##### Steps #####"
	for i in orig["step"]:
		print i
	# print orig["step"]
				# for k in orig[i][j]:
				# 	print k	

# original_recipe = getAllData('http://allrecipes.com/recipe/lasagna-alfredo/')
# original_recipe = getAllData('http://allrecipes.com/recipe/8732/poppy-seed-chicken')
# original_recipe = getAllData('http://allrecipes.com/recipe/214029/lamb-shawarma')



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

def update_steps(directions_list):
  for index,vaule in enumerate(directions_list):
    try:
         formated_step=vaule.encode("utf-8")
         for ch in ['butter','Butter']:
            if ch in formated_step:
              new_step=formated_step.replace(ch,"margarine")
              directions_list[index]=new_step
#        lower_step= vaule.encode("utf-8").lower()
#        if "butter" in lower_step:
#            #Update ingredient list
#            lower_step=  vaule.replace("butter","margarine")
#            directions[index]=lower_step
            
 
    except:
           print vaule+"contains non alphabet leter"      
  return directions_list  

#==============================================================================
# PPS: Increase the denominator by given increase_value
# Input: Fraction in string, int (increase_value)
# Output: Fraction                
#==============================================================================
def update_fraction(a_fraction, increase_value):
    a_fraction_in_fraction_format=Fraction(a_fraction)
    old_denominator=a_fraction_in_fraction_format.denominator
    new_denominator =old_denominator+increase_value
    new_numerator=a_fraction_in_fraction_format.numerator
    new_fraction= Fraction(new_numerator,new_denominator)
    return new_fraction

def update_quantity(a_fraction):
	# print "########################"
    return str(update_fraction(a_fraction,1))



#==============================================================================
# This code sections is for tool transformation
# Available transformation: 
# Bake  -> Fry
# Bake  -> Steam
# Steam -> Fry
# Steam -> Bake
#==============================================================================
print "--------------For Tools Transformation-------------------"

#1. Bake ->  Fry

#==============================================================================
# def replace_tools(pre_tool, updt_tool,tool_lst):
#     for index,tool in enumerate(tool_lst):
#         lower_tool= tool.encode("utf-8").lower()
#         #print lower_tool
#         if pre_tool.lower() in lower_tool:
#             tool_lst[index]=updt_tool
# #            print "catched"
#     return tool_lst
#==============================================================================

def replace_elements(pre_item, updt_item,item_lst):
    for index,item in enumerate(item_lst):
        lower_item= item.encode("utf-8").lower()
        #print lower_item
        if pre_item.lower() in lower_item:
            item_lst[index]=updt_item
#            print "catched"
    return item_lst



def update_steps_in_tool_transform(lst_pre_item,updt_item, dir_list):
  for index,vaule in enumerate(dir_list):
    try:
         formated_step=vaule.encode("utf-8")
         for ch in lst_pre_item:
            if ch in formated_step:
              new_step=formated_step.replace(ch, updt_item)
              dir_list[index]=new_step         
    except:
           print vaule+"contains non alphabet leter"      
  return     dir_list  

def Updata_Quantity_list(protein_list, ingre_list,quantity_list, isIncrease):
    
    protein_index_list=[]
    
    #Get non-protein list
    for index,ingre in enumerate(ingre_list):
        try:
            for protein in protein_list:
                if protein.lower() in ingre.lower():
                    protein_index_list.append(index)
        except:
             pass
         
    
    #Update quantity
    if not isIncrease:
        for index in range(0,len(ingre_list)):
            if index not in protein_index_list:
            #Update dedicated quantity
                prev_quantity= quantity_list[index]            
                upd_quantity = increase_quantity(prev_quantity)   
                quantity_list[index]=upd_quantity  
    else:
        for index in protein_index_list:
            #Update dedicated quantity
            prev_quantity= quantity_list[index]            
            upd_quantity = increase_quantity(prev_quantity)   
            quantity_list[index]=upd_quantity  

        
    return   quantity_list              
    
def bake2fry(toollist, methodlist, ingredient_list,directionlist,ingre_quantitylist):
           
    print toollist
    print methodlist
    print directionlist
    
    
    toollist   =replace_elements("oven", "pan", toollist)
    methodlist =replace_elements("bake", "fry", methodlist)
    directionlist  =update_steps_in_tool_transform(['bake','Bake'],'fry',directionlist)
    directionlist  =update_steps_in_tool_transform(['oven','Oven'],'pan',directionlist)
    
    print "Original quantity list"
    print ingre_quantitylist
    ingre_quantitylist=Updata_Quantity_list(protein_list,ingredient_list,ingre_quantitylist, False)
        
    print "Update quantity list"
    print ingre_quantitylist   
            
    print toollist
    print methodlist
    print directionlist


# bake2fry(glb_tools_list,glb_methods_list,glb_ingredients_list,directions_list,glb_ingredients_quantity_list)


#2. Fry  ->  Bake
def fry2bake(toollist, methodlist, ingredient_list,directionlist,ingre_quantitylist):
           
    print toollist
    print methodlist
    print directionlist
    
    
    toollist   =replace_elements("pan", " oven", toollist)
    methodlist =replace_elements("fry", "bake", methodlist)
    directionlist  =update_steps_in_tool_transform(['fry','Fry'],'bake',directionlist)
    directionlist  =update_steps_in_tool_transform(['pan','Pan'],'oven',directionlist)
    
    print "Original quantity list"
    print ingre_quantitylist
    ingre_quantitylist=Updata_Quantity_list(protein_list,ingredient_list,ingre_quantitylist,True)
        
    print "Update quantity list"
    print ingre_quantitylist   
            
    print toollist
    print methodlist
    print directionlist


# fry2bake(glb_tools_list,glb_methods_list,glb_ingredients_list,directions_list,glb_ingredients_quantity_list)

#3. Roast ->  Fry

def roast2fry(toollist, methodlist, ingredient_list,directionlist,ingre_quantitylist):
           
    print toollist
    print methodlist
    print directionlist
    
    
    toollist   =replace_elements("oven", "pan", toollist)
    methodlist =replace_elements("roast", "fry", methodlist)
    directionlist  =update_steps_in_tool_transform(['roast','Roast'],'fry',directionlist)
    directionlist  =update_steps_in_tool_transform(['oven','Oven'],'pan',directionlist)
    
    print "Original quantity list"
    print ingre_quantitylist
    ingre_quantitylist=Updata_Quantity_list(protein_list,ingredient_list,ingre_quantitylist, False)
        
    print "Update quantity list"
    print ingre_quantitylist   
            
    print toollist
    print methodlist
    print directionlist


# roast2fry(glb_tools_list,glb_methods_list,glb_ingredients_list,directions_list,glb_ingredients_quantity_list)


#4. Fry  ->  Roast
def fry2roast(toollist, methodlist, ingredient_list,directionlist,ingre_quantitylist):
           
    print toollist
    print methodlist
    print directionlist
    
    
    toollist   =replace_elements("pan", "oven", toollist)
    methodlist =replace_elements("fry", "roast", methodlist)
    directionlist  =update_steps_in_tool_transform(['fry','Fry'],'roast',directionlist)
    directionlist  =update_steps_in_tool_transform(['pan','Pan'],'oven',directionlist)
    
    print "Original quantity list"
    print ingre_quantitylist
    ingre_quantitylist=Updata_Quantity_list(protein_list,ingredient_list,ingre_quantitylist,True)
        
    print "Update quantity list"
    print ingre_quantitylist   
            
    print toollist
    print methodlist
    print directionlist


# fry2roast(glb_tools_list,glb_methods_list,glb_ingredients_list,directions_list,glb_ingredients_quantity_list)




def getHealthy(original_recipe, url, level):
	glb_ingredients_dic           =original_recipe["ingredients"]
	glb_ingredients_list          =[]
	glb_ingredients_quantity_list =[]
	glb_tools_list                =list(original_recipe["tools"])
	glb_methods_list              =list(original_recipe["methods"])

	print "original!!"
	showRecipe(original_recipe)
	print "original!!"
	directions_list=[]
	directions = getDirections(url)
	index=1

	print "Your Selected " + level + " Healthy Level."

	for direction in directions:
	    new_dir = removeLeadingBlank(direction.split("."))
	    new_dir = filter(None, new_dir) # fastest
	    for element in new_dir: 
	        new_element=element+"."
	        # print str(index)+". "+new_element
	        directions_list.append(str(index)+". "+new_element)         
	        index=index+1



	for index, value in glb_ingredients_dic.iteritems(): 
	    merged_item=" ".join(value["item"])
	    glb_ingredients_list.append(merged_item)
	#    print merged_item
	# print ingredients_list
	#print glb_ingredients_list

	#PPS: Get ingredient quantity
	for index, value in glb_ingredients_dic.iteritems(): 
	    quantity=value["quantity"]
	    glb_ingredients_quantity_list.append(quantity)

	print "#######################################################3"
	print glb_ingredients_list
	print "#######################################################3"
	for index,vaule in enumerate(glb_ingredients_list):
	    try:
	        lower_ingredient= vaule.encode("utf-8").lower()
	        print lower_ingredient
        	print "#######################################################3"
	        if "butter" in lower_ingredient:
	            #Update ingredient name list
	            lower_ingredient=  lower_ingredient.replace("butter","margarine")
	            glb_ingredients_list[index]=lower_ingredient
	            print "The index is " +str(index)
	            
	            #Update dedicated quantity
	            prev_quantity= glb_ingredients_quantity_list[index]            
	            print "!!!!!"
	            print prev_quantity
	            upd_quantity = update_quantity(prev_quantity) 
	            print "11111"
	            print upd_quantity  
	            glb_ingredients_quantity_list[index]=upd_quantity
	            print "22222"
	            print glb_ingredients_quantity_list[index]

	            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	            print directions_list
	            directions_list = update_steps(directions_list)
	            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	            print directions_list
	        else:
	            pass
	    except:
	       print vaule+"contains non alphabet leter"      

	print glb_ingredients_list
	print glb_ingredients_quantity_list  
	print "@@@@@@@@@@@@@@@ Ingredient - JSON @@@@@@@@@@@@@@@"
	showRecipe(original_recipe)
	print "@@@@@@@@@@@@@@@ Ingredient - Item @@@@@@@@@@@@@@@"

	# print str(len(glb_ingredients_list))
	# print str(len(glb_ingredients_quantity_list))
	# print original_recipe["ingredients"][1]["item"]
	# print original_recipe["ingredients"][1]["quantity"]
	# print glb_ingredients_list[0]
	# print glb_ingredients_quantity_list[0]



	for i in original_recipe["ingredients"]:
		# print original_recipe["ingredients"][i]
		# print str(i)
		# print original_recipe["ingredients"][i]["item"]
		# print original_recipe["ingredients"][i]["quantity"]
		# print glb_ingredients_list[i-1]
		# print glb_ingredients_quantity_list[i-1]
		original_recipe["ingredients"][i]["item"] = glb_ingredients_list[i-1].split()
		original_recipe["ingredients"][i]["quantity"] = glb_ingredients_quantity_list[i-1].split()

	# all_json.update({'ingredients':ingredients})
	# temp = {1 : methods}
	
	print "Directions after healthy transformation"
	print str(len(original_recipe["step"]))
	print str(len(directions_list))
	print "@@@@@@@@@@@@@@@ Ingredient - STEP 1 @@@@@@@@@@@@@@@"
	# print original_recipe["step"]
	print original_recipe["step"][0]
	print original_recipe["step"][1]
	print "@@@@@@@@@@@@@@@ Ingredient - STEP 2 @@@@@@@@@@@@@@@"
	print directions_list[0]
	print directions_list[1]
	print directions_list[2]
	print directions_list[3]
	

	if len(original_recipe["step"]) == len(directions_list):
		count = 0
		for i in original_recipe["step"]:
			print i
			original_recipe["step"][count] = directions_list[count]
			count += 1
	elif len(original_recipe["step"]) < len(directions_list):
		del original_recipe["step"]
		# for i in directions_list:
		original_recipe.update({'step':directions_list})



	print "@@@@@@@@@@@@@@@ Ingredient - STEP 3 @@@@@@@@@@@@@@@"


	for step in directions_list:
	    print step

	print "@@@@@@@@@@@@@@@ Ingredient - Item @@@@@@@@@@@@@@@"
	showRecipe(original_recipe)
	print "@@@@@@@@@@@@@@@ Ingredient - Item @@@@@@@@@@@@@@@"

	




# input_url = 'http://allrecipes.com/recipe/66814/thai-crab-rolls/'
# input_url = 'http://allrecipes.com/recipe/14319/chinese-chicken-salad-iii'
input_url = 'http://allrecipes.com/recipe/18114/butter-crescents/'


# print all_cuisine_list[0]
sel = "0"
print "==================== YOUR RECIPE ===================="
original_recipe = getAllData(input_url)

# for test
# transform2(original_recipe, "soy sauce2")
print "==================== TEST!!! ===================="
transformed_recipe3 = getHealthy(original_recipe, input_url, "3")
# exit
print "==================== TEST!!! ===================="

# showRecipe(original_recipe)
print "### Select One For Your Recipe Transformation ###"
print "1. To and from vegetarian and/or vegan"
print "2. Sytle of cuisine"
print "3. To and from healthy"
print "4. DIY to easy"
print "5. Cooking method"
while 1:
	sel = raw_input("### What kind of transformation do you want? (Press \"exit\" to Exit) ")
	if sel == "1":
		transformed_recipe = transform(original_recipe, sel)
		print "==================== TRANSFORMED RECIPE ===================="
		showRecipe(transformed_recipe)
	elif sel == "2":
		count = 0
		for i in all_cuisine_list_text:
			print str(count) + ". " + all_cuisine_list_text[count] + " Cuisine"
			count += 1
		sel2 = raw_input("### Which number do you want to choose? (Press \"exit\" to Exit) ")
		
		# print str(int(sel2)+5)
		# if sel2 == "0":
		if int(sel2) in range(0, len(all_cuisine_list)):
			for i in all_cuisine_list[int(sel2)]:
				print i
			while 1:
				sel22 = raw_input("### Select Source : ")
				if sel22 in all_cuisine_list[int(sel2)]:
					print "you select!"
					transformed_recipe2 = transform2(original_recipe, sel22)
					print "==================== TRANSFORMED RECIPE ===================="
					showRecipe(transformed_recipe2)
					break
				else:
					print "You Pressed wrong button. Plese Try Again."

	elif sel == "3":
		sel3 = raw_input("### Which Healthy Level do you want to choose? (Press \"exit\" to Exit) ")
		transformed_recipe3 = getHealthy(original_recipe, input_url, sel3)
		print "==================== TRANSFORMED RECIPE ===================="
		showRecipe(transformed_recipe3, level)
		break
	elif sel == "4":
		while 1:
			sel4 = raw_input("### Which one do you want to choose \"easy\" or \"super \"easy\"? (Press \"exit\" to Exit) ")
			if sel4 == "easy":
				diytoeasy(original_recipe, sel4, input_url)
			elif sel4 == "super easy":
				diytoeasy(original_recipe, sel4, input_url)
			elif sel4 == "exit":
				print ""
				break
	elif sel == "5":
		print "sel5"
	elif sel == "exit":
		print "Thank you for using recipe transformation"
		break



# showRecipe(original_recipe)
# transformed_recipe = transform(original_recipe, sel)









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
