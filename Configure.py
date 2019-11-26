from collections import OrderedDict as od
import json

class Configure(object):
    conf = None

    def get(name):
        if Configure.conf == None:
            Configure.conf = {}

        if Configure.conf.get(name) == None:
            f = open( name + '.json','r')
            Configure.conf[name] = od(json.load(f))

        return Configure.conf[name]

