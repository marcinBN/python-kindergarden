#!/usr/bin/python3
#-*- coding: utf-8 -*-

# Knapsack problem

class Item:
    def __init__(self, label, weight, value):
        self.label = label
        self.weight = weight
        self.value = value

class Bag:
    def __init__(self, cap):
        self.cap = cap
        self.items = []
    def value(self):
        res = 0
        for item in self.items:
            res += item.value
        return res
    def weight(self):
        res = 0
        for item in self.items:
            res += item.weight
        return res
    def freespace(self):
        return self.cap - self.weight()
        

def knapsack():
    v = [3, 4, 8, 8, 10]
    w = [2, 3, 4, 5, 9]
    n = 5
    cap = 20
    m = [[0 for x in range(cap+1)] for z in range(n+1)]

    for j in range(cap+1):
        m[0][j] = j
    for k in m:
        print(k)
    for i in range(n):
        print(i)
        for j in range(cap+1):
            if w[i] <= j:
                m[i][j] = max(m[i-1][j], m[i-1][j-w[i]] + v[i])
            else:
                m[i][j] = m[i-1][j]
    for p in m:
        print(p)

#knapsack()

#items = label, weight, value
items = [
Item('10$ banknot', 2, 3),
Item('memoryCard', 3, 4),
Item('smartphone', 4, 8),
Item('camera', 5, 8),
Item('notebook', 9, 10)
]

bag = Bag(20)

def solveProblem(items, cap):
    
    res = [[] for i in range(len(items)+1)]
    #res.insert(0, [Bag(capp) for capp in range(cap+1)])

    for c in range(cap+1):
        currentBag = Bag(c)
        best = Item('nothing', 0, 0)
        for fitItem in [i for i in items if i.weight<=currentBag.cap]:
            if fitItem.value > best.value:
                best = fitItem
        currentBag.items.append(best)
        res[1].append(currentBag)
    for nitems in range(2, len(items)+1):
        for c in range(cap+1):
            prevFreespace = res[nitems-1][c].freespace()
            prevItems = res[nitems-1][c].items
            
            taken = res[1][prevFreespace].items
            best = Item('nothing', 0, 0)
            for fitItem in [i for i in items if i.weight<=prevFreespace and i.label not in [i.label for i in prevItems]]:
                if fitItem.value > best.value:
                    best = fitItem
            newBag = Bag(c)
            addItem = [best]
            if best.label != 'nothing':
                summa = prevItems + [best]
            else:
                summa = prevItems
            newBag.items = summa
            out = newBag
            if c > 0:
                prev2Freespace = res[nitems-1][c-1].freespace()
                temp = res[nitems-1][c-1].items 
                
                best = Item('nothing', 0, 0)
                for fitItem in [i for i in items if i.weight<=prev2Freespace+1 and i.label not in [i.label for i in temp]]:
                    if fitItem.value > best.value:
                        best = fitItem
                temp = res[nitems-1][c-1].items + [best]
                newBag2 = Bag(c)
                newBag2.items = temp
                if newBag2.value() > newBag.value():
                    out = newBag2
            
            
            
            res[nitems].append(out)
    
    resBag = res[len(items)][cap]
    print('Knapsack cap={}'.format(resBag.cap))
    print('Number of taken items={}'.format(len(resBag.items)))
    print('Value={}'.format(resBag.value()))
    print('Items:')
    for item in resBag.items:
        print('{}; weight={}; value={}'.format(item.label, item.weight, item.value))


    
    return res 

mapp = solveProblem(items, 20)
#for bag in mapp[2]:
#    print(bag.cap, len(bag.items), bag.value())

