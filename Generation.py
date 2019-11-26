from Field import Field as fl
import random
import json
import numpy as np

class Generation(object):
    
    def __init__(self):
        self.pool = []
        self.call()

    def call(self):
        while len(self.pool) < 2:
            f = fl()
            f.set_fix()
            f.set_random()
            self.pool.append(f)

    def cross(self):
        while(len(self.pool) < 2):
            self.call()

        parents = random.sample(self.pool , 2)
        for parent in parents:
            self.pool.remove(parent)

        area = fl.get_random_area()

        children = []
        children.append(fl.cross(parents[0] , parents[1] , area))
        children.append(fl.cross(parents[1] , parents[0] , area))

        children[1].mutate()

        parents.sort(key=lambda f:f.score)
        children.sort(key=lambda f:f.score)

        if parents[1].score < children[0].score:
            self.pool.append(parents[1])
            self.pool.append(children[0])
            self.pool.append(children[1])
            return

        if children[1].score < parents[0].score:
            self.pool.append(parents[1])
            return

        if parents[1].score > children[1].score:
            self.pool.append(parents[1])
            self.pool.append(children[1])
            return

        self.pool.append(children[1])
        self.call()
        return

    def get_answer(self):
        self.pool.sort(key = lambda f:f.score)
        return self.pool[-1]


    def print_answer(self):
        f = self.get_answer()
        f.print()

    def print_all(self):
        for p in self.pool:
            p.print()

    def save(self):
        f = open('result.json','w')
        json.dump(self.get_answer().cells.tolist(),f)

    def load(self):
        f = fl()
        f.cells = np.array(json.load(open('result.json','r')))
        self.pool.append(f)