#!/usr/bin/python3
#-*- coding: utf-8 -*-

from queues import *

time = 0
waitingList = []

# Simulation of banker job
# Estimates amount of time that
# client has to wait until served

class Client:
    def __init__(self, age, hurry=1):
        self.age = age
        self.hurry = hurry
        self.issue = [self.withdraw, self.paybills, self.createaccount]
        self.enteredTime = 0
        self.leftTime = 0
    def withdraw(self):
        return self.age // 5 * 60 // self.hurry

    def paybills(self):
        return random.randrange(60*5, 60*15)

    def createaccount(self):
        return random.randrange(60*15, 60*30) // self.hurry
    
    def howlong(self):
        return self.leftTime - self.enteredTime

class Banker:
    def __init__(self):
        self.finishTime = 0
    def busy(self):
        global time
        return self.finishTime > time
    def takeClient(self, client):
        if not self.busy():
            global time
            print('time: ', time)
            self.finishTime = time + client.issue
            client.lefTime = time + client.issue
            print('Ahtung: ', client.enteredTime, self.finishTime)
            waitingList.append(time - client.enteredTime)

        
def simulation(numSeconds, numBankers):
    queue = Queue() 
    bankers = []
    for n in range(numBankers):
        bankers.append(Banker())
    for i in range(numSeconds):
        global time
        time = i
        newClient = random.randrange(1, 721)
        if newClient == 720:
            newClient = Client(random.randrange(18, 90), random.choice([1,1,1,2,3]))
            newClient.issue = random.choice(newClient.issue)()
            newClient.enteredTime = time
            queue.enqueue(newClient)
            print('New client! Age={} Issue={} EnteredT={}'.format(
                newClient.age, newClient.issue, newClient.enteredTime))
        if queue.size() > 0:
            taken = None
            j = 0
            while not taken and j < len(bankers):
                banker = bankers[j]
                if not banker.busy():
                    print('Client age={} taken by Banker{}'.format(queue.peek().age, j))
                    banker.takeClient(queue.dequeue())
                    taken = True
                else:
                    j += 1
    
    print('\n Results: \n')
    print(waitingList)
    print('Average wait = {:.0f}min'.format(sum(waitingList) / len(waitingList) / 60))
    print('Still waiting: {}'.format(queue.size()))


eightHours = 60*60*8
simulation(eightHours, 1)


