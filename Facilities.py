from collections import OrderedDict as od
from Configure import Configure as conf
from Materials import Materials as mt
import numpy as np

class Facilities(object):

    #facility_id : facility_name
    list = None
    # map[f_id][m_id] = t/f
    map = None


    def get_map():

        if  Facilities.map is None:
            map = np.zeros((len(Facilities.get_list()) , len(mt.get_list())))

            for f_name , m_names in conf.get('facilities').items():
                f_id = Facilities.get_id(f_name)
                for m_name in m_names:
                    m_id = mt.get_id(m_name)

                    map[f_id][m_id] = 1

            Facilities.map = map
        return Facilities.map


    def get_list():
        if Facilities.list == None:
            Facilities.list = list(conf.get('facilities').keys())
            Facilities.list.sort()
            Facilities.list.insert(0,'None')

        return Facilities.list

    def get_id(label):
        return Facilities.get_list().index(label)

    def get_name(id):
        return Facilities.get_list()[int(id)]