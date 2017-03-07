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

#Helper functions
#Clear the redudant suffix
def prettify_link(link):
    sep = '/?internal'  
    link = link.split(sep, 1)[0]
    return link
#Remove the leading space for all element in a list
def removeLeadingBlank(ingredientList):
    updated_ingredientList=[]
    for ingredient in ingredientList:
        updated_ingredientList.append(ingredient.lstrip(' '))
    return updated_ingredientList



common_meausurements = ['package','cup','cups','teaspoon','teaspoons',
                        'tablespoon','tablespoons','clove','cloves','ounce',
                        'ounces','liter','liters','ml','pint',
                        'pints','quart','quarts','pound','pounds',
                        'slice','slices','can','cans','container',
                        'containers','jars']

# italian_recipes      ="http://allrecipes.com/recipes/723/world-cuisine/european/italian"

# African
# italian_recipes      ="http://allrecipes.com/recipes/15039/world-cuisine/african/north-african/egyptian/"
#"http://allrecipes.com/recipes/1827/world-cuisine/african/north-african/moroccan/"
italian_recipes      ="http://allrecipes.com/recipes/17475/world-cuisine/african/main-dishes/"
# http://allrecipes.com/recipes/17477/world-cuisine/african/soups-and-stews/
# http://allrecipes.com/recipes/17845/world-cuisine/african/east-african/
# http://allrecipes.com/recipes/15035/world-cuisine/african/south-african/
# http://allrecipes.com/recipes/17476/world-cuisine/african/side-dishes/

# Asian
# http://allrecipes.com/recipes/695/world-cuisine/asian/chinese/
# http://allrecipes.com/recipes/699/world-cuisine/asian/japanese/
# http://allrecipes.com/recipes/700/world-cuisine/asian/korean/
# http://allrecipes.com/recipes/16100/world-cuisine/asian/bangladeshi/
# http://allrecipes.com/recipes/233/world-cuisine/asian/indian/
# http://allrecipes.com/recipes/15937/world-cuisine/middle-eastern/persian/
# http://allrecipes.com/recipes/15974/world-cuisine/asian/pakistani/
# http://allrecipes.com/recipes/696/world-cuisine/asian/filipino/
# http://allrecipes.com/recipes/698/world-cuisine/asian/indonesian/
# http://allrecipes.com/recipes/701/world-cuisine/asian/malaysian/
# http://allrecipes.com/recipes/702/world-cuisine/asian/thai/
# http://allrecipes.com/recipes/703/world-cuisine/asian/vietnamese/




real_ref_index=1

ingedientDic = {}




#Get all recipes of given cuisine category in link
def get_all_recipes(recipe_category_link):
    no_of_pagedowns = 100 #Decide how many steps to scroll down
    recipe_refs=[]

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome("C:/Users/KU/Desktop/2017 Winter/NLP/Assignment 3/chromedriver_win32/chromedriver.exe") 
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
                
        except NoSuchElementException:
            pass
            
    driver.close()
    return recipe_refs





#TFIDF Procedures
def tf(word, blob):
    return (float)(blob.words.count(word)) / (float)(len(blob.words))

def n_containing(word, bloblist):
    return (float)(sum(1 for blob in bloblist if word in blob))

def idf(word, bloblist):
    return (float)(math.log(len(bloblist)) / (float)(1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return (float)((float)(tf(word, blob)) * (float)(idf(word, bloblist)))







    

def getrecipe(url):    
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

    recipe = []
    recipe.append(ingredients)
    recipe.append(directions)

    return recipe


def getIngredients(url):
    #List store the ingredient name
    receipt_ingredients=[]
    
    p1 = re.compile('\([0-9]* ounce(|s)\)')
    raw_ingredients = getrecipe(url)[0]
    ingredients = []
    for i in raw_ingredients:
        
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
        receipt_ingredients.append(item)        
        ingredients.append(ingredient)
    
    #clear the leading white space
    receipt_ingredients=removeLeadingBlank(receipt_ingredients)
    
    return receipt_ingredients





#Add ingedient to a dictionary
def addToIngredientDic(ingedient):  
        key=ingedient.lower()
        if key in ingedientDic:
            ingedientDic[key]=ingedientDic[key]+1
        else:
            ingedientDic[key]=1
            


#Get the links for recipe categories
def get_category_links():
    links_ = set()
    names_ = set()
    real_ref_index=1
    
    recipe_refs=[]
    
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome("C:/Users/KU/Desktop/2017 Winter/NLP/Assignment 3/chromedriver_win32/chromedriver.exe")
    driver.get("http://allrecipes.com/recipes/86/world-cuisine")  
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
    return links_     
        



ingredient_list1='http://allrecipes.com/recipe/lasagna-alfredo/'
ingredient_list2='http://allrecipes.com/recipe/234312/how-to-make-focaccia/'
ingredient_list3='http://allrecipes.com/recipe/222680/bon-appetits-meatballs'
ingredient_list4='http://allrecipes.com/recipe/246528/stracciatella-soup/'
ingredient_list5='http://allrecipes.com/recipe/126942/ricotta-gnocchi/'
ingredient_list6='http://allrecipes.com/recipe/21412/tiramisu-ii/'
ingredient_list7='http://allrecipes.com/recipe/246628/spaghetti-cacio-e-pepe/'
ingredient_list8='http://allrecipes.com/recipe/246866/rigatoni-alla-genovese/'
ingredient_list9='http://allrecipes.com/recipe/17167/sicilian-spaghetti/'
ingredient_list10='http://allrecipes.com/recipe/7245/jays-signature-pizza-crust/'
ingredient_list11='http://allrecipes.com/recipe/23600/worlds-best-lasagna/'
ingredient_list12='http://allrecipes.com/recipe/8887/chicken-marsala/'
ingredient_list13='http://allrecipes.com/recipe/20669/double-tomato-bruschetta/'
ingredient_list14='http://allrecipes.com/recipe/25321/eggplant-parmesan-ii/'
ingredient_list15='http://allrecipes.com/recipe/70522/garlic-cheddar-chicken/'

# ingredient_list1='http://allrecipes.com/recipe/lasagna-alfredo/'
# ingredient_list2='http://allrecipes.com/recipe/234312/how-to-make-focaccia/'
# ingredient_list3='http://allrecipes.com/recipe/222680/bon-appetits-meatballs'
# ingredient_list4='http://allrecipes.com/recipe/246528/stracciatella-soup/'
# ingredient_list5='http://allrecipes.com/recipe/126942/ricotta-gnocchi/'
# ingredient_list6='http://allrecipes.com/recipe/21412/tiramisu-ii/'
# ingredient_list7='http://allrecipes.com/recipe/246628/spaghetti-cacio-e-pepe/'
# ingredient_list8='http://allrecipes.com/recipe/246866/rigatoni-alla-genovese/'
# ingredient_list9='http://allrecipes.com/recipe/17167/sicilian-spaghetti/'
# ingredient_list10='http://allrecipes.com/recipe/7245/jays-signature-pizza-crust/'
# ingredient_list11='http://allrecipes.com/recipe/23600/worlds-best-lasagna/'
# ingredient_list12='http://allrecipes.com/recipe/8887/chicken-marsala/'
# ingredient_list13='http://allrecipes.com/recipe/20669/double-tomato-bruschetta/'
# ingredient_list14='http://allrecipes.com/recipe/25321/eggplant-parmesan-ii/'
# ingredient_list15='http://allrecipes.com/recipe/70522/garlic-cheddar-chicken/'

recipes_links=get_all_recipes(italian_recipes)
# recipes_links=[ingredient_list1,ingredient_list2,ingredient_list3,ingredient_list4,ingredient_list5,
#                ingredient_list6,ingredient_list7,ingredient_list8,ingredient_list9,ingredient_list10 ,
#                ingredient_list11,ingredient_list12,ingredient_list13,ingredient_list14,ingredient_list15]

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
print "COME HERE 1"
# print(sorted_ingdtDic)
for i in sorted_ingdtDic:
    print i[0]
    
    
    
##Italian recipes
#ingredient_list1=getIngredients('http://allrecipes.com/recipe/lasagna-alfredo/')
#ingredient_list2=getIngredients('http://allrecipes.com/recipe/234312/how-to-make-focaccia/')
#ingredient_list3=getIngredients('http://allrecipes.com/recipe/222680/bon-appetits-meatballs')
#ingredient_list4=getIngredients('http://allrecipes.com/recipe/246528/stracciatella-soup/')
##ingredient_list5=getIngredients('http://allrecipes.com/recipe/126942/ricotta-gnocchi/') Get ingredient function error (ppp: two eggs)
#ingredient_list6=getIngredients('http://allrecipes.com/recipe/21412/tiramisu-ii/')
#ingredient_list7=getIngredients('http://allrecipes.com/recipe/246628/spaghetti-cacio-e-pepe/')
#ingredient_list8=getIngredients('http://allrecipes.com/recipe/246866/rigatoni-alla-genovese/')
#ingredient_list9=getIngredients('http://allrecipes.com/recipe/17167/sicilian-spaghetti/')
#ingredient_list10=getIngredients('http://allrecipes.com/recipe/7245/jays-signature-pizza-crust/')
#ingredient_list11=getIngredients('http://allrecipes.com/recipe/23600/worlds-best-lasagna/')
#ingredient_list12=getIngredients('http://allrecipes.com/recipe/8887/chicken-marsala/')
#ingredient_list13=getIngredients('http://allrecipes.com/recipe/20669/double-tomato-bruschetta/')
#ingredient_list14=getIngredients('http://allrecipes.com/recipe/25321/eggplant-parmesan-ii/')
#ingredient_list15=getIngredients('http://allrecipes.com/recipe/70522/garlic-cheddar-chicken/')
#ingredient_list5=getIngredients('http://allrecipes.com/recipe/85389/gourmet-mushroom-risotto/')
#
#
#rcp1=' '.join(ingredient_list1)
#rcp2=' '.join(ingredient_list2)
#rcp3=' '.join(ingredient_list3)
#rcp4=' '.join(ingredient_list4)
#rcp5=' '.join(ingredient_list5)
#rcp6=' '.join(ingredient_list6)
#rcp7=' '.join(ingredient_list7)
#rcp8=' '.join(ingredient_list8)
#rcp9=' '.join(ingredient_list9)
#rcp10=' '.join(ingredient_list10)
#rcp11=' '.join(ingredient_list11)
#rcp12=' '.join(ingredient_list12)
#rcp13=' '.join(ingredient_list13)
#rcp14=' '.join(ingredient_list14)
#rcp15=' '.join(ingredient_list15)
#
#document1 = tb(rcp1)
#document2 = tb(rcp2)
#document3 = tb(rcp3)
#document4 = tb(rcp4)
#document5 = tb(rcp5)
#document6 = tb(rcp6)
#document7 = tb(rcp7)
#document8 = tb(rcp8)
#document9 = tb(rcp9)
#document10 = tb(rcp10)
#document11 = tb(rcp11)
#document12 = tb(rcp12)
#document13 = tb(rcp13)
#document14 = tb(rcp14)
#document15 = tb(rcp15)
#
#
#print(document1)
#
#
#bloblist = [document1,  document2,  document3,
#            document4,  document5,  document6,
#            document7,  document8,  document9,
#            document10, document11, document12,
#            document13, document14, document15]
#
#
#for i, blob in enumerate(bloblist):
#    print("Top words in document {}".format(i + 1))
#    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
#    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#    for word, score in sorted_words[:3]:
#        addToIngredientDic(word)
#        print("Word: {}, TF-IDF: {}".format(word.encode('utf-8'), round(score, 5)))
#    print('')
#
#
#
#sorted_ingdtDic = sorted(ingedientDic.items(), key=operator.itemgetter(1),reverse=True)
#print(sorted_ingdtDic)




