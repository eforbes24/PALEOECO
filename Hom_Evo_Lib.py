#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaleoEco Model

@author: eden
"""
##### IMPORTS #####
import numpy as np
import math

def fitness(genome):
    class env:
        def __init__(self, init_pop, timesteps):

            ### CONSTANTS ###
            self.timesteps = timesteps
            self.init_pop = init_pop
            self.C = 0
            self.P = 0
            self.K = 0
            self.nutrient_inflow = 20
            self.nutrient_outflow = 0.1
            self.s_intensity = 0.8
            self.s_length = 0.0005

            ### BIOMASS RATIOS - SUM TO 1 ###
            self.biom_ratio = np.array([0.5, 0.3, 0.2])
        
            ### INITS ###
            self.nutrients = np.zeros(N)
            self.population = list()
            self.init_eq_steps = 50
            self.steps = 0

            ### LIFE HISTORY ###
            self.d_thresh = 50

        def influx(self):
            self.C = self.C + self.nutrient_inflow
            self.P = self.P + (self.s_intensity*self.nutrient_inflow)*math.sin(self.s_length*(self.steps + (1/self.s_length) * 1 * math.pi)) + self.s_intensity*self.nutrient_inflow
            self.K = self.K + (self.s_intensity*self.nutrient_inflow)*math.sin(self.s_length*(self.steps + (1/self.s_length) * 2 * math.pi)) + self.s_intensity*self.nutrient_inflow
        def outflux(self):
            self.C = self.C - self.nutrient_outflow*self.C
            self.P = self.P - self.nutrient_outflow*self.P
            self.K = self.K - self.nutrient_outflow*self.K

    class hominid:
        def __init__(self, env, genome):
            self.env = env
            self.makeup = np.array([50,50,50])
            self.biomass = 0
            self.genome = genome
            self.maxcon = 10
            self.col = 1

            self.c_loci = []
            self.s_loci = []
            self.e_loci = []
            
            ### Normalize genome ###
            for i in range((3)):
                self.c_loci.append(self.genome[i])
            for i in range((3)):
                self.s_loci.append(self.genome[i+(3)])
            for i in range((3)):
                self.e_loci.append(self.genome[i+(6)])
            sum_c = sum(self.c_loci)
            for i in range(len(self.c_loci)):
                self.c_loci[i] = abs(self.c_loci[i]/sum_c)
            sum_s = sum(self.s_loci)
            for i in range(len(self.s_loci)):
                self.s_loci[i] = abs(self.s_loci[i]/sum_s)
            sum_e = sum(self.e_loci)
            for i in range(len(self.e_loci)):
                self.e_loci[i] = abs(self.e_loci[i]/sum_e)

            self.biom_vec = np.zeros(env.timesteps)
        
        def feed(self,env):
            ## calculate C change
            C_in = (self.maxcon * self.e_loci[0]) * self.c_loci[0]
            C_out = 1 - self.makeup[0]*self.s_loci[0]
            self.makeup[0] = self.makeup[0] + C_in - C_out
            ## calculate P change
            P_in = (self.maxcon * self.e_loci[1]) * self.c_loci[1]
            P_out = 1 - self.makeup[1]*self.s_loci[1]
            self.makeup[1] = self.makeup[1] + P_in - P_out
            ## calculate K change
            K_in = (self.maxcon * self.e_loci[2]) * self.c_loci[2]
            K_out = 1 - self.makeup[2]*self.s_loci[2]
            self.makeup[2] = self.makeup[2] + K_in - K_out

            ## calculate biomass change by multiplying ratios by makeup
            biom_array = self.makeup*env.biom_ratio
            self.biomass = min(biom_array)
            self.biom_vec[env.steps] = self.biomass

    
    ## Inits
    test_env = env(100, 1000)
    test_hominid = hominid(test_env, genome)

    for i in range(test_env.init_eq_steps):
        test_env.influx()
        test_env.outflux()
    for i in range(test_env.timesteps):
        test_env.influx()
        test_hominid.feed()
        test_env.outflux()
        test_env.steps = test_env.steps + 1
    
    biom_avg = np.average(test_hominid.biom_vec)
    return(biom_avg)
