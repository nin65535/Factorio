import numpy as np
import json




class Points(object):
    MAX_FIELD = 100

    def generate():
        points = np.random.randint(0,MAX_FIELD,(20,2))
        fw = open('points.json','w')
        json.dump(points.tolist() , fw)

    def read():
        f = open('points.json','r')
        points = np.array(json.load(f))
        return points