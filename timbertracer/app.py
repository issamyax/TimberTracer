#external imports
import pandas as pd


#internal imports
from ttlibs.dendrometer import dendrometer
from ttlibs.thinning import perform_thinning
from ttlibs.bucking import bucking_allocation
from ttlibs.processor import processor
from ttlibs.recycling import total_stock_calculator
from ttlibs.recycling import total_emission_calculator
from ttlibs.recycling import total_recycling_calculator
from ttlibs.substitution import energy_sub
from ttlibs.substitution import material_sub
import config as ttdata


def run_model(scale, shape, class_width, tolerance_g, a1, a2, b1, b2, b3, b4, a, c, alpha,
              beta, tolerance_hfind, efficiency, loss_allocation, recycling, substitution_matrix, decay, PH, R, management_dic, K, D, CC):

  result_df = pd.DataFrame()
  # loop over the management interventions
  for i in range(0, len(next(iter(management_dic.values())))):
    # dictionnary of an individual intervention
    dico =  {key: value[i] for key, value in management_dic.items()}
    # Projection period
    PP = PH - (dico.get('N_rotation') - 1)* R - dico.get('age')
    # Remaining period (that should receive 0)
    RP = PH - PP
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
    f = total_stock_calculator(resultat_reallocation, recycling, decay, PP, K, D, CC)
    # Compute emissions
    f1 = total_emission_calculator(resultat_reallocation, recycling, decay, PP, K, D, CC)
    # Compute energy substitution
    s1 = energy_sub(resultat_reallocation, recycling, substitution_matrix, decay, ttdata.C_CO2, PP)
    # Compute material substitution
    s3 = material_sub(resultat_reallocation, recycling, substitution_matrix, decay, ttdata.C_CO2, PP)
    # Total recycling *10
    rec = total_recycling_calculator(resultat_reallocation, recycling, decay, PP, K, D, CC)
    # Cumulative list of yearly emissions
    f2 = [0]#[s3[0]]
    for i in range(2, PP + 1):
        f2.append(f2[i - 2] + f1[i - 1])
    f2 = list0 + f2
    # Cumulative list of material substitution
    s2 = [s3[0]]
    for i in range(2, PP + 1):
        s2.append(s2[i - 2] + s3[i - 1])
    s2 = list0 + s2
    # Cumulative list of energy substitution
    s4 = [s1[0]]
    for i in range(2, PP + 1):
        s4.append(s4[i - 2] + s1[i - 1])
    s4 = list0 + s4
    # Add list0 before the starting of simulations
    f = list0 + f
    f1 = list0 + f1
    s1 = list0 + s1
    s3 = list0 + s3
    rec = list0 + rec
    # Organize outputs into a dataframe
    df = pd.DataFrame(list(zip(f, f1, f2, s1, s4, s3, s2, rec)), columns = ['C_Stock', 'Y_Emissions', 'C_Emissions', 'Y_ESUB', 'C_ESUB', 'Y_MSUB', 'C_MSUB', 'Y_REC'])
    # add dataframes contents
    result_df = result_df.add(df, fill_value = 0)

  return result_df


#run_model(scale = 20.33, shape= 5.65, class_width = 1 , tolerance_g = 0.3, a1 = 0.6626, a2 = 0.8769, b1= 0.9712, b2 = -0.2774, b3 = 1.1107, b4 = 26.4390,
#          a = 0.7, c = 1, alpha = 0.04, beta = 2.10, tolerance_hfind = 0.0001, efficiency = efficiency , loss_allocation = loss_allocation , recycling = recycling,
#          substitution_matrix = substitution_matrix, decay = decay, PH = 300, R = 100, management_dic = management_sim)
