
"""
Here we present the parameters and inputs data necessary to running the model
"""

###########################
# Block wood use parameters
###########################

# Efficiency of the industrial processes
efficiency = {"Stump": 1, "fire": 1, "furniture": 0.45, "lumber": 0.5, "paper": 0.8 , "particle": 0.76, "sawing": 0.40, "toplog": 1}

# Reallocation of the industrial loss
loss_allocation = {"furniture": {"fire": 0.15, "particle": 0.1, "paper": 0.2, "millsite": 0.1},
                   "lumber": {"fire": 0.15 , "particle": 0.1, "paper": 0.15, "millsite": 0.10},
                   "sawing": {"fire": 0.2, "particle": 0.2, "paper": 0, "millsite": 0.1},
                   "particle":{"fire": 0.14, "particle":0, "paper": 0, "millsite": 0.2},
                   "paper": {"fire": 0, "particle": 0, "paper": 0, "millsite": 0.2}}

# Recycling data on products
recycling = {"furniture": {'r': 0.1, 'ls': 30 , 'fire': 0.8 , 'landfill': 0.1},
             "lumber": {'r': 0.1, 'ls': 65, 'fire': 0.8, 'landfill': 0.1},
             "paper": {'r': 0.1, 'ls': 1, 'fire': 0.8, 'landfill': 0.1},
             "sawing": {'r': 0.1, 'ls': 50, 'fire': 0.8, 'landfill': 0.1},
             "particle": {'r': 0.1, 'ls': 20, 'fire': 0.8 , 'landfill': 0.1}}


# Half-lifetime of "non-main-products"
decay = {"landfill": 145, "millsite": 5, "fire" : 1}

# Matrix of substitution coefficient. Values are by reference to the dry volume tCO2 / m3 (dry volume)
substitution_matrix = {"furniture": 0.82,
                       "lumber": 0.06,
                       "sawing": 0.32,
                       "particle": 0.2,
                       "fire": 0.48}

# Moisture content
MC = 0.12
K = 1/(1+MC)

# Density and carbon content
D = 0.588 #t/m3 # https://doi.org/10.1007/s13595-018-0734-6 (source from where density has been extracted)
CC = 0.5 # proportion of carbon in the dry biomass
C_CO2 = 3.67 # The conversion factor from C to CO2

##########


#Management Scenarios

management_jardin = {"N_rotation": [1, 1, 1, 1, 1],
            "age": [39, 63, 78, 93, 108],
            "total_pop" : [1396, 532, 314, 192, 123],
            "target_sum": [10.47, 11.70, 11.68, 11.69, 11.53],
            "DBH": [19.54, 31.61, 41.12, 52.61, 65.3],
            "bark": [1.5, 1.5, 1.5, 1.5, 1.5],
            "sap_area": [199.72, 412.95, 634, 979, 1415],
            "heart_area": [100.31, 372.21, 693, 1195, 1933],
            "thinning_type": ['above', 'above', 'above', 'above', 'above']}

management_clearcut = {"N_rotation": [1, 1],
            "age": [39, 84],
            "total_pop" : [1396, 275],
            "target_sum": [10.47, 41.83],
            "DBH": [19.54, 44.01],
            "bark": [1.5, 1.5],
            "sap_area": [199.72, 698.16],
            "heart_area": [100.31, 823.18],
            "thinning_type": ['above', 'neutral']}


management_shelter = {"N_rotation": [1, 1, 1, 1, 1],
            "age": [39, 63, 73, 84, 94],
            "total_pop" : [1396, 532, 376, 261, 52],
            "target_sum": [10.47, 8.35, 8.38, 33.44, 14.51],
            "DBH": [19.54, 31.62, 37.67, 45.16, 59.61],
            "bark": [1.5, 1.5, 1.5, 1.5, 1.5],
            "sap_area": [199.72, 412.95, 550.07,750.85, 1552.51],
            "heart_area": [100.31, 372.21, 564.51, 851.08, 1238.62],
            "thinning_type": ['above', 'bottom', 'bottom', 'neutral', 'neutral']}

#Wood use scenarios

recycling_BAU = {"furniture": {'r': 0.1, 'ls': 30 , 'fire': 0.8 , 'landfill': 0.1},
            "lumber": {'r': 0.1, 'ls': 65, 'fire': 0.8, 'landfill': 0.1},
            "paper": {'r': 0.1, 'ls': 1, 'fire': 0.8, 'landfill': 0.1},
            "sawing": {'r': 0.1, 'ls': 50, 'fire': 0.8, 'landfill': 0.1},
            "particle": {'r': 0.1, 'ls': 20, 'fire': 0.8 , 'landfill': 0.1}}

recycling_RR10 = {"furniture": {'r': 0.11, 'ls': 30 , 'fire': 0.79 , 'landfill': 0.1},
            "lumber": {'r': 0.11, 'ls': 65, 'fire': 0.79, 'landfill': 0.1},
            "paper": {'r': 0.11, 'ls': 1, 'fire': 0.79, 'landfill': 0.1},
            "sawing": {'r': 0.11, 'ls': 50, 'fire': 0.79, 'landfill': 0.1},
            "particle": {'r': 0.11, 'ls': 20, 'fire': 0.79 , 'landfill': 0.1}}

recycling_LS10 = {"furniture": {'r': 0.1, 'ls': 33 , 'fire': 0.8 , 'landfill': 0.1},
            "lumber": {'r': 0.1, 'ls': 71.5, 'fire': 0.8, 'landfill': 0.1},
            "paper": {'r': 0.1, 'ls': 1.1, 'fire': 0.8, 'landfill': 0.1},
            "sawing": {'r': 0.1, 'ls': 55, 'fire': 0.8, 'landfill': 0.1},
            "particle": {'r': 0.1, 'ls': 22, 'fire': 0.8 , 'landfill': 0.1}}

recycling_RRLS10 = {"furniture": {'r': 0.11, 'ls': 33 , 'fire': 0.79 , 'landfill': 0.1},
            "lumber": {'r': 0.11, 'ls': 71.5, 'fire': 0.79, 'landfill': 0.1},
            "paper": {'r': 0.11, 'ls': 1.1, 'fire': 0.79, 'landfill': 0.1},
            "sawing": {'r': 0.11, 'ls': 55, 'fire': 0.79, 'landfill': 0.1},
            "particle": {'r': 0.11, 'ls': 22, 'fire': 0.79, 'landfill': 0.1}}

dynamic_subs_file = "dynamic_subs.xlsx"
