from random import choice
def foo(hist, drinkers, n):
    return [(name, weightedDrinksInLastRounds(hist,name,n)) for name in drinkers]

def choose(hist,drinkers,n):
    truncHist = [(name, weightedDrinksInLastRounds(hist,name,n)) for name in drinkers]
    weightedSum = sum([x[1] for x in truncHist])
    picked = choice(range(0,weightedSum+1))

    i = 0
    tmp = truncHist[i][1]

    while (picked > tmp and i < (len(drinkers)-1)):
        i += 1
        tmp = tmp + truncHist[i][1]

    return truncHist[i][0]

def weightedDrinksInLastRounds(hist, name, n):
    maxRound = max(hist.keys())
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

def main():
    addHistory(history, 1, "Leonie", "Vodka")
    addHistory(history, 1, "Chris", "Beer")
    addHistory(history, 1, "Chris", "Beer")
    addHistory(history, 2, "Leonie", "Vodka")
    addHistory(history, 2, "Chris", "Beer")
    h = {}
    for x in range(0,100000):
        n = choose(history, ["Leonie", "Chris", "Tudy"], 2)
        if not n in h.keys(): h[n]=1
        else: h[n]+=1

    print h
    i =  foo(history, ["Leonie", "Chris", "Tudy"], 2)
    print i

main()