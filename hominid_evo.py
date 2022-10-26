#!/usr/bin/env python
"""
PaleoEco Model - Evolution Run

@author: eden
"""

from tkinter import W
import numpy as np
import pickle
# WARNING I AM FILTERING WARNINGS BECUASE PATHOS DOESN'T LIKE THEM
import warnings
warnings.filterwarnings("ignore")

from EvolSearch import EvolSearch
from Hom_Evo_Lib import fitness
from functools import partial


use_best_individual = False
if use_best_individual:
    with open("best_individual", "rb") as f:
        best_individual = pickle.load(f)

########################
# Parameters
########################
gens = 100
pop_size = 100
## FIXED
continuous_genotype_size = 9

########################
# Evolve Solutions
########################
evol_params = {
    "num_processes": 100,
    "pop_size": pop_size,  # population size
    "continuous_genotype_size": continuous_genotype_size,  # dimensionality of solution
    "fitness_function": partial(fitness),  # custom function defined to evaluate fitness of a solution
    "elitist_fraction": 0.1,  # fraction of population retained as is between generation
    "continuous_mutation_variance": 0.1,  # mutation noise added to offspring.
}
continuous_initial_pop = np.random.uniform(0, 1, size=(pop_size, continuous_genotype_size))

#if use_best_individual:
#    initial_pop[0] = best_individual["params"]

evolution = EvolSearch(evol_params, continuous_initial_pop)

save_best_individual = {
    "continuous_params": None,
    "best_fitness": [],
    "mean_fitness": [],
}

for i in range(gens):
    evolution.step_generation()
    
    save_best_individual["continuous_params"] = evolution.get_best_individual()
    
    save_best_individual["best_fitness"].append(evolution.get_best_individual_fitness())
    save_best_individual["mean_fitness"].append(evolution.get_mean_fitness())

    print(
        len(save_best_individual["best_fitness"]), 
        save_best_individual["best_fitness"][-1], 
        save_best_individual["mean_fitness"][-1]
    )

    with open("best_individual", "wb") as f:
        pickle.dump(save_best_individual, f)