import sys
from random import choice
from random import sample
from os import system
from DrinkingBotGUI import runBot

def main():
    runBot(sys.argv, botAction)

def botAction(playTab, drinkers, bar, settings, says):
    playTab.clear()

    sayStack = ["Goaoaong."]
    
    if (isBonusRound(settings)):
        sayStack += ["Bonusround Bonusround!"] 
        sayStack += [doOnce(playTab, drinkers, bar, settings, says) for x in [1,2,3]]
    else:
        sayStack += [doOnce(playTab, drinkers, bar, settings, says)]

    sayStack += [ "Drink drink. Drink drink." ]

    if not( settings.quiet() ):
        say(settings.pauseCommand(), ". ".join(sayStack), settings.playCommand() )


def isBonusRound(settings):
    return (choice(range(0, int(1/settings.bonusrounds()) )) == 0)

def doOnce(playTab, drinkers, bar, settings, says):
    sentence = choice(says.contents())

    drink = choice(bar.contents())
    name = choose(history, drinkers.contents())
    substSentence = substitute(sentence, name, drink )

    if requiresAction(sentence):
        addHistory(history, playTab.gameRound(), name, drink)
        addRecord(record, name, drink)
        playTab.updateRecord(record)

    playTab.sayMore(substSentence)
    return substSentence


def say(pause, sentence, play):
    system("(" + pause + "; echo \"" + sentence + "\" | festival --tts; " + play + ") & ")


def choose(hist, drinkers):
 #   return choice(drinkers)
    return chooseFromHist(hist, sample(drinkers, len(drinkers)), 4)


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


def chooseFromHist(hist,drinkers,n):
    truncHist = [(name, weightedDrinksInLastRounds(hist,name,n)) for name in drinkers]
    m = min([x[1] for x in truncHist])
    truncHist = [(x[0], x[1]-m) for x in truncHist]
    weightedSum = sum([x[1] for x in truncHist])

    picked = choice(range(0,int(weightedSum+1)))
    i = 0
    tmp = truncHist[i][1]

    while (picked > tmp and i < (len(drinkers)-1)):
        i += 1
        tmp = tmp + truncHist[i][1]
    return truncHist[i][0]

def weightedDrinksInLastRounds(hist, name, n):
    if len(hist.keys()) == 0: maxRound = 0
    else: maxRound = max(hist.keys())
    def weight(x): #x is the round the drinking happened
        return (x - (maxRound - n))
    maxSum = 3 * sum ([weight(x) for x in range(maxRound - n +1,maxRound+1)])
    return maxSum - sum([ weight(x) * len(hist[x][name]) for x in hist.keys() 
                                if x > (maxRound - n) 
                                if name in hist[x].keys()])
history = {}

def addHistory(history, rnd, name, drink):
    if not rnd in history.keys():
        history[rnd] = {name:[drink]}
    elif not name in history[rnd].keys():
        history[rnd][name] = [drink]
    else:
        history[rnd][name].append(drink)


#    addHistory(history, 1, "Leonie", "Vodka")
#    addHistory(history, 1, "Chris", "Beer")
#    addHistory(history, 1, "Chris", "Beer")
#    addHistory(history, 2, "Leonie", "Vodka")
#    addHistory(history, 2, "Chris", "Beer")
#    print history
# prints
#    {1: {'Chris': ['Beer', 'Beer'], 'Leonie': ['Vodka']}, 
#     2: {'Chris': ['Beer'], 'Leonie': ['Vodka']}}



if __name__ == "__main__":
    main()