from Materials import Materials as mt
from Facilities import Facilities as fc
from Field import Field as fl
import numpy as np
from Configure import Configure as conf
from Generation import Generation as gen
import random
import json

g = gen()
#g.load()

for i in range(10000):
    if not i % 1000:
        print(i)
    g.cross()

g.print_answer()

g.save()