import re

#Encrypted program
def message(text, plain, encryp):
    dictionary = dict(zip(plain, encryp))
    newmessage = ''
    for char in text:
        try:
            newmessage += dictionary[char]
        except:
            newmessage += ' '
    print(text + '\nhas been encrypted to:')
    print(newmessage)

text = "Hello, Nuertey is bored, and unsurprisingly, he is quite dangerous when bored."

text = re.sub("[\[].*?[\]]", "", text) ## Remove brackets and anything inside it (to remove the citations)
# You can do more cleaning (like lemmatization, stemming, stopword removal, etc if you want)
 
message(text)

#Python Assistant
#Get a method and its documentation for a particular use case without remembering its name or even the module it belongs to.

## Get a list of all available modules
#help('modules')
## Import a module from the list of modules
#import <name of module>
## Get the available class/functions of the module
#dir(<name of module>)
## Get the documentation of the class/method of the module
#help(<name of module>.<class/method in module>)
