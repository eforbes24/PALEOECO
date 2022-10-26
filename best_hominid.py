#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaleoEco Model - Best Individual

@author: eden
"""
import pickle
import numpy as np
from Hom_Evo_Lib import fitness

with open("best_individual", "rb") as f:
    best_individual = pickle.load(f)
    
fitness(best_individual["continuous_params"])
print(best_individual["continuous_params"]) 