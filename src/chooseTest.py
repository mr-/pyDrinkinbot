from random import choice
def foo(hist, drinkers, n):
    return [(name, weightedDrinksInLastRounds(hist,name,n)) for name in drinkers]

def choose(hist, drinkers, n):
    return chooseFromHist(hist, drinkers, n)

def chooseFromHist(hist,drinkers,n):
    truncHist = [(name, weightedDrinksInLastRounds(hist,name,n)) for name in drinkers]
    m = min([x[1] for x in truncHist])/float(1.2)
    truncHist = [(x[0], x[1]) for x in truncHist]
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
        return 1 # (x - (maxRound - n))
    maxSum = 3 * sum ([weight(x) for x in range(maxRound - n +1,maxRound+1)])
    return sum([ weight(x) * len(hist[x][name]) for x in hist.keys() 
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

def props(h):
    s = sum([ h[x] for x in h.keys()])
    for x in sorted(h.keys()):
        print x + ": " + str(h[x]/float(s))

def stats(h):
    stat = {}
    for rnd in h.keys():
        for name in h[rnd]:
            if not name in stat.keys(): stat[name] = len(h[rnd][name])
            else: stat[name] += len(h[rnd][name]) 

    for name in sorted(stat.keys()):
        print name + ": " + str(stat[name])

def main():
    addHistory(history, 1, "Leonie", "Vodka")
    addHistory(history, 1, "Chris", "Beer")
    addHistory(history, 1, "Chris", "Beer")
    addHistory(history, 2, "Leonie", "Vodka")
    addHistory(history, 2, "Chris", "Beer")
    addHistory(history, 2, "Tudy", "Beer")
    h = {}
    for x in range(0,100000):
        n = choose(history, ["Leonie", "Chris", "Tudy"], 3)
        if not n in h.keys(): h[n]=1
        else: h[n]+=1

    print "Stats:"
    stats(history)
    print "Propabilities:"
    props(h) 


main()