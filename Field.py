import json
import numpy as np
import collections
import random
import copy

from Configure import Configure as conf
from Facilities import Facilities as fc
from Materials import Materials as mt

class Field(object):
 
    free_cells = None
    conf = None

    def get_conf():
        if(Field.conf is None):
            Field.conf = conf.get('fields')
        return Field.conf


    def get_free_cells():
        if Field.free_cells is None:
            size = Field.get_conf()['size']
            Field.free_cells = np.ones(size)
            for pos in Field.get_conf()['fix'].values():
                Field.free_cells[pos[0]][pos[1]] = 0

        return Field.free_cells


    def __init__(self):
        size = Field.get_conf()['size']
        self._score = None
        self.cells :np.ndarray = np.zeros(size)
        
    def set_fix(self):
        for facility_name,pos in Field.get_conf()['fix'].items():
            fid = fc.get_id(facility_name)
            self.set_cell(pos,fid)

    def set_cell(self,pos,value):
        self.cells[pos[0]][pos[1]] = value
        self._score = None

    def get_cell(self,pos):
        return self.cells[pos[0]][pos[1]]

    def set_random(self):
        for facility_name,count in Field.get_conf()['free'].items():
            fid = fc.get_id(facility_name)
            pos = np.transpose(np.where(self.cells == 0))
            samples = random.sample(list(pos) , count)
            for sample in samples:
                self.set_cell(sample , fid)

    def get_score(self):
        m_max = len(mt.get_list())
        score = np.zeros(m_max)

        for m_id in range(m_max):
            #該当マテリアルに関連する施設のID
            f_ids = np.where(fc.get_map()[:,m_id])
            x,y = np.where(np.isin(self.cells , f_ids))
            if(len(x)):
                score[m_id] = max(x) - min(x) + max(y) - min(y)

        s = sum(score)
        return (0 if s == 0 else 1 / s)

    @property
    def score(self):
        if self._score is None:
            self._score = self.get_score()

        return self._score


    def swap_set(self,pos,value):
        if(self.get_cell(pos) == value):
            return
        pos2 = self.search(value)
        self.swap(pos,pos2)


    def swap(self,pos1,pos2):
        temp = self.get_cell(pos1)
        self.set_cell(pos1 , self.get_cell(pos2))
        self.set_cell(pos2 , temp)

    def search(self,value):
        p = np.transpose(np.where(self.cells == value))
        return random.choice(list(p))

    def get_random_area():
        f_size = np.array(Field.get_conf()['size'])
        size_max = np.floor((f_size + 1) / 2)
        size = [ random.randint(1,i) for i in size_max ]
        base = [ random.randint(0,i) for i in (f_size - size)]
        positions = np.array([[x,y] for x in range(size[0]) for y in range(size[1]) ]) + base
        return positions
    

    def cross(parent1,parent2,area):
        child = copy.deepcopy(parent1)
        for pos in area:
            v = parent2.get_cell(pos)
            child.swap_set(pos,v)
        return child

    def slide(self,step):
        f_size = np.array(Field.get_conf()['size'])

        pos_from = np.transpose(np.where(Field.get_free_cells()))

        def get_to(pf):
            pt = pf + step
            for d in range(len(pt)):
                if(pt[d] < 0):
                    pt[d] += f_size[d]

                if(pt[d] >= f_size[d]):
                    pt[d] -= f_size[d]

            if(not Field.get_free_cells()[pt[0]][pt[1]]):
                pt = get_to(pt)

            return pt

        pos_to = np.array([get_to(p) for p in pos_from])

        old_cells = copy.deepcopy(self.cells)

        for i in range(len(pos_to)):
            self.set_cell(pos_to[i] , old_cells[pos_from[i][0]][pos_from[i][1]])



    def mutate(self):
        step = random.choice([[0,1],[0,-1],[1,0],[-1,0],[0,0]])
        if(step == [0,0]):
            return

        self.slide(step)

    def print(self):
        print(self.get_named_cells())
        print(self.score)

    def get_named_cells(self):
        return np.vectorize(fc.get_name)(self.cells)