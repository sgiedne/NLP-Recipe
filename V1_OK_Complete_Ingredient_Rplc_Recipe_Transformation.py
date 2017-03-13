from bs4 import BeautifulSoup
import urllib2
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import json
import unicodedata
from fractions import Fraction

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
"Vietnamese cooking techniques", "Wok cooking","Fry", "Drain","Heat"]

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

glb_ingredients=[]
glb_tools=[]
glb_methods =[]



#PPS: Remove the redudant suffix in given link
#Input:  URL
#Output: URL
def prettify_link(link):
    sep = '/?internal'  
    link = link.split(sep, 1)[0]
    return link

#PPS:Remove the leading space for all element in a list
#Input:   A list of strings(repents ingredients)
#Output:  A list of strings(repents ingredients)
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
#        item = ingredient.text.split(' ',1)[1]
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
        #     i[0] = '1'
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
            elif word.lower() in state_list:
                types.append("state")

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
    #     print key
    #     print ingredient_json[key]

    return ingredient_json

def getMethods(url):
    direction_list = getRecipe(url)[1]
    
    # for i in direction_list:
    #     print i
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

def getAllData(url):
    print "########## Recipe Data Representation (" + url + ") ##########"
    all_json = {}
    ingredients=getIngredients(url)
    methods=getMethods(url)
    tools=getTools(url)

    all_json.update({'ingredients':ingredients})
    all_json.update({'methods':methods})
    all_json.update({'tools':tools})
    
#    print all_json["ingredients"]
#    print all_json
    
#    glb_ingredients=all_json["ingredients"]
#    glb_tools      =all_json["tools"]
#    glb_methods    =all_json["methods"]

    # print "##### Extracting ingredients #####"
    # print all_json["ingredients"]
    # print "##### Extracting methods #####"
    # print all_json["methods"]
#    print "##### Extracting tools #####"
#    print all_json["tools"]
   
    # print ""
    return all_json

def transform(orig, sel):
    print "########## Recipe Transformation ##########"
    orig["tools"] = ['AAA', 'BBB']
    print orig

# original_recipe = getAllData('http://allrecipes.com/recipe/lasagna-alfredo/')
# original_recipe = getAllData('http://allrecipes.com/recipe/8732/poppy-seed-chicken')
#original_recipe = getAllData('http://allrecipes.com/recipe/66814/thai-crab-rolls')
#aLink='http://allrecipes.com/recipe/61071/addictive-sesame-chicken'

aLink='http://allrecipes.com/recipe/18114/butter-crescents/'
original_recipe = getAllData(aLink)


directions = getDirections(aLink)
directions_list=[]
index=1
#PPS: Get steps
for direction in directions:
    new_dir = removeLeadingBlank(direction.split("."))
    new_dir = filter(None, new_dir) # fastest
    for element in new_dir: 
        new_element=element+"."
        print str(index)+". "+new_element
        directions_list.append(str(index)+". "+new_element)         
        index=index+1

#==============================================================================
# The code fragment below is for HEALTHY transformation
#
#I would focus on ingredients and cooking method.
# 
# 1) Like you sad, frying -> boiling is a good idea, but there might be recipes where that doesn't work
# 2) Butter -> vegetable / peanut / olive oil, or maybe reducing the amount of butter, cream, sugar, etc (so long as you're not baking). You can even do Butter -> margarine as an easy one.
#==============================================================================



#print original_recipe["tools"]
glb_ingredients_dic           =original_recipe["ingredients"]
glb_ingredients_list          =[]
glb_ingredients_quantity_list =[]
glb_tools_list                =list(original_recipe["tools"])
glb_methods_list              =list(original_recipe["methods"])

#for index, ingredient in original_recipe["ingredients"].iteritems(): 
#    glb_ingredients.append(ingredient)
    
glb_ingredients_list.append("butter")
print len(glb_ingredients_dic)

#PPS: Get ingredient name
for index, value in glb_ingredients_dic.iteritems(): 
    merged_item=" ".join(value["item"])
    glb_ingredients_list.append(merged_item)
#    print merged_item

#print glb_ingredients_list

#PPS: Get ingredient quantity
for index, value in glb_ingredients_dic.iteritems(): 
    quantity=value["quantity"]
    glb_ingredients_quantity_list.append(quantity)
#    print quantity

#print glb_ingredients_quantity_list


#Approach replace Butter -> margarine

#==============================================================================
# #PPS:Update butter in steps
#==============================================================================
def update_steps():
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

#==============================================================================
# PPS:   Update quantity by increasing the denominator by 1
# Input: Fraction in string
# Output: Fraction in string               
#==============================================================================
def update_quantity(a_fraction):
    return str(update_fraction(a_fraction,1))


for index,vaule in enumerate(glb_ingredients_list):
    try:
        lower_ingredient= vaule.encode("utf-8").lower()
        if "butter" in lower_ingredient:
            #Update ingredient name list
            lower_ingredient=  lower_ingredient.replace("butter","margarine")
            glb_ingredients_list[index]=lower_ingredient
            print "The index is " +str(index)
            
            #Update dedicated quantity
            prev_quantity= glb_ingredients_quantity_list[index]            
            upd_quantity = update_quantity(prev_quantity)   
            glb_ingredients_quantity_list[index]=upd_quantity
#=======================Dubug=======================================================
# #            print "The quantity bf changing is "+prev_quantity
# #            print "The quantity after chaning is "+upd_quantity                        
#==============================================================================
            update_steps()
        else:
            pass
#            print "no butter in this recipe"
    except:
       print vaule+"contains non alphabet leter"          

print glb_ingredients_list
print glb_ingredients_quantity_list  

print "Directions after healthy transformation"
for step in directions_list:
    print step
#print directions_list 
#for ingredient in glb_ingredients_list:
#    try:
#       lower_ingredient= ingredient.encode("utf-8").lower()
#       if "butter" in lower_ingredient:
#           .replace(" and ","/")
#           replace_butter()
#           print "true"
#       else:
#           print "false"
#    except:
#       print ingredient+"contains non alphabet leter" 
  
       
##if "butter" in (x.lower() for x in glb_ingredients_list):
#if "butter" in glb_ingredients_list:    
#    print "true"
#print glb_ingredients_list
#print glb_ingredients
#print glb_tools
#print glb_methods

