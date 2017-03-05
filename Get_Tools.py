'''
Pending improvements

- Eureka, 3/4/2017
Not sure how to get a match if a tool has more than one word (e.g., "baking dish")

'''

from bs4 import BeautifulSoup
import urllib2
from nltk.tokenize import word_tokenize

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
	words = word_tokenize(direction.text)
	directions.append(words)

# Transform all the words in the directions from unicode into strings
directions_str = []
i = 0
while i < len(directions):
	for word in directions[i]:
		directions_str.append(str(word))
	i += 1
    
# Check if each word in directions_str is in the kitchenware list
for word in directions_str: 
	if word.lower() in (tool.lower() for tool in completeKitchenWare):
	    kitchenWareIncluded.append(word)

# Print out the list of included tools
print ("The tools included in this receipt are:")
if len(kitchenWareIncluded) == 0:
    print ("none")
else:
    for kitchenWare in kitchenWareIncluded:
        print(kitchenWare)
