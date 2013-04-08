import sys
from random import choice
from os import system
from GUI import runBot

def main():
    runBot(sys.argv, botAction)

def botAction(genTab, drinkers, bar, settings, says):
    genTab.clear()

    sayStack = ["Goaoaong."]
    
    if (isBonusRound(settings)):
        sayStack += ["Bonusround Bonusround!"] 
        sayStack += [doOnce(genTab, drinkers, bar, settings, says) for x in [1,2,3]]
    else:
        sayStack += [doOnce(genTab, drinkers, bar, settings, says)]

    sayStack += [ "Drink drink. Drink drink." ]
    if not( settings.quiet() ):
        say(settings.fadeCommand(), ". ".join(sayStack) )


def isBonusRound(settings):
    return (choice(range(0, int(1/settings.bonusrounds()) )) == 0)

def doOnce(genTab, drinkers, bar, settings, says):
    sentence = choice(says.contents())

    drink = choice(bar.contents())
    name = choice(drinkers.contents())
    substSentence = substitute(sentence, name, drink )

    if requiresAction(sentence):
        addRecord(record, name, drink)
        genTab.updateRecord(record)

    genTab.sayMore(substSentence)
    return substSentence

def requiresAction(sentence):
    return "NAME" in sentence and "DRINK" in sentence

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

def say(fc, sentence):
    system(fc + " && echo \"" + sentence + "\" | festival --tts && " + fc + " & ")



if __name__ == "__main__":
    main()