#external imports
import pandas as pd


#internal imports
from ttlibs.dendrometer import dendrometer
from ttlibs.thinning import perform_thinning
from ttlibs.bucking import bucking_allocation
from ttlibs.processor import processor
from ttlibs.recycling_methane import total_stock_calculator
from ttlibs.recycling_methane import total_emission_calculator
from ttlibs.recycling_methane import total_recycling_calculator
from ttlibs.substitution_dynamic import energy_sub_dynamic
from ttlibs.substitution_dynamic import material_sub_dynamic
import config as ttdata

