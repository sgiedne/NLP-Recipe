#Ref:http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/
import math
from textblob import TextBlob as tb

from bs4 import BeautifulSoup
from urllib.request import urlopen


import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk

import operator

common_meausurements = ['package','cup','cups','teaspoon','teaspoons',
                        'tablespoon','tablespoons','clove','cloves','ounce',
                        'ounces','liter','liters','ml','pint',
                        'pints','quart','quarts','pound','pounds',
                        'slice','slices','can','cans','container',
                        'containers','jars']


def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


#Remove the leading space for all element in a list
def removeLeadingBlank(ingredientList):
    updated_ingredientList=[]
    for ingredient in ingredientList:
        updated_ingredientList.append(ingredient.lstrip(' '))
    return updated_ingredientList





def getrecipe(url):    
    page = urlopen(url).read()
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
    #List store the ingredient name
    receipt_ingredients=[]
    
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
#    for i in ingredients:
#        print (i)



ingedientDic = {}

#Rank the popularity of the ingedient
def addToIngredientDic(ingedient):  
        key=ingedient.lower()
        if key in ingedientDic:
            ingedientDic[key]=ingedientDic[key]+1
        else:
            ingedientDic[key]=1
            

#Italian recipes
ingredient_list1=getIngredients('http://allrecipes.com/recipe/lasagna-alfredo/')
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


rcp1=' '.join(ingredient_list1)
rcp2=' '.join(ingredient_list2)
rcp3=' '.join(ingredient_list3)
rcp4=' '.join(ingredient_list4)
rcp5=' '.join(ingredient_list5)
rcp6=' '.join(ingredient_list6)
rcp7=' '.join(ingredient_list7)
rcp8=' '.join(ingredient_list8)
rcp9=' '.join(ingredient_list9)
rcp10=' '.join(ingredient_list10)
rcp11=' '.join(ingredient_list11)
rcp12=' '.join(ingredient_list12)
rcp13=' '.join(ingredient_list13)
rcp14=' '.join(ingredient_list14)
rcp15=' '.join(ingredient_list15)

document1 = tb(rcp1)
document2 = tb(rcp2)
document3 = tb(rcp3)
document4 = tb(rcp4)
document5 = tb(rcp5)
document6 = tb(rcp6)
document7 = tb(rcp7)
document8 = tb(rcp8)
document9 = tb(rcp9)
document10 = tb(rcp10)
document11 = tb(rcp11)
document12 = tb(rcp12)
document13 = tb(rcp13)
document14 = tb(rcp14)
document15 = tb(rcp15)


print(document1)


bloblist = [document1,  document2,  document3,
            document4,  document5,  document6,
            document7,  document8,  document9,
            document10, document11, document12,
            document13, document14, document15]


for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        addToIngredientDic(word)
        print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
    print('')

#print(ingedientDic)

sorted_ingdtDic = sorted(ingedientDic.items(), key=operator.itemgetter(1),reverse=True)
print(sorted_ingdtDic)