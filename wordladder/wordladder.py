#! /usr/bin/python3

import sys

class PQueue:

  def OrdinaryComparison(self,a,b):
    if a < b: return -1
    if a == b: return 0
    return 1

  def __init__(self, comparator = None):
    if comparator == None:
      comparator = self.OrdinaryComparison
    self.queue = [0]
    self.length = 1
    self.cmpfunc = comparator

  def __str__(self):
    return "[[[" + '\n'.join([str(i) for i in self.queue]) + "]]]"

  def switch(self, a, b):
    temp = self.queue[a]
    self.queue[a] = self.queue[b]
    self.queue[b] = temp

  def push(self, data):
    if len(self.queue)>self.length:
      self.queue[self.length] = data
    else:
      self.queue.append(data)
    self.length+=1
    index = self.length-1
    while (index//2!=0 and self.cmpfunc(data, self.queue[index//2])==-1):
      self.switch(index, index//2)
      index = index//2

  def pop(self):
    if self.length>1:
      root = self.queue[1]
      #print("self.length: " + str(self.length))
      #print("len(self.queue): " + str(len(self.queue)))
      if self.length>2:
        self.queue[1] = self.queue[self.length-1]
        self.length-=1
        index = 1
        while(index*2<self.length):
          #print("index: " + str(index))
          if (index*2+1<self.length):
            if (self.cmpfunc(self.queue[index],self.queue[index*2+1])==1 and
                self.cmpfunc(self.queue[index*2+1],self.queue[index*2])==-1):
              self.switch(index, index*2+1)
              index = index*2+1
            elif (self.cmpfunc(self.queue[index],self.queue[index*2])==1):
              self.switch(index, index*2)
              index = index*2
            else:
              index = self.length
          elif (self.cmpfunc(self.queue[index],self.queue[index*2])==1):
            #print("index: " + str(index))
            self.switch(index, index*2)
            index = index*2
          else:
            index = self.length
      else:
        self.queue[1] = None
        self.length-=1
      return root
    return None

  def peek(self):
    if len(self.queue)>1:
      return self.queue[1]

  def tolist(self):
    list = []
    while (self.peek()!=None):
      list.append(self.pop())
    return list

  def push_all(self, list):
    for x in range(len(list)):
        self.push(list[x])

  def internal_list(self):
    list = []
    index = 1
    while (index<self.length):
        list.append(self.queue[index])
        index+=1
    return list

def makeDict():
    dict_f = open("dictall.txt", "r")
    dict_f_cont = dict_f.read()
    words = dict_f_cont.split('\n')
    subdict = set()
    for i in range(len(words)):
        if len(words[i])==4:
            subdict.add(words[i])
    result = {}
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for x in subdict:
        result[x] = []
        word = x
        for i in range(len(x)):
            for s in alphabet:
                word = x[:i] + s + x[i+1:]
                if word in subdict and word != x:
                    result[x].append(word)
    #print(result)
    return result

def read_input():
    req_f = open(sys.argv[1], "r")
    req_f_cont = req_f.read()
    requests = req_f_cont.split('\n')
    req_f.close()
    #print(requests)
    index = len(requests)-1
    while requests[index]=='':
        del requests[index]
        index-=1
    #print(requests)
    return requests

def write_output(string):
    ans_f = open(sys.argv[2], 'w')
    ans_f.write(string)
    ans_f.close()

class Node:
    def __init__(self, value):
        self.word = value
        self.g = 0
        self.h = 0
        self.path = []

    def __str__(self):
        return self.word + ', ' + str(self.g) + ', ' + str(self.h) + ', ' + ','.join(self.path)

def g(node_prev):
    return node_prev.g + 1

def h(node, target):
    dist_away = 0
    for x in range(len(node.word)):
        if node.word[x]!=target[x]:
            dist_away+=1
    return dist_away

def my_cmp(a, b):
    if a.g + a.h < b.g + b.h: return -1
    if a.g + a.h == b.g + b.h: return 0
    return 1

def search(input):
    nbors = makeDict()
    #print(nbors)
    output = ""
    for x in input:
        target = x.split(',')[1]
        explored = []
        frontier = PQueue(comparator = my_cmp)
        frontier.push(Node(x.split(',')[0]))
        current = frontier.pop()
        #print("cur word: " + current.word)
        #print("frontier: " + str(frontier))
        while current!=None and current.word != target:
            #print("cur word: " + current.word)
            for i in nbors[current.word]:
                if i not in explored:
                    neighbor = Node(i)
                    neighbor.g = g(current)
                    neighbor.h = h(neighbor, target)
                    neighbor.path.extend(current.path)
                    neighbor.path.append(current.word)
                    frontier.push(neighbor)
            #print("frontier: " + str(frontier))
            #print("NBOR LOOP ENDED")
            explored.append(current.word)
            current = frontier.pop()
        if current!=None:
            output = output + ','.join(current.path) + ',' + current.word + "\n"
        else:
            output = output + x.split(',')[0] + ',' + target + '\n'
    return output

def main():
    #print("running")
    requests = read_input()
    #print(requests)
    output = search(requests)
    write_output(output)

main()
