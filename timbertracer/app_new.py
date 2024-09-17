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
from ttlibs.recycling_methane import total_stock_calculator_ipcc
from ttlibs.recycling_methane import total_emission_calculator_methane
from ttlibs.substitution_dynamic import energy_sub_dynamic
from ttlibs.substitution_dynamic import material_sub_dynamic
from ttlibs.substitution_dynamic import substitution_factors_dynamic
import config as ttdata

def run_model(scale, shape, class_width, tolerance_g, a1, a2, b1, b2, b3, b4, a, c, alpha,
              beta, tolerance_hfind, efficiency, loss_allocation, recycling, decay, PH, R, management_dic,
              t05 = 10, L0 = 0.1, MM_C= 12, MM_CO2 = 44, MM_CH4 = 16, GWP_CH4 = 28, f = 0.5, C_CO2 = 3.67, D = 0.588 , MC = 0.22, CC = 0.5, K = 1/1.22):

  # initiate an empty dataframe where to store resulting variables
  result_df = pd.DataFrame()

  # read the emission trend by https://www.science.org/doi/10.1126/science.aah3443
  df_DSEF = substitution_factors_dynamic(2010, PH) # where 2010 is the reference year here by default as set by Rockstrom - please consult the function documentation more above for further infos

  # loop over the management interventions
  for i in range(0, len(next(iter(management_dic.values())))):
    # dictionnary of an individual intervention
    dico =  {key: value[i] for key, value in management_dic.items()}
    # Projection period
    PP = PH - (dico.get('N_rotation') - 1)* R - dico.get('age')
    # Remaining period (that should receive 0)
    RP = PH - PP
    # filter the df_DSEF to include only the years of interest - between [2010 + (N°Rotation -1).R + age ] && [2010 + PH]
    df_DSEF_filtered = df_DSEF[(df_DSEF['year'] >= 2010 + (dico.get('N_rotation') - 1)*R + dico.get('age')) & (df_DSEF['year'] <= PH + 2010)] # total rows == PP + 1
    # generate the stand
    first_step = dendrometer(scale = scale, shape = shape, total_population = dico.get('total_pop'), class_width = class_width, DBH = dico.get('DBH'))
    # perform the thinning
    second_step = perform_thinning(trees_df= first_step, thinning_type= dico.get('thinning_type'), target_sum = dico.get('target_sum'), tolerance = tolerance_g)
    second_step = first_step[first_step['ID'].isin(second_step)]
    # perform the dissagregation
    third_step = second_step.apply(lambda row: bucking_allocation(dbh = row['Diameter_Center'], ht = row['Height_Center'], a1 = a1, a2 = a2, b1 = b1, b2 = b2, b3 = b3, b4 = b4, bark = dico.get('bark'), a = a, c = c, alpha = alpha, beta = beta, DBH = dico.get('DBH'), sap_area = dico.get('sap_area'), heart_area = dico.get('heart_area'), tolerance = tolerance_hfind), axis=1)
    resultat = pd.concat(third_step.tolist())
    resultat = resultat.groupby('product')['volume'].sum().reset_index()
    # Wood processing
    resultat_reallocation = processor(resultat, efficiency = efficiency, loss_allocation = loss_allocation)
    # Generate list of 0s before the start of projection
    list0 = [0] * RP
    # Compute stock
    f0 = total_stock_calculator_ipcc(resultat_reallocation, recycling, decay, PP+1, t05, L0, f,  D, MC, CC, MM_CO2, MM_C, MM_CH4, GWP_CH4) #modified from number of years to period from PP -> PP+1
    # Compute emissions
    f1 = total_emission_calculator_methane(resultat_reallocation, recycling, decay, PP+1, t05, L0, f, D, MC, CC, K, MM_CO2, MM_C, MM_CH4, GWP_CH4) #modified from number of years to period from PP -> PP+1
    # Compute energy substitution
    s1 = energy_sub_dynamic(resultat_reallocation, recycling, df_DSEF_filtered , decay, C_CO2, PP+1, K) #modified from number of years to period from PP -> PP+1
    # Compute material substitution
    s3 = material_sub_dynamic(resultat_reallocation, recycling, df_DSEF_filtered, decay, C_CO2, PP+1) #modified from number of years to period from PP -> PP+1
    # Total recycling *10
    rec = total_recycling_calculator(resultat_reallocation, recycling, decay, PP+1) #modified from number of years to period from PP -> PP+1
    # Cumulative list of yearly emissions
    f2 = [0]#[s3[0]]
    for i in range(2, PP + 2): # changed from PP+1 => PP+2 because range doesn't account for the last element and the number of years = period + 1
        f2.append(f2[i - 2] + f1[i - 1])
    f2 = list0 + f2
    # Cumulative list of material substitution
    s2 = [s3[0]]
    for i in range(2, PP + 2): # changed from PP+1 => PP+2 because range doesn't account for the last element and the number of years = period + 1
        s2.append(s2[i - 2] + s3[i - 1])
    s2 = list0 + s2
    # Cumulative list of energy substitution
    s4 = [s1[0]]
    for i in range(2, PP + 2): # changed from PP+1 => PP+2 because range doesn't account for the last element and the number of years = period + 1
        s4.append(s4[i - 2] + s1[i - 1])
    s4 = list0 + s4
    # Add list0 before the starting of simulations
    f0 = list0 + f0
    f1 = list0 + f1
    s1 = list0 + s1
    s3 = list0 + s3
    rec = list0 + rec
    # Organize outputs into a dataframe
    df = pd.DataFrame(list(zip(f0, f1, f2, s1, s4, s3, s2, rec)), columns = ['C_Stock', 'Y_Emissions', 'C_Emissions', 'Y_ESUB', 'C_ESUB', 'Y_MSUB', 'C_MSUB', 'Y_REC'])
    # add dataframes contents
    result_df = result_df.add(df, fill_value = 0)

  return result_df

