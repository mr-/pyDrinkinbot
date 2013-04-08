import sys
from random import choice
from os import system
from GUI import runBot

def main():
    runBot(sys.argv, botAction)

def botAction(genTab, drinkers, bar, settings, says):
    drink = choice(bar.contents())
    name = choice(drinkers.contents())
    sentence = choice(says.contents())
    ns = substitute(sentence, name, drink )
    genTab.say(ns)
    addRecord(record, name, drink)
    genTab.updateRecord(record)
    say( "Goaoaong. " + ns + ". Drink drink. Drink drink.")

def substitute(s1, name, drink):
    s2 = s1.replace("NAME", name)
    s3 = s2.replace("DRINK", drink)
    return s3

record = {}
#        record = {
#            'Tudy':[("Vodka",9)],
#            'Martin':[("Wine",2), ("Vodka",3)],
#            'Leonie':[("Beer",4)],
#            }  
def addRecord(record, name, drink):
    if not(name in record.keys()):
        record[name] = [(drink, 1)]
    elif not(drink in [ x[0] for x in record[name] ]):
        record[name].append((drink,1))
    else:
        ele = next( x for x in record[name] if x[0] == drink)
        record[name].remove(ele)
        record[name].append((ele[0], ele[1]+1))

def say(sentence):
    system("echo " + sentence + " | festival --tts & ")



if __name__ == "__main__":
    main()