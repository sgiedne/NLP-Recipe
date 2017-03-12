# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:02:10 2017

@author: KU
"""

#Ref:http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/
#    http://stackoverflow.com/questions/31137552/unicodeencodeerror-ascii-codec-cant-encode-character-at-special-name
#Ref:http://stackoverflow.com/questions/21006940/how-to-load-all-entries-in-an-infinite-scroll-at-once-to-parse-the-html-in-pytho
#Approach handle the blank space in CSS decoration
#REF: http://stackoverflow.com/questions/7475449/webdriver-classname-with-space-using-java
import os
import math
from textblob import TextBlob as tb
from bs4 import BeautifulSoup
import urllib2
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import operator
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from sets import Set
import csv


#common_meausurements = ['package','cup','cups','teaspoon','teaspoons',
#                        'tablespoon','tablespoons','clove','cloves','ounce',
#                        'ounces','liter','liters','ml','pint',
#                        'pints','quart','quarts','pound','pounds',
#                        'slice','slices','can','cans','container',
#                        'containers','jars']

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

state_list = ["broth", "soup"]

#italian_recipes      ="http://allrecipes.com/recipes/723/world-cuisine/european/italian"
real_ref_index=1
chrome_driver_path="C:/Users/KU/Desktop/2017 Winter/NLP/Assignment 3/chromedriver_win32/chromedriver.exe" #Path to local Chrome Driver



#Helper functions

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










#Get all recipes of given cuisine category in link
def get_all_recipes(recipe_category_link):
    no_of_pagedowns = 100 #Decide how many steps to scroll down
    recipe_refs=[]
    recipe_refs_dic={}
    
    driver = webdriver.Chrome(chrome_driver_path) #Path to local Chrome Driver
    driver.get(recipe_category_link)  
    time.sleep(1)
    
    #Drag down the page to expose enough receipts
    elem = driver.find_element_by_tag_name("body")
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1
    
    #Get the exposed receipts
    recipe_elems = driver.find_elements_by_class_name("grid-col--fixed-tiles")   
    recipe_num=len(recipe_elems)
    print "The number of exposed recipes are:"
    print recipe_num
    
    for index in range(0,recipe_num):  
        #Filter out the advertisement 
        try:
            recipe_name= recipe_elems[index].find_element_by_css_selector('h3').text #Feature to differentiate ads and recipes
            href_list  = recipe_elems[index].find_elements_by_css_selector('a')       
            real_href  = href_list[real_ref_index].get_attribute('href') #Get the link
            real_href  = prettify_link(real_href) #Clean the link
            recipe_refs.append(real_href)   
            recipe_refs_dic[recipe_name]=real_href    
        except NoSuchElementException:
            pass
            
    driver.close()
#    return recipe_refs
    return recipe_refs_dic













    



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

def getIngredients(url):

    p1 = re.compile('\([0-9]* ounce(|s)\)')
    raw_ingredients = getRecipe(url)[0]
    direction_list = getRecipe(url)[1]
    ingredients = []
    ingredient_names=[]

    for i in raw_ingredients:
        ingredient = []
        measures = []
        prep = []
        desc = []
        types = []

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
        ingredient_item = []
        for chunk in item_chunks:
            if(chunk[1]=='VBD' or chunk[1]=='RB'):
                desc.append(chunk[0])
                item = item.replace(chunk[0],"").replace(',','').strip()

            it = []
            if(chunk[1] in ['NN','NNS','JJ','NNP']):
                it.append(chunk[0])
          
#            print len(str_list)
#            print ''.join(str_list)
            
            ingredient_item.append(' '.join(it))
#            ingredient_names.append(' '.join(it))

        # get preparation
        item = item.lstrip(' ');
        #print item
        ingredient_names.append(item)
      
        

    return ingredient_names

##Purpose（PPS_: Get all ingredients in given recipes
##Input: URL (a recipe link)
##Output: A list of ingredients
#def getIngredients(url):
#    #List store the ingredient name
#    receipt_ingredients=[]
#    
#    p1 = re.compile('\([0-9]* ounce(|s)\)')
#    raw_ingredients = getrecipe(url)[0]
#    ingredients = []
#    for i in raw_ingredients:
#        
#        ingredient = []
#        measures = []
#        prep = []
#
#        #get quantity
#        ingredient.append(i[0])
#        
#        item = i[1]
#
#        #get measures
#        split_word = ''
#        if(p1.match(item)):
#               measures.append(p1.search(item).group())
#               item = item.split(p1.search(item).group())[1]
#            
#        for word in item.split():
#            for measure in common_meausurements:
#                if(word == measure):
#                    measures.append(measure)
#                    split_word = measure
#        ingredient.append(measures)
#        if(split_word != ''):
#            item = item.split(split_word)[1]
#
#        #get descriptors/preparation
#        item_chunks = pos_tag(word_tokenize(item))
#        for chunk in item_chunks:
#            if(chunk[1]=='VBD' or chunk[1]=='RB'):
#                prep.append(chunk[0])
#                item = item.replace(chunk[0],"").replace(',','').strip()
#        ingredient.append(prep)
#        ingredient.append(item)
#        receipt_ingredients.append(item)        
#        ingredients.append(ingredient)
#    
#    #clear the leading white space
#    receipt_ingredients=removeLeadingBlank(receipt_ingredients)
#    
#    return receipt_ingredients






            


#PPS： Get the links for each recipe category
#Input: link (the root page of allrecipes site)
#Output: Dictionary（key is the name of cuisine type in continent, value is the link, e.g. Key[Asian Cuisine="url") 
def get_category_links(root_page):
    recipe_link_dic={}
    links_ = set()
    names_ = set()
    real_ref_index=1
    
#    recipe_refs=[]
    
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get(root_page)  
    time.sleep(1)
    
    recipe_elems = driver.find_element_by_css_selector("div[class='grid slider desktop-view']")
    
                 
    items = recipe_elems.find_elements_by_tag_name("li")
    
    for item in items:
        href = item.find_element_by_css_selector('a') 
        category_name=item.find_element_by_class_name("category-title").get_attribute("innerHTML")      
        real_href=href.get_attribute('href')       
        names_.add(category_name)
     
        real_href=prettify_link(real_href)
        links_.add(real_href)
        recipe_link_dic[category_name]=real_href
    #driver.close()
    return recipe_link_dic     
        
#TFIDF Procedures
def tf(word, blob):
    return (float)(blob.words.count(word)) / (float)(len(blob.words))

def n_containing(word, bloblist):
    return (float)(sum(1 for blob in bloblist if word in blob))

def idf(word, bloblist):
    return (float)(math.log(len(bloblist)) / (float)(1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return (float)((float)(tf(word, blob)) * (float)(idf(word, bloblist)))

#Print tf-idf value of given cuisine
def get_tfidf(cuisine, cuisine_link):
    #print "Current cuisine is:"
    #print cuisine
    ingedientDic = {}
    
    #Add ingedient to a dictionary
    def addToIngredientDic(ingedient):  
        key=ingedient.lower()
        if key in ingedientDic:
            ingedientDic[key]=ingedientDic[key]+1
        else:
            ingedientDic[key]=1
    
    #Get all recipes                   
    recipes_links=get_all_recipes(cuisine_link)
    
    
    recipe_collections =[]
    recipe_ingredient_collections =[]
    recipe_ingredient_collections_in_doc =[]
    
    for recipe_link in recipes_links:
        recipe_collections.append(getIngredients(recipe_link))
        
    for recipe in recipe_collections:
        recipe_ingredient_collections.append(' '.join(recipe))
    
    for recipe_ingredient in recipe_ingredient_collections:
        recipe_ingredient_collections_in_doc.append(tb(recipe_ingredient))
    
    bloblist=recipe_ingredient_collections_in_doc
    
    for i, blob in enumerate(bloblist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:3]:
            addToIngredientDic(word)
            print("Word: {}, TF-IDF: {}".format(word.encode('utf-8'), round(score, 5)))
        print('')
    
    
    
    sorted_ingdtDic = sorted(ingedientDic.items(), key=operator.itemgetter(1),reverse=True)
    print(sorted_ingdtDic)

#PPS: Create the given "path" if necessary
#Input: string (as path)
#Output: None
def createDir(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
            
            
#def get_all_cuisines_link(cuisine_type_links):
#     for key, value in cuisine_type_links.iteritems():
    
    
#Main program

#get_tfidf("Itilian",italian_recipes)

root_page="http://allrecipes.com/recipes/86/world-cuisine"

#Get world cuisine type
cuisine_type_in_continent=get_category_links(root_page)

#all_cuisines_link=get_all_cuisines_link(cuisine_type_in_continent)

#dubug
#for key, value in cuisine_type_in_continent.iteritems():    
#    print key+" "+value
print "Start get cuisine links FOR continent"


        


createDir('./result/')
    
with open('./result/world_cuisine.csv', 'w') as csvfile:
    fieldnames = ['Cuisine Type', 'URL']
    writer = csv.DictWriter(csvfile,lineterminator='\n', fieldnames=fieldnames)

    writer.writeheader()
    
    for key, value in cuisine_type_in_continent.iteritems():    
        writer.writerow({'Cuisine Type': key.encode("utf-8"), 'URL': value.encode("utf-8")})

print "Done writting continent cuisine in csv file"

print "Start get cuisine links IN each continent"

#Get cuisines among the continent
for key_continent, value in cuisine_type_in_continent.iteritems(): 
#    if("Middle Eastern Recipes"==key_continent):
#        pass
#    else if("Latin American Recipes"==key_continent):
#        pass
#    else if("Australian and New Zealander Recipes"==key_continent):
#        pass
#    else:
        print "Start writting for "+ key_continent+" cuisine"
        cuisine_in_continent=get_category_links(value)
        
        
        csv_name='./result/'+key_continent+'_cuisine.csv'
        with open(csv_name, 'w') as csvfile:
            fieldnames = ['Cuisine Type', 'URL']
            writer = csv.DictWriter(csvfile,lineterminator='\n', fieldnames=fieldnames)
        
            writer.writeheader()
            
            for country, country_link in cuisine_in_continent.iteritems():    
                writer.writerow({'Cuisine Type': country.encode("utf-8"), 'URL': country_link.encode("utf-8")})
    
        #Get recipes for each country
        for key_country, value_country_link in cuisine_in_continent.iteritems(): 
            print "Get recipe links for "+key_country+ " in "+key_continent
            recipes_dic=get_all_recipes(value_country_link)
            #recipe_ingredient= getIngredients(value)
            continent_dir='./result/'+key_continent+'/'
            createDir(continent_dir)
            csv_name=continent_dir+key_country+'_recipe_links.csv'
            with open(csv_name, 'w') as csvfile:
                fieldnames = ['Recipe', 'URL']
                writer = csv.DictWriter(csvfile,lineterminator='\n', fieldnames=fieldnames)
            
                writer.writeheader()
                
                
                for recipe_name, recipe_link in recipes_dic.iteritems():    
                    writer.writerow({'Recipe': recipe_name.encode("utf-8"), 'URL': recipe_link.encode("utf-8")})
            
            
            
            country_dir=continent_dir+key_country+'/'
            createDir(country_dir)
            recipes_csv_name=country_dir+key_country+'_ingredients.csv'
            
            
            for recipe_name, recipe_link in recipes_dic.iteritems(): 
                print recipe_link
                
            print "Get ingredients for "+key_country+ " in "+key_continent
            with open(recipes_csv_name, 'w') as csvfile:
                fieldnames = ['Recipe Name', 'Ingredient','URL']
                writer = csv.DictWriter(csvfile,lineterminator='\n', fieldnames=fieldnames)
            
                writer.writeheader()
                
              
                for recipe_name, recipe_link in recipes_dic.iteritems(): 
                    print recipe_link
                    try:
                        ingredients= getIngredients(recipe_link)
                        
                        for ingredient in ingredients:
                            writer.writerow({'Recipe Name': recipe_name.encode("utf-8"), 'Ingredient': ingredient.encode("utf-8"), 'URL': recipe_link.encode("utf-8")}) 
    #                except ValueError:
                    except:
                        print "Error link is : "+ recipe_link
                        csv_name='./result/error_link.csv'
                  
#print len(cuisine_type_in_European)
##dubug
#for key, value in cuisine_type_in_European.iteritems():
#    print key+","+value



#for key, value in all_cuisines_dic.iteritems():
#    print "Current cuisine category is", key 
#    print value
#    #current_cuisine_dic=get_all_recipes(value)
#    get_tfidf(key,value)
#    
#    print "---------------------------------------------"