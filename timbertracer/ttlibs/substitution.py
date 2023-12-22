import scipy.stats as stats
from ttlibs.recycling import compute_D, compute_R
import config as ttdata

def energy_sub(df, recycling_matrix, substitution_matrix, decay_matrix, C_CO2, n):
  """
  This function computes the annual energy substitution
  """
  result_list1 = []
  SEF = substitution_matrix['fire']
  # Iterate through the DataFrame rows
  for index, row in df.iterrows():
      product1 = row['product']
      filtered_substitution_matrix = {key: value for key, value in substitution_matrix.items() if key != 'fire'}
      if product1 in filtered_substitution_matrix:
          r1 = recycling_matrix[product1]['r']
          r2 = recycling_matrix[product1]['fire']
          init_stock1 = row['post_process_volume']*ttdata.K #K drying
          lifespan1 = recycling_matrix[product1]['ls']
          result2 = compute_D(n, r1, init_stock1, lifespan1, r2)
          result_list1.append(result2)


  # Sum the elements at corresponding positions in the lists
  sum_result1 = [sum(x) for x in zip(*result_list1)]
  sum_result1[0] = df[df['product']== 'fire']['post_process_volume'].iloc[0]


  # Create a normal distribution
  distribution1 = stats.norm(decay_matrix["fire"], decay_matrix["fire"] / 3)

  FRE = [0]
  # Calculate FRE values for indices 2 to n
  for i in range(2, n+1):
    termo = 0
    for j in range(1, i):
      termo += sum_result1[j-1] * (distribution1.cdf(i-j) - distribution1.cdf(i-j-1))
    FRE.append(termo)

  FRE = [x*SEF/C_CO2 for x in FRE] # SEF: Substitution for Energy, C_CO2: C to CO2 conversion factor
  return FRE

def material_sub(df, recycling_matrix, substitution_matrix, decay_matrix, C_CO2, n):
  """
  This function computes the annual material substitution
  """
  result_list1 = []
  # Iterate through the DataFrame rows
  for index, row in df.iterrows():
      product1 = row['product']
      filtered_substitution_matrix = {key: value for key, value in substitution_matrix.items() if key != 'fire'}
      if product1 in filtered_substitution_matrix:
          r1 = recycling_matrix[product1]['r']
          SC = filtered_substitution_matrix[product1]
          init_stock1 = row['post_process_volume']*ttdata.K #K drying
          lifespan1 = recycling_matrix[product1]['ls']
          result2 = compute_R(n, r1, init_stock1, lifespan1)
          result2[0] = init_stock1
          result2 = [x*SC for x in result2]
          result_list1.append(result2)

  sum_result1 = [sum(x) for x in zip(*result_list1)]
  sum_result1 = [x/C_CO2 for x in sum_result1]

  return sum_result1

