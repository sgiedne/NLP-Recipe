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

italian_recipes      ="http://allrecipes.com/recipes/723/world-cuisine/european/italian"
real_ref_index=1






#Get all recipes of given cuisine category in link
def get_all_recipes(recipe_category_link):
    no_of_pagedowns = 100 #Decide how many steps to scroll down
    recipe_refs=[]
    
    driver = webdriver.Chrome("C:/Users/KU/Desktop/2017 Winter/NLP/Assignment 3/chromedriver_win32/chromedriver.exe") 
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






            


#Get the links for recipe categories
def get_category_links():
    links_ = set()
    names_ = set()
    real_ref_index=1
    
#    recipe_refs=[]
    
    driver = webdriver.Chrome("C:/Users/KU/Desktop/2017 Winter/NLP/Assignment 3/chromedriver_win32/chromedriver.exe")
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
        


#Print tf-idf value of given cuisine
def get_tfidf(cuisine, cuisine_link):
    print "Current cuisine is:"
    print cuisine
    ingedientDic = {}
    
    #Add ingedient to a dictionary
    def addToIngredientDic(ingedient):  
        key=ingedient.lower()
        if key in ingedientDic:
            ingedientDic[key]=ingedientDic[key]+1
        else:
            ingedientDic[key]=1
                        
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
    
    
    

get_tfidf("Itilian",italian_recipes)

